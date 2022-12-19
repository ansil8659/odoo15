{
    'name': "Discount Limit",
    'version': '15.01.0.0   ',
    'depends': ['base', 'sale_management'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "Sa;e Order Discount Limit",
    'application': True,
    # data files always loaded at installation
    'data': [
        'view/sale_discount_limit.xml',
        'security/ir.model.access.csv',
    ],
}
