{
    'name': "Import Orderline",
    'version': '15.01.0.0   ',
    'depends': ['base', 'sale_management'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "Order Line Import",
    'application': True,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'view/orderline_import.xml',
        'wizard/orderline_wizard.xml',
    ],
}
