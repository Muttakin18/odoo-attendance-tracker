{
    'name': 'Attendance Tracker',
    'version': '17.0.1.0.0',
    'summary': 'Record employee attendance and print an attendance summary report',
    'description': """
Attendance Tracker
==================
* Attendance records linked to HR employees
* Computed worked hours, validation, draft/confirmed workflow
* Security groups (User / Manager), record rules and multi-company support
* Wizard + QWeb PDF report (attendance summary by employee)
""",
    'category': 'Human Resources',
    'author': 'Muttakin Mahmud',
    'license': 'LGPL-3',
    'depends': ['base', 'hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/attendance_record_views.xml',
        'wizard/attendance_report_wizard_views.xml',
        'report/attendance_report.xml',
        'report/attendance_report_templates.xml',
        'views/menus.xml',
    ],
    'application': True,
    'installable': True,
}
