# Copyright 2016-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Task Customization",
    "summary": "Project Task Customization",
    "version": "16",
    "category": "Project",
    "author": "Mounika",
    "installable": True,
    "auto_install": False,
    "depends": ["base", "project","web","mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/sales_team_security.xml",
        "views/project.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'project_c_click_task/static/src/js/mail_template.xml',
            # 'project_c_click_task/static/src/js/mail.js',
        ]}
}
