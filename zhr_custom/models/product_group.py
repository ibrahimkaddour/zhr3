from odoo import fields, models


class ProductGroup(models.Model):
    _name = 'product.group'

    name = fields.Char('Group Name')
    description = fields.Text('Description')
