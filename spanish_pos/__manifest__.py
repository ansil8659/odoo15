{
    'name': "Spanish POS",
    'version': '15.01.0.0   ',
    'depends': ['base', 'mail', 'account', 'website'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "Spanish name in POS",
    'application': True,

    'assets': {
        'web.assets_qweb': [
            '/spanish_pos/static/src/xml/receipt_pos.xml',
            '/spanish_pos/static/src/xml/product_view_pos.xml',
        ],
        'web.assets_backend': [
            '/spanish_pos/static/src/js/receipt_pos.js',
            '/spanish_pos/static/src/js/product_view_pos.js',
        ],
    },

    'data': [
        'view/spanish_name.xml',
    ],

    # 'qweb': [
    #     'static/src/xml/receipt_pos.xml',
    # ]
}
