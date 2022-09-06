import datetime
from collections import defaultdict
from markupsafe import Markup
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero, plaintext2html
import logging
_logger = logging.getLogger(__name__)


class SalaryRulesInherit(models.Model):
    _inherit = 'hr.salary.rule'

    journal = fields.Boolean('New Journal')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal')


class HrPayslipLineInherit(models.Model):
    _inherit = 'hr.payslip.line'

    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal')


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    move_ids = fields.One2many(
        comodel_name='account.move', inverse_name='payslip_id', string='Moves')

    def compute_sheet(self):
        res = super(HrPayslipInherit, self).compute_sheet()
        for line in self.line_ids:
            if line.salary_rule_id.journal:
                line.write({'journal_id': line.salary_rule_id.journal_id})
        return res

    def action_payslip_done(self):
        res = super(HrPayslipInherit, self).action_payslip_done()

        date = fields.date.today()

        # if self.contract_id.is_vacation:
        #     line_ids = []
        #     journal = int(self.env['ir.config_parameter'].sudo().get_param('vacation_journal_id'))
        #     if self.employee_id.type_of_employee == 'employee':
        #         debit_account = int(
        #             self.env['ir.config_parameter'].sudo().get_param('vacation_debit_account'))
        #         credit_account = int(
        #             self.env['ir.config_parameter'].sudo().get_param('vacation_credit_account'))
        #     elif self.employee_id.type_of_employee == 'operator':
        #         credit_account = int(self.env['ir.config_parameter'].sudo().get_param('vacation_credit_pjt_account'))
        #         debit_account = int(self.env['ir.config_parameter'].sudo().get_param('vacation_debit_pjt_account'))
        #     else:
        #         raise ValidationError('Please go to employee and put type of employee')
        #     amount = (self.contract_id.vacation / 365) * self.month_days
        #     if not journal:
        #         raise ValidationError(_('Please go to config and put (Vacation journal)'))
        #
        #     move = {
        #         'name': '/',
        #         'journal_id': journal,
        #         'date': self.date_to,
        #         'employee_id': self.employee_id.id,
        #         'payslip_id': self.id
        #     }
        #     adjust_credit = (0, 0, {
        #         'name': 'Vacation Accrual',
        #         'partner_id': self.employee_id.address_home_id.id,
        #         'account_id': credit_account,
        #         'journal_id': journal,
        #         'date': self.date_to,
        #         'credit': amount,
        #         'debit': 0.0,
        #     })
        #     line_ids.append(adjust_credit)
        #
        #     adjust_debit = (0, 0, {
        #         'name': 'Vacation Accrual',
        #         'partner_id': self.employee_id.address_home_id.id,
        #         'account_id': debit_account,
        #         'journal_id': journal,
        #         'date': self.date_to,
        #         'debit': abs(amount),
        #         'credit': 0.0,
        #     })
        #     line_ids.append(adjust_debit)
        #     move['line_ids'] = line_ids
        #     move_id = self.env['account.move'].create(move)
        #     accrual = {
        #         'move_id': move_id.id,
        #         'employee_id': self.employee_id.id,
        #         'date_from': self.date_from,
        #         'date_to': self.date_to,
        #         'type': 'vacation',
        #     }
        #     self.env['employee.accrual.move'].sudo().create(accrual)

        for line in self.line_ids:
            ids = []
            if line.journal_id:
                debit_dic = {
                    'name': line.name + '-' + self.employee_id.name + '-' + self.name,
                    'partner_id': False,
                    'account_id': line.salary_rule_id.account_debit.id,
                    'journal_id': line.journal_id.id,
                    'date': date,
                    'debit': abs(line.total),
                    'credit': 0.0
                }
                ids.append((0, 0, debit_dic))
                credit_dic = {
                    'name': line.name + '-' + self.employee_id.name + '-' + self.name,
                    'partner_id': False,
                    'account_id': line.salary_rule_id.account_credit.id,
                    'journal_id': line.journal_id.id,
                    'date': date,
                    'debit': 0.0,
                    'credit': abs(line.total)
                }
                ids.append((0, 0, credit_dic))
                # ids.append(credit_dic)
                move = self.env['account.move'].sudo().create({
                    'name': '/',
                    'payslip_id': self.id,
                    'move_type': 'entry',
                    'ref': self.employee_id.name,
                    'journal_id': line.journal_id.id,
                    'date': date,
                    'line_ids': ids
                })

            # self.gosi_move_id = move.id
        return res



        # precision = self.env['decimal.precision'].precision_get('Payroll')
        #
        # # Add payslip without run
        # payslips_to_post = self.filtered(lambda slip: not slip.payslip_run_id)
        #
        # # Adding pay slips from a batch and deleting pay slips with a batch that is not ready for validation.
        # payslip_runs = (self - payslips_to_post).mapped('payslip_run_id')
        # for run in payslip_runs:
        #     if run._are_payslips_ready():
        #         payslips_to_post |= run.slip_ids
        #
        # # A payslip need to have a done state and not an accounting move.
        # payslips_to_post = payslips_to_post.filtered(lambda slip: slip.state == 'done' and not slip.move_id)
        #
        # # Check that a journal exists on all the structures
        # if any(not payslip.struct_id for payslip in payslips_to_post):
        #     raise ValidationError(_('One of the contract for these payslips has no structure type.'))
        # if any(not structure.journal_id for structure in payslips_to_post.mapped('struct_id')):
        #     raise ValidationError(_('One of the payroll structures has no account journal defined on it.'))
        #
        # # Map all payslips by structure journal and pay slips month.
        # # {'journal_id': {'month': [slip_ids]}}
        # slip_mapped_data = defaultdict(lambda: defaultdict(lambda: self.env['hr.payslip']))
        #
        # for slip in payslips_to_post:
        #     slip_mapped_data[slip.struct_id.journal_id.id][fields.Date().end_of(slip.date_to, 'month')] |= slip
        # for journal_id in slip_mapped_data:  # For each journal_id.
        #     for slip_date in slip_mapped_data[journal_id]:  # For each month.
        #         line_ids = []
        #         debit_sum = 0.0
        #         credit_sum = 0.0
        #         date = slip_date
        #         move_dict = {
        #             'narration': '',
        #             'ref': date.strftime('%B %Y'),
        #             'journal_id': journal_id,
        #             'date': date,
        #         }
        #
        #         for slip in slip_mapped_data[journal_id][slip_date]:
        #             move_dict['narration'] += plaintext2html(slip.number or '' + ' - ' + slip.employee_id.name or '')
        #             move_dict['narration'] += Markup('<br/>')
        #             for line in slip.line_ids.filtered(lambda line: line.category_id):
        #
        #                 amount = line.total
        #                 if line.code == 'NET':  # Check if the line is the 'Net Salary'.
        #                     for tmp_line in slip.line_ids.filtered(lambda line: line.category_id):
        #                         if tmp_line.salary_rule_id.not_computed_in_net:  # Check if the rule must be computed in the 'Net Salary' or not.
        #                             if amount > 0:
        #                                 amount -= abs(tmp_line.total)
        #                             elif amount < 0:
        #                                 amount += abs(tmp_line.total)
        #                 if float_is_zero(amount, precision_digits=precision):
        #                     continue
        #                 debit_account_id = line.salary_rule_id.account_debit.id
        #                 credit_account_id = line.salary_rule_id.account_credit.id
        #
        #                 if debit_account_id:  # If the rule has a debit account.
        #                     debit = amount if amount > 0.0 else 0.0
        #                     credit = -amount if amount < 0.0 else 0.0
        #
        #                     debit_line = self._get_existing_lines(
        #                         line_ids, line, debit_account_id, debit, credit)
        #
        #                     if not debit_line:
        #                         debit_line = self._prepare_line_values(line, debit_account_id, date, debit, credit)
        #                         debit_line['tax_ids'] = [(4, tax_id) for tax_id in
        #                                                  line.salary_rule_id.account_debit.tax_ids.ids]
        #                         line_ids.append(debit_line)
        #                     else:
        #                         debit_line['debit'] += debit
        #                         debit_line['credit'] += credit
        #
        #                 if credit_account_id:  # If the rule has a credit account.
        #                     debit = -amount if amount < 0.0 else 0.0
        #                     credit = amount if amount > 0.0 else 0.0
        #                     credit_line = self._get_existing_lines(
        #                         line_ids, line, credit_account_id, debit, credit)
        #
        #                     if not credit_line:
        #                         credit_line = self._prepare_line_values(line, credit_account_id, date, debit, credit)
        #                         credit_line['tax_ids'] = [(4, tax_id) for tax_id in
        #                                                   line.salary_rule_id.account_credit.tax_ids.ids]
        #                         line_ids.append(credit_line)
        #                     else:
        #                         credit_line['debit'] += debit
        #                         credit_line['credit'] += credit
        #
        #         for line_id in line_ids:  # Get the debit and credit sum.
        #             debit_sum += line_id['debit']
        #             credit_sum += line_id['credit']
        #         # The code below is called if there is an error in the balance between credit and debit sum.
        #         acc_id = slip.sudo().journal_id.default_account_id.id
        #         if float_compare(credit_sum, debit_sum, precision_digits=precision) == -1:
        #             if not acc_id:
        #                 raise UserError(
        #                     _('The Expense Journal "%s" has not properly configured the Credit Account!') % (
        #                         slip.journal_id.name))
        #             existing_adjustment_line = (
        #                 line_id for line_id in line_ids if line_id['name'] == _('Adjustment Entry')
        #             )
        #             adjust_credit = next(existing_adjustment_line, False)
        #
        #             if not adjust_credit:
        #                 adjust_credit = {
        #                     'name': _('Adjustment Entry'),
        #                     'partner_id': False,
        #                     'account_id': acc_id,
        #                     'journal_id': slip.journal_id.id,
        #                     'date': date,
        #                     'debit': 0.0,
        #                     'credit': debit_sum - credit_sum,
        #                 }
        #                 line_ids.append(adjust_credit)
        #             else:
        #                 adjust_credit['credit'] = debit_sum - credit_sum
        #
        #         elif float_compare(debit_sum, credit_sum, precision_digits=precision) == -1:
        #             if not acc_id:
        #                 raise UserError(_('The Expense Journal "%s" has not properly configured the Debit Account!') % (
        #                     slip.journal_id.name))
        #             existing_adjustment_line = (
        #                 line_id for line_id in line_ids if line_id['name'] == _('Adjustment Entry')
        #             )
        #             adjust_debit = next(existing_adjustment_line, False)
        #
        #             if not adjust_debit:
        #                 adjust_debit = {
        #                     'name': _('Adjustment Entry'),
        #                     'partner_id': False,
        #                     'account_id': acc_id,
        #                     'journal_id': slip.journal_id.id,
        #                     'date': date,
        #                     'debit': credit_sum - debit_sum,
        #                     'credit': 0.0,
        #                 }
        #                 line_ids.append(adjust_debit)
        #             else:
        #                 adjust_debit['debit'] = credit_sum - debit_sum
        #         # Add accounting lines in the move
        #         move_dict['line_ids'] = [(0, 0, line_vals) for line_vals in line_ids]
        #         move = self.env['account.move'].sudo().create(move_dict)
        #         for slip in slip_mapped_data[journal_id][slip_date]:
        #             slip.write({'move_id': move.id, 'date': date})
        return res

    def _action_create_account_move(self):
        precision = self.env['decimal.precision'].precision_get('Payroll')

        # Add payslip without run
        payslips_to_post = self.filtered(lambda slip: not slip.payslip_run_id)

        # Adding pay slips from a batch and deleting pay slips with a batch that is not ready for validation.
        payslip_runs = (self - payslips_to_post).mapped('payslip_run_id')
        for run in payslip_runs:
            if run._are_payslips_ready():
                payslips_to_post |= run.slip_ids

        # A payslip need to have a done state and not an accounting move.
        payslips_to_post = payslips_to_post.filtered(lambda slip: slip.state == 'done' and not slip.move_id)

        # Check that a journal exists on all the structures
        if any(not payslip.struct_id for payslip in payslips_to_post):
            raise ValidationError(_('One of the contract for these payslips has no structure type.'))
        if any(not structure.journal_id for structure in payslips_to_post.mapped('struct_id')):
            raise ValidationError(_('One of the payroll structures has no account journal defined on it.'))

        # Map all payslips by structure journal and pay slips month.
        # {'journal_id': {'month': [slip_ids]}}
        slip_mapped_data = defaultdict(lambda: defaultdict(lambda: self.env['hr.payslip']))

        for slip in payslips_to_post:
            slip_mapped_data[slip.struct_id.journal_id.id][fields.Date().end_of(slip.date_to, 'month')] |= slip
        for journal_id in slip_mapped_data: # For each journal_id.
            for slip_date in slip_mapped_data[journal_id]: # For each month.
                line_ids = []
                debit_sum = 0.0
                credit_sum = 0.0
                date = slip_date
                move_dict = {
                    'narration': '',
                    'ref': self.employee_id.name + str(date.strftime('%B %Y')),
                    'journal_id': journal_id,
                    'date': date,
                }

                for slip in slip_mapped_data[journal_id][slip_date]:
                    move_dict['narration'] += plaintext2html(slip.number or '' + ' - ' + slip.employee_id.name or '')
                    move_dict['narration'] += Markup('<br/>')
                    for line in slip.line_ids.filtered(lambda line: line.category_id):
                        if not line.journal_id:
                            amount = line.total
                            if line.code == 'NET': # Check if the line is the 'Net Salary'.
                                for tmp_line in slip.line_ids.filtered(lambda line: line.category_id):
                                    if tmp_line.salary_rule_id.not_computed_in_net: # Check if the rule must be computed in the 'Net Salary' or not.
                                        if amount > 0:
                                            amount -= abs(tmp_line.total)
                                        elif amount < 0:
                                            amount += abs(tmp_line.total)
                            if float_is_zero(amount, precision_digits=precision):
                                continue
                            debit_account_id = line.salary_rule_id.account_debit.id
                            credit_account_id = line.salary_rule_id.account_credit.id

                            if debit_account_id: # If the rule has a debit account.
                                debit = amount if amount > 0.0 else 0.0
                                credit = -amount if amount < 0.0 else 0.0

                                debit_line = self._get_existing_lines(
                                    line_ids, line, debit_account_id, debit, credit)

                                if not debit_line:
                                    debit_line = self._prepare_line_values(line, debit_account_id, date, debit, credit)
                                    debit_line['tax_ids'] = [(4, tax_id) for tax_id in line.salary_rule_id.account_debit.tax_ids.ids]
                                    line_ids.append(debit_line)
                                else:
                                    debit_line['debit'] += debit
                                    debit_line['credit'] += credit

                            if credit_account_id: # If the rule has a credit account.
                                debit = -amount if amount < 0.0 else 0.0
                                credit = amount if amount > 0.0 else 0.0
                                credit_line = self._get_existing_lines(
                                    line_ids, line, credit_account_id, debit, credit)

                                if not credit_line:
                                    credit_line = self._prepare_line_values(line, credit_account_id, date, debit, credit)
                                    credit_line['tax_ids'] = [(4, tax_id) for tax_id in line.salary_rule_id.account_credit.tax_ids.ids]
                                    line_ids.append(credit_line)
                                else:
                                    credit_line['debit'] += debit
                                    credit_line['credit'] += credit

                for line_id in line_ids: # Get the debit and credit sum.
                    debit_sum += line_id['debit']
                    credit_sum += line_id['credit']
                # The code below is called if there is an error in the balance between credit and debit sum.
                acc_id = slip.sudo().journal_id.default_account_id.id
                if float_compare(credit_sum, debit_sum, precision_digits=precision) == -1:
                    if not acc_id:
                        raise UserError(_('The Expense Journal "%s" has not properly configured the Credit Account!') % (slip.journal_id.name))
                    existing_adjustment_line = (
                        line_id for line_id in line_ids if line_id['name'] == _('Adjustment Entry')
                    )
                    adjust_credit = next(existing_adjustment_line, False)

                    if not adjust_credit:
                        adjust_credit = {
                            'name': _('Adjustment Entry'),
                            'partner_id': False,
                            'account_id': acc_id,
                            'journal_id': slip.journal_id.id,
                            'date': date,
                            'debit': 0.0,
                            'credit': debit_sum - credit_sum,
                        }
                        line_ids.append(adjust_credit)
                    else:
                        adjust_credit['credit'] = debit_sum - credit_sum

                elif float_compare(debit_sum, credit_sum, precision_digits=precision) == -1:
                    if not acc_id:
                        raise UserError(_('The Expense Journal "%s" has not properly configured the Debit Account!') % (slip.journal_id.name))
                    existing_adjustment_line = (
                        line_id for line_id in line_ids if line_id['name'] == _('Adjustment Entry')
                    )
                    adjust_debit = next(existing_adjustment_line, False)

                    if not adjust_debit:
                        adjust_debit = {
                            'name': _('Adjustment Entry'),
                            'partner_id': False,
                            'account_id': acc_id,
                            'journal_id': slip.journal_id.id,
                            'date': date,
                            'debit': credit_sum - debit_sum,
                            'credit': 0.0,
                        }
                        line_ids.append(adjust_debit)
                    else:
                        adjust_debit['debit'] = credit_sum - debit_sum

                # Add accounting lines in the move
                move_dict['line_ids'] = [(0, 0, line_vals) for line_vals in line_ids]
                move = self.env['account.move'].sudo().create(move_dict)
                for slip in slip_mapped_data[journal_id][slip_date]:
                    slip.write({'move_id': move.id, 'date': date})
        return True


class AccountMove(models.Model):
    _inherit = 'account.move'

    payslip_id = fields.Many2one('hr.payslip', 'Payslip')

