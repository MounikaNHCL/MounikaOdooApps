{
    'name': 'Reporting App',
    'summary': 'Reporting ',
    'author': 'Mounika ',
    'company': '',
    'maintainer': '',
    'website': "",
    'category': 'Employee',
    'version': '16.1.0.1.1',
    'depends': ['base','hr','project'],
    'data': [
        'security/ir.model.access.csv',
        'security/security_groups.xml',
        'views/report_view.xml',
        'views/config.xml',
        'reports/report.xml',
        'reports/reporting.xml',
   ],
    'qweb': [
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
