from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_group_id = fields.Many2one(comodel_name='product.group', string='Group')
