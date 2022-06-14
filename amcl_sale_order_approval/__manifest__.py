{
    'name': "Sale Order Approval",
    'summary': """
        Sale Order Approval
        """,
    'description': """
        Sale Order Approval
        =========================
            Sale Order Approval- Only users with particular group access will be able to approve the order.
        """,
    'author': "Aneesh.AV",
    'category': 'sale',
    'version': '1.0',
    'depends': ['base', 'sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
