# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('waiting_for_approval', 'Waiting For Purchase Manager'),
        ('waiting_for_approval_finance', 'Waiting For Finance'),
        ('waiting_for_approval_ceo', 'Waiting For CEO'),
        ('ready_to_confirm', 'Ready to Confirm'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def submit_for_approval(self):
        for rec in self:
            rec.state = 'waiting_for_approval'

    def confirm_by_manager(self):
        for rec in self:
            rec.state = 'waiting_for_approval_finance'

    def confirm_by_finance(self):
        for rec in self:
            rec.state = 'waiting_for_approval_ceo'

    def confirm_by_ceo(self):
        for rec in self:
            rec.state = 'ready_to_confirm'

    def button_confirm_po(self):
        for order in self:
            if order.state not in ['ready_to_confirm', 'sent', ]:
                continue
            order._add_supplier_to_product()
            order.button_approve()
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True
