{
    'name': "PurchaseLimit POS",
    'version': '15.01.0.0   ',
    'depends': ['base', 'mail', 'account', 'website'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "Purchase Limit in POS",
    'application': True,

    'assets': {
        'web.assets_backend': [
            '/purchaselimit_pos/static/src/js/purchase_limit.js',
        ],
    },

    'data': [
        'view/purchase_limit.xml',
    ],
}
