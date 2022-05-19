# -*- coding:utf-8 -*-
from odoo.tools import float_compare
from odoo import fields, models, api
from odoo.tools import float_round


class Sale(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        for line in self:
            price_before_discount = line.product_uom_qty * line.price_unit
            discount_amount = (price_before_discount * line.discount) / 100.0
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)

            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id,
                                  partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                'price_before_discount': price_before_discount,
                'discount_amount': discount_amount,
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    discount = fields.Float(string='Discount (%)', digits=(16, 20), default=0.0)
    discount_amount = fields.Float('Discount Amount', compute='_compute_amount', store=True)
    price_before_discount = fields.Monetary('Price B/f Disc', compute='_compute_amount', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
