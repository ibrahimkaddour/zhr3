# -*- coding: utf-8 -*-


from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    purchase_order_approval_rule_id = fields.Many2one('purchase.order.approval.rule', related='company_id.purchase_order_approval_rule_id', string='Purchase Order Approval Rules', readonly=False)
    purchase_order_approval = fields.Boolean(related='company_id.purchase_order_approval', string='Purchase Order Approval By Rule', readonly=False)


class PurchaseOrderApprovalRule(models.Model):
    _name = 'purchase.order.approval.rule'
    _description = 'Purchase Order Approval Rule'

    name = fields.Char(required=True)
    approval_rule_ids = fields.One2many('purchase.order.approval.rule.lines', 'approval_rule_id', string='Approval Rule Lines')

    def update_old_po(self):
        for purchase in self.env['purchase.order'].search([('state','=','draft')]):
            values = purchase._get_data_purchase_order_approval_rule_ids()
            approval_roles = purchase.purchase_order_approval_rule_ids.mapped('approval_role')
            for v in values:
                if not v.get('approval_role') in approval_roles.ids:
                    self.env['purchase.order.approval.rules'].create(v)
            for a in purchase.purchase_order_approval_rule_ids:
                if a.approval_role.id not in map(lambda x: x['approval_role'], values):
                    a.unlink()
            purchase.user_ids = [(6, 0, purchase.purchase_order_approval_rule_ids.mapped('users').ids)]


class PurchaseOrderApprovalRuleLines(models.Model):
    _name = 'purchase.order.approval.rule.lines'
    _description = "Purchase Order Approval Rule Lines"

    approval_rule_id = fields.Many2one('purchase.order.approval.rule')
    sequence = fields.Integer(string='Sequence', required=True)
    approval_role = fields.Many2one('approval.role', string='Approval Role', required=True)
    approval_category = fields.Many2one('purchase.approval.category', string='Approval Category')
    user_ids = fields.Many2many('res.users', string='Users')
    email_template = fields.Many2one('mail.template', string='Mail Template')
    purchase_lower_limit = fields.Float(string="Lower Limit", required=True)
    purchase_upper_limit = fields.Float(string="Upper Limit", required=True)

    @api.onchange('approval_role')
    def onchange_approval_role(self):
        if self.approval_role and self.approval_role.user_ids:
            self.user_ids = [(5, 0, 0)]
            self.user_ids = [(6, 0, self.approval_role.user_ids.ids)]

    @api.constrains('purchase_upper_limit')
    def _constrains_reconcile(self):
        for record in self:
            if record.purchase_upper_limit <= record.purchase_lower_limit and record.purchase_upper_limit != -1:
                raise UserError(_('An Upper limit must be grater then lower limit'))