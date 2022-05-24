# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits='BOM Quantity', required=True)
