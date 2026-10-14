from odoo import api, models


class ReportAttendanceSummary(models.AbstractModel):
    # Name must be: report.<module>.<report_name>
    _name = 'report.attendance_tracker.report_attendance_summary'
    _description = 'Attendance Summary Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['attendance.record'].browse(docids).sorted(
            key=lambda r: (r.employee_id.name or '', r.date))
        summary = []
        for employee in docs.mapped('employee_id'):
            lines = docs.filtered(lambda r: r.employee_id == employee)
            summary.append({
                'employee': employee,
                'days': len(lines),
                'hours': sum(lines.mapped('worked_hours')),
            })
        summary.sort(key=lambda s: s['hours'], reverse=True)  # ranked
        dates = docs.mapped('date')
        return {
            'doc_ids': docids,
            'doc_model': 'attendance.record',
            'docs': docs,
            'summary': summary,
            'date_from': min(dates) if dates else False,
            'date_to': max(dates) if dates else False,
            'total_hours': sum(docs.mapped('worked_hours')),
        }
