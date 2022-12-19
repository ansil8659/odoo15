{
    'name': "University Event",
    'version': '15.01.0.0   ',
    'depends': ['base', 'website_event'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "university events",
    'application': True,
    # data files always loaded at installation

    'assets': {
        'web.assets_frontend': [
            '/portal_event/static/src/js/portal_event.js',
        ],
    },

    'data': [
        'view/university.xml',
        'view/university_event.xml',
        'view/event_portal_view.xml',
        'security/ir.model.access.csv',
    ],
}
