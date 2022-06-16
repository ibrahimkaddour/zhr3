{
    'name': "Purchase Order Approval",
    'summary': """
        Purchase Order Approval
        """,
    'description': """
        Purchase Order Approval
        =========================
            Purchase Order Approval- Only users with particular group access will be able to approve the order.
        """,
    'author': "Aneesh.AV",
    'category': 'sale',
    'version': '1.0',
    'depends': ['base', 'purchase'],
    'data': [
        'data/mail_template.xml',
        'security/security.xml',
        'views/purchase_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
