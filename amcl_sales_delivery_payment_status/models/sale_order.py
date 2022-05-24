# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    deliveries = fields.Char('Delivery Details', compute='_get_invoiced_data', store=True)
    payments = fields.Char('Payment Status', compute='_get_invoiced_data', store=True)

    @api.depends('order_line.invoice_lines','picking_ids')
    def _get_invoiced_data(self):
        for order in self:
            invoices = order.order_line.invoice_lines.move_id.filtered(
                lambda r: r.move_type in ('out_invoice', 'out_refund'))
            data = ''
            for invoice in invoices:
                data += invoice.name + ':' + str(invoice.payment_state).upper().replace('_', ' ') + '|'

            order.payments = data
            data = ''
            for pick in order.picking_ids:
                data += pick.name + ':' + str(pick.scheduled_date)+ '|'
            order.deliveries = data
