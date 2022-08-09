from odoo import fields, api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    user_approve_id = fields.Many2one('res.users', 'User Approval')

    def action_confirm(self):
        res = super(PurchaseOrder, self).action_confirm()
        self.write({'user_approve_id': self.env.user.id})
        return res
