# -*- coding: utf-8 -*-


{
    "name": "Sale Approval Rules",
    'summary': 'Sale order approval rules',
    "version": "15.0.1.0",
    "category": "Sales",
    "license": "OPL-1",
    "summary": "Sale Approval Rules",
    "description": "Sale Approval Rules",
    "author": "Aneesh.AV",
    "depends": ["sale_management","base"],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "views/approval_config.xml",
        "views/sale_order_config.xml",
        "views/sale_view.xml",
        "wizard/custom_warning_view.xml"
    ],
    'sequence': 1,
    "installable": True,
}
