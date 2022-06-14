# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_po = fields.Binary(tracking=True, string='Customer P.O')
    customer_po_filename = fields.Char(tracking=True)

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('waiting_for_approval', 'Waiting For Manager'),
        ('waiting_for_approval_ceo', 'Waiting For CEO'),
        ('ready_to_confirm', 'Ready to Confirm'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def submit_for_approval(self):
        for rec in self:
            rec.state = 'waiting_for_approval'

    def confirm_by_manager(self):
        for rec in self:
            rec.state = 'waiting_for_approval_ceo'

    def confirm_by_ceo(self):
        for rec in self:
            rec.state = 'ready_to_confirm'

    def approve_sale_order(self):
        # for rec in self:
        # rec.action_confirm()
        # rec.state = 'sale'
        res = super(SaleOrder, self).action_confirm()
        return res
    #
    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
    #                     submenu=False):
    #     res = super().fields_view_get(view_id, view_type, toolbar, submenu)
    #     if self._context.get('params'):
    #         sale = self.env["sale.order"].browse(self._context.get('params').get('id'))
    #         # if toolbar and 'print' in res['toolbar'] and sale.state not in ('ready_to_confirm','sale','done'):
    #         #      res['toolbar'].pop('print')
    #
    #         if sale.state not in ('ready_to_confirm','sale','done'):
    #             if res.get('toolbar', False) and res.get('toolbar').get('print', False):
    #                 reports = res.get('toolbar').get('print')
    #                 for report in reports:
    #                     res['toolbar']['print'].remove(report)
    #     return res

