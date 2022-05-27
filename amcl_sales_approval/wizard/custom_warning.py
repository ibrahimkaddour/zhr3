# -*- coding: utf-8 -*-


from odoo import models, _


class SaleCustomWarning(models.TransientModel):
    _name = 'sale.custom.warning'
    _description = 'Custom Warning'

    def action_continue(self):
        active_id = self.env.context.get('active_id')
        if active_id and self.env.context.get('sale_order'):
            sale_order = self.env['sale.order'].browse(active_id)
            if sale_order.sale_order_approval_rule_ids:
                sale_order.message_subscribe(
                    partner_ids=sale_order.sale_order_approval_rule_ids.mapped(
                        'users.partner_id.id'))
                msg = _("Quotation is waiting for approval.")
                sale_order.message_post(body=msg, subtype='mail.mt_comment')
            sale_order.write({'send_for_approval': True})
        return True
