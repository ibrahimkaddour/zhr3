# -*- coding: utf-8 -*-
{
    'name': 'Employee - Petty Cash Customizations',
    'category': 'Account',
    'sequence': 5,
    'version': '15.0.1.0',
    'license': 'LGPL-3',
    'summary': """Employee - Petty Cash Customizations""",
    'description': """Employee - Petty Cash Customizations""",
    'author': 'Aneesh.AV',
    'depends': ['account','hr'],
    'data': [
        'views/invoice_view.xml',
        'views/journal_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
