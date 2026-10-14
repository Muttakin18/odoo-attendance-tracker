from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AttendanceRecord(models.Model):
    _name = 'attendance.record'
    _description = 'Attendance Record'
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True, index=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.context_today)
    check_in = fields.Datetime(string='Check-in')
    check_out = fields.Datetime(string='Check-out')
    worked_hours = fields.Float(string='Worked Hours',
                                compute='_compute_worked_hours', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed')],
        string='Status', default='draft', required=True, copy=False)
    note = fields.Text(string='Notes')

    _sql_constraints = [
        ('employee_date_uniq', 'unique(employee_id, date)',
         'This employee already has an attendance record for that date.'),
    ]

    # ---------- ORM overrides ----------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'attendance.record') or 'New'
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_confirmed(self):
        if any(rec.state == 'confirmed' for rec in self):
            raise UserError(_('You cannot delete a confirmed attendance record. '
                              'Reset it to draft first.'))

    # ---------- Computed fields ----------
    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                delta = rec.check_out - rec.check_in
                rec.worked_hours = delta.total_seconds() / 3600.0
            else:
                rec.worked_hours = 0.0

    # ---------- Validation ----------
    @api.constrains('check_in', 'check_out')
    def _check_times(self):
        for rec in self:
            if rec.check_in and rec.check_out and rec.check_out <= rec.check_in:
                raise ValidationError(_('Check-out must be later than check-in.'))

    @api.onchange('check_in')
    def _onchange_check_in(self):
        if self.check_in:
            self.date = fields.Date.context_today(self, self.check_in)

    # ---------- Button actions ----------
    def action_confirm(self):
        for rec in self:
            if not rec.check_in or not rec.check_out:
                raise UserError(_('Please set both check-in and check-out '
                                  'before confirming.'))
        self.write({'state': 'confirmed'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})
