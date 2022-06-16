# -*- coding:utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _default_petty_cash_journal(self):
        company_id = self.env.company.id
        return self.env['account.journal'].search([
            ('company_id', '=', company_id),
            ('is_a_petty_cash', '=', True),
        ], limit=1)

    employee_id = fields.Many2one('hr.employee', 'Employee Petty Cash')
    petty_cash_journal_id = fields.Many2one('account.journal', string='Petty Cash Journal',
                                            default=_default_petty_cash_journal,
                                            domain="[('type', '=', 'general'),('is_a_petty_cash', '=', True)]")
    cash_payment_id = fields.Many2one('account.move', 'Cash Payment Move')


    @api.onchange('employee_id')
    def onchange_employee_id(self):
        petty_cash_journal_id = self.env['account.journal'].search([
                                ('company_id', '=', self.env.company.id),
                                ('is_a_petty_cash', '=', True),
                            ])
        self.write({'petty_cash_journal_id': petty_cash_journal_id.id or False})

    def action_post(self):
        res = super(AccountMove, self).action_post()
        if self.move_type == 'in_invoice' and self.employee_id and self.petty_cash_journal_id:
            if not self.employee_id.address_home_id:
                raise ValidationError("Please add the Employee Address.")
            cash_journal = self.env['account.move'].create({
                'move_type': 'entry',
                'date': fields.Date.today(),
                'journal_id': self.petty_cash_journal_id.id,
                'ref': self.name,
                'line_ids': [
                    (0, 0, {
                        'name': 'Cash Payment',
                        'debit': self.amount_total,
                        'credit': 0.0,
                        'quantity': 1.0,
                        'currency_id': self.currency_id.id,
                        'account_id': self.partner_id.property_account_payable_id.id,
                        'partner_id': self.commercial_partner_id.id,
                    }),
                    (0, 0, {
                        'name': 'Cash Payment',
                        'credit': self.amount_total,
                        'debit': 0.0,
                        'quantity': 1.0,
                        'currency_id': self.currency_id.id,
                        'account_id': self.petty_cash_journal_id.default_account_id.id,
                        'partner_id': self.employee_id.address_home_id.id
                    }),
                ],
            })
            self.cash_payment_id = cash_journal.id
            self.cash_payment_id._post()
            (self + self.cash_payment_id).line_ids \
                .filtered(lambda line: line.account_internal_type == 'payable') \
                .reconcile()

        return res
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
