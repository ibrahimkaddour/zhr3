# -*- coding: utf-8 -*-

{
    'name': 'AHCEC HR Travel Request',
    'version': '1.0',
    'category': 'human resource',
    'description': """
        Its request for traveling for Visa Run, Personal, Business...
        Employee send request to his Manager via email.
        This email can be edited by Employee.
        After that, the Manager receive this letter
        and decide to approve or refuse.
    """,
    'author': 'AHCEC',
    'website': 'http://www.ahcec.com',
    'depends': [
        'hr_contract',
        'ahcec_hr_contract',
        'ahcec_hr_dependent',
        'ahcec_hr_air_allowance',
        'hr_holidays'
    ],
    'data': [
        # data
        'data/hr_travel_type_data.xml',
        # 'data/hr_travel_request_email_template_data.xml',
        # View
        'view/hr_travel_request_view.xml',
        'view/ir_attachment_view.xml',
        # 'view/hr_holiday.xml',
        # menu
        'menu/hr_travel_request_menu.xml',
        # security
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
