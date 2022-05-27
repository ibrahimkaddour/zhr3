# -*- coding: utf-8 -*-

from odoo import fields, models


class ApprovalRole(models.Model):
    _name = 'approval.role'
    _description = 'Approval Role'

    name = fields.Char(required=True)
    user_ids = fields.Many2many('res.users', string='Role Users')

class ApprovalCategory(models.Model):
    _name = 'purchase.approval.category'
    _description = 'Approval Category'

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)

# class HrEmployee(models.Model):
#     _inherit = 'hr.employee'
#
#     approval_role = fields.Many2many('approval.role', 'approval_role_hr_employee_rel', 'approval_role_id', 'hr_employee_id', string='Approval Role')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    approval_category = fields.Many2one('purchase.approval.category', string='Approval Category')
