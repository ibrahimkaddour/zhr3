# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class AccountMove(models.Model):
    _inherit = "account.move"

    name = fields.Char(string='Number', required=True, readonly=False, copy=False, default='/')

    def _get_sequence(self):
        self.ensure_one()
        journal = self.journal_id
        if self.move_type in ('entry', 'out_invoice', 'in_invoice', 'out_receipt', 'in_receipt') or not journal.refund_sequence:
            return journal.sequence_id
        if not journal.refund_sequence_id:
            return
        return journal.refund_sequence_id

    def _post(self, soft=True):
        for move in self:
            if move.name == '/':
                sequence = move._get_sequence()
                if not sequence:
                    raise UserError(_('Please define a sequence on your journal.'))
                move.name = sequence.with_context(ir_sequence_date=move.date).next_by_id()
                if move.journal_id.month_wise and move.journal_id.sequence_id.month_wise:
                    if not move.invoice_date:
                        raise ValidationError('Please add the Invoice Date')
                    prefix = str(move.journal_id.sequence_id.prefix).split('/')
                    if "%(range_month)s" in prefix:
                        index = prefix.index('%(range_month)s')
                        x = move.name.split('/')
                        x[index] = str(move.invoice_date.month).zfill(2)
                        move.name = '/'.join(x)
        res = super(AccountMove, self)._post(soft=True)
        return res

    @api.onchange('journal_id')
    def onchange_journal_id(self):
        self.name = '/'

    def _constrains_date_sequence(self):
        return

    @api.ondelete(at_uninstall=False)
    def _unlink_forbid_parts_of_chain(self):
        """ Moves with a sequence number can only be deleted if they are the last element of a chain of sequence.
        If they are not, deleting them would create a gap. If the user really wants to do this, he still can
        explicitly empty the 'name' field of the move; but we discourage that practice.
        """
        if (not self.journal_id.sequence_id or not self.journal_id.refund_sequence_id) and not self._context.get('force_delete') and not self.filtered(
                lambda move: move.name != '/')._is_end_of_seq_chain():
            raise UserError(
                _("You cannot delete this entry, as it has already consumed a sequence number and is not the last one in the chain. Probably you should revert it instead."))


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    month_wise = fields.Boolean('Month Wise')