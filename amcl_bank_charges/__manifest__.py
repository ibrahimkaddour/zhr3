# -*- coding: utf-8 -*-
{
    'name': 'Bank Charges on Vendor Bill',
    'category': 'Account',
    'sequence': 5,
    'version': '15.0.1.0',
    'license': 'LGPL-3',
    'summary': """Bank Charges on Vendor Bill""",
    'description': """Bank Charges on Vendor Bill""",
    'author': 'Aneesh.AV',
    'depends': ['base', 'account'],
    'data': [
        'views/res_config_settings_view.xml',
        'views/payment_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
