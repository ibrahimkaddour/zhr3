# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    deliveries = fields.Char('Delivery Details', compute='_get_invoiced_data')
    payments = fields.Char('Payment Status', compute='_get_invoiced_data')

    @api.depends()
    def _get_invoiced_data(self):
        for order in self:
            invoices = order.order_line.invoice_lines.move_id.filtered(lambda r: r.move_type == 'out_invoice')
            data = ''
            for invoice in invoices:
                code = dict(invoice._fields['payment_state'].selection).get(invoice.payment_state)
                data += invoice.name + ':' + code + '|'
            order.payments = data[:-1]
            data = ''
            for pick in order.picking_ids:
                if pick.state != 'cancel':
                    data += pick.name + ':' + str(pick.scheduled_date) + '|'
            order.deliveries = data[:-1]

