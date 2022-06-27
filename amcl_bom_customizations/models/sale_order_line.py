# -*- coding:utf-8 -*-
from odoo.tools import float_compare
from odoo import fields, models, api
from odoo.tools import float_round


class Sale(models.Model):
    _inherit = 'sale.order.line'

    bom_id = fields.Many2one('mrp.bom', string='BOM', copy=False)
    label = fields.Char(string='Label', copy=False)
    drawing = fields.Char(string='Drawing', copy=False)
    non_standard_bom = fields.Boolean(related='product_id.non_standard_bom', string='Non Standard BOM')

    @api.onchange('product_id')
    def onchange_product_set_bom(self):
        if self.product_id.standard_bom:
            bom = self.env['mrp.bom']._bom_find(self.product_id, company_id=self.company_id.id, bom_type='normal')[
                self.product_id]
            if bom:
                self.bom_id = bom.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
