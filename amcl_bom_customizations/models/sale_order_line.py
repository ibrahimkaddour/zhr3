# -*- coding:utf-8 -*-
from odoo.tools import float_compare
from odoo import fields, models, api
from odoo.tools import float_round


class Sale(models.Model):
    _inherit = 'sale.order.line'

    bom_id = fields.Many2one('mrp.bom', string='BOM', copy=False)
    label = fields.Char(string='Label', copy=False)
    drawing = fields.Char(string='Drawing', copy=False)
    standard_bom = fields.Boolean(related='product_id.standard_bom', string='Standard BOM')
    non_standard_bom = fields.Boolean(related='product_id.non_standard_bom', string='Non Standard BOM')

    @api.onchange('product_id','standard_bom')
    def onchange_product_set_bom(self):
        if self.product_id.standard_bom:
            bom = self.env['mrp.bom']._bom_find(self.product_id, company_id=self.company_id.id, bom_type='normal')[
                self.product_id]
            if bom:
                self.bom_id = bom.id

    def on_standard_bom(self):
        if self.product_id:
            self.product_id.write({'standard_bom': True, 'non_standard_bom': False})
            self.onchange_product_set_bom()

    def on_non_standard_bom(self):
        if self.product_id:
            self.product_id.write({'standard_bom': False, 'non_standard_bom': True})
            self.onchange_product_set_bom()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
