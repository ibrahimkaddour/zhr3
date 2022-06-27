# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_po = fields.Binary(tracking=True, string='Customer P.O')
    customer_po_filename = fields.Char(tracking=True)
    next_apporoval_user_ids =  fields.Many2many('res.users', string='Next Approvals')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('waiting_for_approval', 'Waiting For Manager'),
        ('waiting_for_approval_ceo', 'Waiting For CEO'),
        ('ready_to_confirm', 'Ready to Confirm'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def _creation_subtype(self):
        # OVERRIDE
        if self.state == 'draft':
            return self.env.ref('amcl_sale_order_approval.mt_quotation_created')
        else:
            return super(SaleOrder, self)._creation_subtype()

    def submit_for_approval(self):
        for rec in self:
            self.next_apporoval_user_ids = self.env.ref('amcl_sale_order_approval.group_sale_order_approval').users
            template_id = self.env.ref('amcl_sale_order_approval.email_template_quotation_approval_request')

            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('sale.view_order_form', raise_if_not_found=False)
            link = """{}/web#id={}&view_type=form&model=sale.order&action={}""".format(web_base_url,
                                                                                           self.id,
                                                                                           action_id.id)
            template_ctx = {'action_url': link}


            all_emails = {user.email for user in self.next_apporoval_user_ids}
            email_values = {
                'email_to': ','.join(all_emails)
            }
            template_id.with_context(**template_ctx).send_mail(rec.id, force_send=True,email_values=email_values)
            rec.state = 'waiting_for_approval'

    def confirm_by_manager(self):
        for rec in self:
            self.next_apporoval_user_ids = self.env.ref('amcl_sale_order_approval.group_sale_order_ceo').users
            template_id = self.env.ref('amcl_sale_order_approval.email_template_quotation_approval_ceo')
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('sale.view_order_form', raise_if_not_found=False)
            link = """{}/web#id={}&view_type=form&model=sale.order&action={}""".format(web_base_url,
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
            template_id = self.env.ref('amcl_sale_order_approval.email_template_quotation_approval_ceo')
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('sale.view_order_form', raise_if_not_found=False)
            link = """{}/web#id={}&view_type=form&model=sale.order&action={}""".format(web_base_url,
                                                                                       self.id,
                                                                                       action_id.id)
            template_ctx = {'action_url': link}

            template_id.with_context(**template_ctx).send_mail(rec.id, force_send=True)
            rec.state = 'ready_to_confirm'

    def approve_sale_order(self):
        # for rec in self:
        # rec.action_confirm()
        # rec.state = 'sale'
        res = super(SaleOrder, self).action_confirm()
        return res

    def action_print(self):
        return self.env.ref('sale.action_report_saleorder').report_action(self)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)
        if self._context.get('params'):
            if res.get('toolbar', False) and res.get('toolbar').get('print', False):
                reports = res.get('toolbar').get('print')
                for report in reports:
                    res['toolbar']['print'].remove(report)
        return res

