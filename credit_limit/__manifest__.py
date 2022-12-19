{
    'name': "Credit Limit",
    'version': '15.01.0.0   ',
    'depends': ['base', 'sale_management'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "Sale Order Credit Limit",
    'application': True,
    # data files always loaded at installation
    'data': [
        'view/sale_credit_limit.xml',
        'view/sale_due_amount.xml',
        'security/ir.model.access.csv',
    ],
}
