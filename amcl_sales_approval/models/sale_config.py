# -*- coding: utf-8 -*-


from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_order_approval_rule_id = fields.Many2one('sale.order.approval.rule', related='company_id.sale_order_approval_rule_id', string='Sale Order Approval Rules', readonly=False)
    sale_order_approval = fields.Boolean(related='company_id.sale_order_approval', string='Sale Order Approval By Rule', readonly=False)


class SaleOrderApprovalRule(models.Model):
    _name = 'sale.order.approval.rule'
    _description = 'Sale Order Approval Rule'

    name = fields.Char(required=True)
    approval_rule_ids = fields.One2many('sale.order.approval.rule.lines', 'approval_rule_id', string='Approval Rule Lines')

    def update_old_so(self):
        for sale in self.env['sale.order'].search([('state','=','draft')]):
            print('Sale :: ', sale)
            values = sale._get_data_sale_order_approval_rule_ids()
            print('Values :: ', values)
            approval_roles = sale.sale_order_approval_rule_ids.mapped('approval_role')
            for v in values:
                if not v.get('approval_role') in approval_roles.ids:
                    self.env['sale.order.approval.rules'].create(v)
            for a in sale.sale_order_approval_rule_ids:
                if a.approval_role.id not in map(lambda x: x['approval_role'], values):
                    a.unlink()
            sale.user_ids = [(6, 0, sale.sale_order_approval_rule_ids.mapped('users').ids)]

class SaleOrderApprovalRuleLines(models.Model):
    _name = 'sale.order.approval.rule.lines'
    _description = "Sale Order Approval Rule Lines"

    approval_rule_id = fields.Many2one('sale.order.approval.rule')
    sequence = fields.Integer(string='Sequence', required=True)
    approval_role = fields.Many2one('sale.approval.role', string='Approval Role', required=True)
    sale_approval_category = fields.Many2one('sale.approval.category', string='Approval Category')
    user_ids = fields.Many2many('res.users', string='Users')
    email_template = fields.Many2one('mail.template', string='Mail Template')
    sale_lower_limit = fields.Float(string="Lower Limit", required=True)
    sale_upper_limit = fields.Float(string="Upper Limit", required=True)

    @api.onchange('approval_role')
    def onchange_approval_role(self):
        if self.approval_role and self.approval_role.user_ids:
            self.user_ids = [(5, 0, 0)]
            self.user_ids = [(6, 0, self.approval_role.user_ids.ids)]

    @api.constrains('sale_upper_limit')
    def _constrains_reconcile(self):
        for record in self:
            if record.sale_upper_limit <= record.sale_lower_limit and record.sale_upper_limit != -1:
                raise UserError(_('An Upper limit must be grater then lower limit'))
