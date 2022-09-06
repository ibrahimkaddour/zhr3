{
    'name': "Hr Salary Rules",
    'summary': """ Human Resource Salary Rules ZHR""",
    'description': "",
    'author': 'Ibrahim.K',
    'website': 'http://www.ahcec.com',
    'category': 'Human Resources',
    'version': '1.0',
    'sequence': 20,
    'depends': ['hr_payroll', 'hr_payroll_account', 'account'],
    'data': [
        'views/salary_rule.xml',
    ],
    'demo': ['demo/hr_employee_demo.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
