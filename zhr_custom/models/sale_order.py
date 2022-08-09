from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_period = fields.Char('Delivery Period')
    customer_po_text = fields.Char('Customer Po')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.picking_ids.write({'customer_po_text': self.customer_po_text})
        return res


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    customer_po_text = fields.Char('Customer Po')
