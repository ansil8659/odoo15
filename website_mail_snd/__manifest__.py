{
    'name': "Website Mail",
    'version': '15.01.0.0   ',
    'depends': ['base', 'mail', 'account', 'website', 'sale_management'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "Send Mail From Website",
    'application': True,

    'assets': {
        'web.assets_frontend': [
            '/website_mail_snd/static/src/js/mail_website.js',
        ],
    },

    'data': [
        'data/mail_template.xml',
    ]
}
