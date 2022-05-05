# -*- coding: utf-8 -*-

from odoo import fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"
    _order = "date, id"

    date = fields.Datetime(related="stock_move_id.date", store=True, string="Move Date")
