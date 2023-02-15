
{
    'name': 'Class Room Management',
    'summary': '''Class Room Management''',
    'version': '15.1.0.1.1',
    'application': False,
    "auto_install": False,
    'installable': True,
'category': 'Educational',
    'author': 'Mounika',
    "license" :  "Other proprietary",
    'images': ['static/description/icon.png'],
    'company': 'New Horizon Cyber Limited',
    'website': "https://www.nhclindia.com/",
    'depends': ['base','sale','stock','account','faculty_nhcl'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/configuration.xml',
        'views/class_room.xml',
    ],
    "external_dependencies": {"python": [], "bin": []},
}
