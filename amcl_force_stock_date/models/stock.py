# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _update_available_quantity(
            self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None, in_date=None
    ):
        res = super(StockQuant, self)._update_available_quantity(
            product_id, location_id, quantity, lot_id, package_id, owner_id, in_date
        )

        return res


class StockPicking(models.Model):
    _inherit = "stock.picking"

    forced_date = fields.Datetime('Forced Date')

    def action_force_date(self):
        self.write({"date": self.forced_date, "date_done": self.forced_date})
        # self.move_lines.write({"date": self.forced_date})  # 'date_expected': use_date,
        # self.move_line_ids.write({"date": self.forced_date})
        for line in self.move_lines:
            line.write({"date": self.forced_date, 'date_deadline': self.forced_date})
            line.move_line_ids.write({"date": self.forced_date})
            account_move = self.env['account.move'].search([('stock_move_id', '=', line.id)])
            for mv in account_move:
                mv.write({"date": self.forced_date})

                stock_layer = self.env['stock.valuation.layer'].search([('account_move_id', '=', mv.id)])
                for layer in stock_layer:

                    layer.write({"create_date": self.forced_date})
                    layer.stock_move_id.write({"date": self.forced_date})

                    self.env.cr.execute("UPDATE stock_move set date=%s WHERE id=%s", (self.forced_date, line.id))
                    self.env.cr.execute("UPDATE stock_valuation_layer set create_date=%s WHERE id=%s",
                                        (self.forced_date, layer.id))

        for line in self.move_line_ids:
            line.write({"date": self.forced_date})
