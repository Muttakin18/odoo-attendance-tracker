# Odoo Attendance Tracker (Odoo 17)

A custom Odoo module to record employee attendance, validate it, secure it by role
and company, and print a PDF attendance summary.

## Features
- `attendance.record` model linked to `hr.employee`
- Auto reference (ATT/0001) via `ir.sequence`
- Computed worked hours (`@api.depends`), validation (`@api.constrains`, SQL unique constraint)
- Draft / Confirmed workflow with buttons and statusbar
- Form, list and search views, menus and actions
- Security: User and Manager groups, access rights, record rules, multi-company rule
- Wizard (date range + employees) and QWeb PDF report with per-employee summary
- Unit tests

## Run it
```bash
docker compose up -d
# open http://localhost:8069 -> create a database (tick "Demo data" if you like)
# Apps -> remove the "Apps" filter -> search "Attendance Tracker" -> Install
```

After changing Python code: `docker compose restart odoo`.
After changing XML: upgrade the module (Apps -> Attendance Tracker -> Upgrade) or run
`docker compose exec odoo odoo -d <db> -u attendance_tracker --stop-after-init --db_host=db --db_user=odoo --db_password=odoo`.

## Run tests
```bash
docker compose exec odoo odoo -d <test_db> -i attendance_tracker --test-enable --stop-after-init --db_host=db --db_user=odoo --db_password=odoo
```

## Odoo 18 note
Change `<tree>` to `<list>` in views and `view_mode` `tree,form` to `list,form`.

Author: Muttakin Mahmud
