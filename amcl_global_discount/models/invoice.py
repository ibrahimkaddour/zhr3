# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    discount = fields.Float('Discount', compute='_compute_all_price')
    price_before_discount = fields.Monetary('Total ( Excluded VAT)', compute='_compute_all_price')

    discount_type = fields.Selection([('fixed_amount', 'Fixed Amount'),
                                      ('percentage_discount', 'Percentage')], string='Discount Type',
                                     readonly=True, states={'draft': [('readonly', False)]},
                                     default='percentage_discount')
    discount_rate = fields.Float('Discount Amount', digits=(16, 2), readonly=True,
                                 states={'draft': [('readonly', False)]})
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount',
                                      track_visibility='always')

    @api.depends('invoice_line_ids', 'amount_untaxed', 'amount_tax')
    def _compute_all_price(self):
        price_before_discount = discount = 0
        for line in self.invoice_line_ids:
            price_before_discount += line.price_before_discount
            discount += line.discount_amount

        self.price_before_discount = price_before_discount
        self.discount = discount

    @api.onchange('discount_type', 'discount_rate', 'invoice_line_ids')
    def supply_rate(self):
        for inv in self:
            if inv.discount_type == 'percentage_discount':
                for line in inv.line_ids:
                    line.discount = inv.discount_rate
                    line._onchange_price_subtotal()
            else:
                total = discount = 0.0
                for line in inv.invoice_line_ids:
                    total += (line.quantity * line.price_unit)
                if inv.discount_rate != 0 and total > 0:
                    discount = (inv.discount_rate / total) * 100
                else:
                    discount = inv.discount_rate
                for line in inv.line_ids:
                    line.discount = discount
                    line._compute_tax_line_id()
                    line._onchange_price_subtotal()

            inv._compute_tax_totals_json()
    #

    def button_dummy(self):
        self.supply_rate()
        return True


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    discount = fields.Float(string='Discount (%)', digits=(16, 20), default=0.0)
    tax_amount = fields.Monetary('Tax amount', compute='_compute_tax_amount', store=True)
    discount_amount = fields.Float('Discount Amount', compute='_compute_all_price', store=True)
    price_before_discount = fields.Monetary('Price B/f Disc', compute='_compute_all_price', store=True)

    @api.depends('discount', 'price_unit', 'quantity')
    def _compute_all_price(self):
        for line in self:
            line.price_before_discount = line.quantity * line.price_unit
            line.discount_amount = (line.price_before_discount * line.discount) / 100.0

    @api.depends('price_unit', 'quantity', 'price_subtotal', 'price_total')
    def _compute_tax_amount(self):
        for line in self:
            line.tax_amount = line.price_total - line.price_subtotal
