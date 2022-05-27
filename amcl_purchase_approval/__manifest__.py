# -*- coding: utf-8 -*-


{
    "name": "Purchase Approval Rules",
    'summary': 'Purchase order approval rules',
    "version": "15.0.1.0",
    "category": "Inventory/Purchase",
    "license": "OPL-1",
    "summary": "Purchase Approval Rules",
    "description": "Purchase Approval Rules",
    "author": "Aneesh.AV",
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "views/approval_config.xml",
        "views/purchase_order_config.xml",
        "views/purchase_view.xml",
        "wizard/custom_warning_view.xml"
    ],
    'sequence': 1,
    "installable": True,

}
