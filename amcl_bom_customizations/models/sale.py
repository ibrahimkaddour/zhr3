# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import json
import odoo.addons.decimal_precision as dp


class Sale(models.Model):
    _inherit = 'sale.order'

    show_request_bom = fields.Boolean(string='Show Request BOM', compute="set_show_request_bom")
    bom_request_id = fields.Many2one('bom.request', string='BOM Request', copy=False)

    def action_confirm(self):
        if self.show_request_bom and not self.bom_request_id:
            raise ValidationError('Please request non standard BOM.')
        elif self.bom_request_id and self.bom_request_id.state != 'confirmed':
            raise ValidationError('Please Approve the BOM Request.')
        self.validate_order_line()
        res = super(Sale, self).action_confirm()
        return res

    def action_cancel(self):
        res = super().action_cancel()
        # if the order is canceled then remove relationship to BOM request
        self.bom_request_id.cancel_dummy_bom()
        self.bom_request_id.write({
            'state': 'cancel'
        })
        self.write({
            'bom_request_id': False,
        })
        for line in self.order_line:
            line.bom_id = False
            line.drawing = ''
        self.set_show_request_bom()
        return res

    def validate_order_line(self):
        for line in self.order_line:
            if line.product_id.non_standard_bom and not line.bom_id:
                raise ValidationError("Assign BOM in order line where product '%s' is added." % (line.product_id.name))
            if line.product_id.standard_bom and not line.bom_id:
                raise ValidationError(
                    "Assign Standard BOM in order line where product '%s' is added." % (line.product_id.name))

    def action_view_bom_request(self):
        bom_requests = self.mapped('bom_request_id')
        context = {
            'id': bom_requests.id,
        }
        return {
            'type': 'ir.actions.act_window',
            'name': 'BOM Request',
            'view_mode': 'form,tree',
            'res_model': 'bom.request',
            'res_id': bom_requests.id,
            'domain': [('id', '=', bom_requests.id)],
            'context': context
        }

    def request_bom(self):
        product_data = self.get_non_standard_prd_data()
        values = {
            'order_id': self.id,
            'bom_request_line_ids': product_data
        }
        bom_request_id = self.create_bom_request(values)
        self.write({
            'bom_request_id': bom_request_id.id,
        })

    def create_bom_request(self, values):
        BOMRequest = self.env['bom.request']
        return BOMRequest.create(values)

    def get_non_standard_prd_data(self):
        data = []
        for line in self.order_line:
            if line.product_id.non_standard_bom:
                data.append((0, 0, {
                    'product_id': line.product_id.id,
                    'description': line.name,
                    'label': line.label,
                    'drawing': line.drawing,
                    'quantity': line.product_uom_qty,
                    # 'quantity': 1,
                    'product_uom_id': line.product_uom.id,
                    'order_line_id': line.id
                }))
        return data

    @api.depends('order_line.product_id', 'order_line.bom_id', 'bom_request_id', 'state')
    def set_show_request_bom(self):
        show = False
        if self.state == 'ready_to_confirm' and not self.bom_request_id:
            for line in self.order_line:
                if line.product_id.non_standard_bom and not line.bom_id:
                    show = True
                    break

        self.show_request_bom = show

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
