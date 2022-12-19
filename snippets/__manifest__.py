{
    'name': "Snippets",
    'version': '15.01.0.0   ',
    'depends': ['base', 'mail', 'account', 'website'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "Snippets",
    'application': True,

    'assets': {
        'web.assets_frontend': [
            '/snippets/static/src/js/snippet.js',
        ],
    },

    'data': [
        'view/snippet_course.xml',
        'view/website_snippet.xml',
        'website/learning_website.xml'
    ]
}
