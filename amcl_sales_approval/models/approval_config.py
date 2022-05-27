# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleApprovalRole(models.Model):
    _name = 'sale.approval.role'
    _description = 'Sale Approval Role'

    name = fields.Char(required=True)
    user_ids = fields.Many2many('res.users', string='Role Users')




class SaleApprovalCategory(models.Model):
    _name = 'sale.approval.category'
    _description = 'Sale Approval Category'

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_approval_category = fields.Many2one('sale.approval.category', string='Sale Approval Category')
