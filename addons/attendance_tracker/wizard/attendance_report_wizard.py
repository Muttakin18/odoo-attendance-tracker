from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AttendanceReportWizard(models.TransientModel):
    _name = 'attendance.report.wizard'
    _description = 'Attendance Summary Wizard'

    date_from = fields.Date(
        string='From', required=True,
        default=lambda self: fields.Date.context_today(self).replace(day=1))
    date_to = fields.Date(
        string='To', required=True, default=fields.Date.context_today)
    employee_ids = fields.Many2many(
        'hr.employee', string='Employees',
        help='Leave empty to include all employees.')

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for wiz in self:
            if wiz.date_from > wiz.date_to:
                raise ValidationError(_('"From" date must be before "To" date.'))

    def action_print_report(self):
        self.ensure_one()
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('state', '=', 'confirmed'),
        ]
        if self.employee_ids:
            domain.append(('employee_id', 'in', self.employee_ids.ids))
        records = self.env['attendance.record'].search(domain)
        if not records:
            raise UserError(_('No confirmed attendance records found for the '
                              'selected period.'))
        return self.env.ref(
            'attendance_tracker.action_report_attendance_summary'
        ).report_action(records)
