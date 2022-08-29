from odoo import fields, api, models


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    include_weekend = fields.Boolean(default=False, string='Include WeekEnd')


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.depends('date_from', 'date_to', 'employee_id')
    def _compute_number_of_days(self):
        for holiday in self:
            if not holiday.holiday_status_id.include_weekend:
                if holiday.date_from and holiday.date_to:
                    holiday.number_of_days = \
                        holiday._get_number_of_days(holiday.date_from, holiday.date_to, holiday.employee_id.id)['days']
                else:
                    holiday.number_of_days = 0
            else:
                if holiday.date_from and holiday.date_to:
                    holiday.number_of_days = \
                        (holiday.date_to - holiday.date_from).days + 1
                else:
                    holiday.number_of_days = 0
