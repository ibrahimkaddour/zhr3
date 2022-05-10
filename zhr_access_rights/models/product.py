# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hide_sales = fields.Boolean(string='Hide Sale Price', compute='set_hide_sales')
    hide_cost = fields.Boolean(string='Hide Sale Cost', compute='set_hide_cost')

    def set_hide_sales(self):
        if self.env.user.has_group('zhr_access_rights.group_hide_sale_price'):
            self.hide_sales = True
        else:
            self.hide_sales = False

    def set_hide_cost(self):
        if self.env.user.has_group('zhr_access_rights.group_hide_cost'):
            self.hide_cost = True
        else:
            self.hide_cost = False


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
