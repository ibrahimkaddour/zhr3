# -*- coding: utf-8 -*-
{
    'name': 'AMCL - Global Discount (Sales / Accounting / Purchase)',
    'category': 'Sales',
    'sequence': 1,
    'version': '15.0.1',
    'license': 'LGPL-3',
    'summary': """AMCL - Global Discount (Sales / Accounting / Purchase)""",
    'description': """AMCL - Global Discount (Sales / Accounting / Purchase)""",
    'author': 'Aneesh.AV',
    'depends': ['account', 'sale', 'sale_management', 'purchase'],
    'data': [
        'views/sale_view.xml',
        'views/invoice_view.xml',
        'views/purchase_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
