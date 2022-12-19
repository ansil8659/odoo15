{
    'name': "OrderLine POS",
    'version': '15.01.0.0   ',
    'depends': ['base', 'point_of_sale'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "OrderLine Remove in POS",
    'application': True,

    "assets": {
        'web.assets_backend': [
            '/order_line_pos/static/src/js/clear_all.js',
            '/order_line_pos/static/src/js/clear_line.js',
        ],
        'web.assets_qweb': [
                '/order_line_pos/static/src/xml/clear_all.xml',
                '/order_line_pos/static/src/xml/clear_line.xml',
         ]
    },
}
