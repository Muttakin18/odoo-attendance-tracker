from datetime import datetime

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestAttendance(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env['hr.employee'].create({'name': 'Test Employee'})

    def _make(self, check_in, check_out, date='2026-01-10'):
        return self.env['attendance.record'].create({
            'employee_id': self.employee.id,
            'date': date,
            'check_in': check_in,
            'check_out': check_out,
        })

    def test_worked_hours_computed(self):
        rec = self._make(datetime(2026, 1, 10, 9, 0), datetime(2026, 1, 10, 17, 30))
        self.assertAlmostEqual(rec.worked_hours, 8.5)

    def test_checkout_before_checkin_fails(self):
        with self.assertRaises(ValidationError):
            self._make(datetime(2026, 1, 10, 17, 0), datetime(2026, 1, 10, 9, 0))

    def test_reference_sequence(self):
        rec = self._make(datetime(2026, 1, 10, 9, 0), datetime(2026, 1, 10, 17, 0))
        self.assertTrue(rec.name.startswith('ATT/'))
