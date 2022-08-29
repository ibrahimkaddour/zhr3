# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Leave Custom",
    'summary': """ HR Leave""",
    'description': """ put condition if leave include weekend or not""",
    'author': 'Ibrhaim',
    'website': 'http://www.ahcec.com',
    'category': 'HR',
    'version': '1.0',
    'depends': ['hr', 'base', 'hr_holidays'],
    'data': [
        'views/hr_leave_type.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': False,
}
