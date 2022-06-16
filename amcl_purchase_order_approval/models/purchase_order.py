# -*- coding: utf-8 -*-

from odoo import models, fields, api
from werkzeug.urls import url_encode

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
    next_apporoval_user_ids = fields.Many2many('res.users', string='Next Approvals')

    def submit_for_approval(self):
        for rec in self:
            self.next_apporoval_user_ids = self.env.ref('amcl_purchase_order_approval.group_purchase_order_approval').users
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('purchase.purchase_rfq', raise_if_not_found=False)
            link = """{}/web#id={}&view_type=form&model=purchase.order&action={}""".format(web_base_url,
                                                                                            self.id,
                                                                                            action_id.id)

            # send mail template to users having email address
            template_ctx = {'action_url': link}
            template_id = self.env.ref('amcl_purchase_order_approval.email_template_po_approval_request')
            all_emails = {user.email for user in self.next_apporoval_user_ids}
            email_values = {
                'email_to': ','.join(all_emails)
            }
            template_id.with_context(**template_ctx).send_mail(rec.id, force_send=True, email_values=email_values)
            rec.state = 'waiting_for_approval'

    def confirm_by_manager(self):
        for rec in self:
            self.next_apporoval_user_ids = self.env.ref('amcl_purchase_order_approval.group_purchase_order_finance').users
            template_id = self.env.ref('amcl_purchase_order_approval.email_template_finance_approval_request')

            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('purchase.purchase_rfq', raise_if_not_found=False)
            link = """{}/web#id={}&view_type=form&model=purchase.order&action={}""".format(web_base_url,
                                                                                           self.id,
                                                                                           action_id.id)
            template_ctx = {'action_url': link}
            all_emails = {user.email for user in self.next_apporoval_user_ids}
            email_values = {
                'email_to': ','.join(all_emails)
            }
            template_id.with_context(**template_ctx).send_mail(rec.id, force_send=True, email_values=email_values)
            rec.state = 'waiting_for_approval_finance'

    def confirm_by_finance(self):
        for rec in self:
            self.next_apporoval_user_ids = self.env.ref('amcl_purchase_order_approval.group_purchase_order_ceo').users
            template_id = self.env.ref('amcl_purchase_order_approval.email_template_po_approval_ceo')

            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('purchase.purchase_rfq', raise_if_not_found=False)
            link = """{}/web#id={}&view_type=form&model=purchase.order&action={}""".format(web_base_url,
                                                                                           self.id,
                                                                                           action_id.id)
            template_ctx = {'action_url': link}

            all_emails = {user.email for user in self.next_apporoval_user_ids}
            email_values = {
                'email_to': ','.join(all_emails)
            }
            template_id.with_context(**template_ctx).send_mail(rec.id, force_send=True, email_values=email_values)
            rec.state = 'waiting_for_approval_ceo'

    def confirm_by_ceo(self):
        for rec in self:
            template_id = self.env.ref('amcl_purchase_order_approval.email_template_po_approved')
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('purchase.purchase_rfq', raise_if_not_found=False)
            link = """{}/web#id={}&view_type=form&model=purchase.order&action={}""".format(web_base_url,
                                                                                           self.id,
                                                                                           action_id.id)
            template_ctx = {'action_url': link}
            template_id.with_context(**template_ctx).send_mail(rec.id, force_send=True)
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
