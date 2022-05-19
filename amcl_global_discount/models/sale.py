# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import json
import odoo.addons.decimal_precision as dp

class Sale(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.price_total', 'discount_rate')
    def _amount_all(self):
        for order in self:
            price_before_discount = amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_discount += line.discount_amount
                price_before_discount += line.price_before_discount
                # amount_discount += (line.product_uom_qty * line.price_unit * line.discount) / 100
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'price_before_discount': price_before_discount,
                'amount_discount': amount_discount,
                'amount_total': amount_untaxed + amount_tax,
            })

    discount_type = fields.Selection([('fixed_amount', 'Fixed Amount'),
                                      ('percentage_discount', 'Percentage')],
                                     string='Discount type',
                                     readonly=True,
                                     states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                     default='percentage_discount')
    discount_rate = fields.Float('Discount Rate', digits=dp.get_precision('Account'),
                                 readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all',
                                 track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
                                   track_visibility='always')

    price_before_discount = fields.Monetary('Total ( Excluded VAT)', compute='_amount_all', store=True,
                                            readonly=True)
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_all',
                                      digits=dp.get_precision('Account'), track_visibility='always')

    @api.onchange('discount_type', 'discount_rate', 'order_line')
    def supply_rate(self):
        for order in self:
            if order.discount_type == 'percentage_discount':
                for line in order.order_line:
                    line.discount = order.discount_rate
            else:
                total = discount = 0.0
                for line in order.order_line:
                    total += round((line.product_uom_qty * line.price_unit))
                if order.discount_rate != 0:
                    discount = (order.discount_rate / total) * 100
                else:
                    discount = order.discount_rate
                for line in order.order_line:
                    line.discount = discount
                    line._compute_amount()

    def _prepare_invoice(self, ):
        invoice_vals = super(Sale, self)._prepare_invoice()
        invoice_vals.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
        })
        return invoice_vals

    def button_dummy(self):
        self.supply_rate()
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
