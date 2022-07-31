# -*- coding:utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import fields, models, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    routing_id = fields.Many2one('mrp.routing', string='Routing', compute='set_routing')
    partner_id = fields.Many2one('res.partner', string='Client Name')
    client_name = fields.Char(string='Client Name', compute='set_client', store=True)
    client_order_ref = fields.Char(string='Customer Reference')
    line_no = fields.Char(string="Line No", related='bom_id.line_no')
    sale_reference = fields.Many2one('sale.order.line', string='SO Line', compute='_compute_reference_value')
    product_desc = fields.Text(related='sale_reference.name')

    @api.depends('origin')
    def _compute_reference_value(self):
        for value in self:
            sale_ids = self.env['sale.order'].search([('name', '=', value.origin)]).order_line.filtered(
                lambda m: m.product_uom_qty == value.product_qty and m.product_id.id == value.product_id.id)
            print('mo  name:: ', value.name)
            print('sale ids:: ', sale_ids)
            if sale_ids:
                for sale in sale_ids:
                    value.sale_reference = sale.id
            else:
                mrp_ids = self.env['mrp.production'].search([('name', '=', value.origin)])
                value.sale_reference = mrp_ids.sale_reference.id

    @api.depends('origin')
    def set_client(self):
        for each in self:
            if each.origin:
                sale_order_id = self.env['sale.order'].search([('name', '=', each.origin)])
                if sale_order_id:
                    each.client_name = sale_order_id.partner_id.name
                    each.client_order_ref = sale_order_id.client_order_ref

    @api.depends('bom_id')
    def set_routing(self):
        routing_id = False
        if self.bom_id and self.bom_id.id:
            routing_id = self.bom_id.routing_id.id
        self.routing_id = routing_id

    def unlink(self):
        if any(production.state not in ['draft', 'cancel'] for production in self):
            raise ValidationError(_('Cannot delete a manufacturing order not in draft or cancel state'))
        return super().unlink()

    def action_confirm(self):
        if self._context.get('from_saleorder', False):
            return True
        for mrp in self:
            if mrp.sale_reference and mrp.sale_reference.bom_id and mrp.sale_reference.bom_id != mrp.bom_id.id:
                mrp.state = 'draft'
                mrp.move_raw_ids.unlink()
                mrp.bom_id = mrp.sale_reference.bom_id.id
                mrp.product_qty = mrp.sale_reference.bom_id.product_qty
                mrp.product_uom_id = mrp.sale_reference.bom_id.product_uom_id.id
                mrp._onchange_product_id()
                mrp._onchange_move_raw()
        res = super().action_confirm()
        return res

class Workorder(models.Model):
    _inherit = 'mrp.workorder'

    sale_reference = fields.Many2one('sale.order.line', 'SO Reference', related='production_id.sale_reference')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
