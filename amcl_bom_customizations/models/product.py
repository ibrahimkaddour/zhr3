# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    standard_bom = fields.Boolean('Having Standard BOM', default=False)
    non_standard_bom = fields.Boolean('Not having Standard BOM', default=False)

    @api.onchange('standard_bom')
    def _onchange_standard_bom(self):
        if self.standard_bom:
            self.non_standard_bom = False

    @api.onchange('non_standard_bom')
    def _onchange_non_standard_bom(self):
        if self.non_standard_bom:
            self.standard_bom = False
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
