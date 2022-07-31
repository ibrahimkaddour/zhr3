# -*- coding: utf-8 -*-
{
    'name': 'ZHR Custom',
    'category': 'Custom',
    'sequence': 1,
    'version': '15.0.1',
    'license': 'LGPL-3',
    'summary': """ZHR Custom""",
    'description': "",
    'author': 'Ibrahim.Kaddour',
    'depends': ['product', 'stock', 'sale', 'mrp'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/product_group.xml',
        'views/product_inherit.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',
        'reports/inherit_template.xml',
        'data/service.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
