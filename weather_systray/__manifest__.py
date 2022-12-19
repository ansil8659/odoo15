{
    'name': "Weather Notification",
    'version': '15.01.0.0   ',
    'depends': ['base', 'mail', 'account', 'website'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "weather notification in systray",
    'application': True,

    'assets': {
        'web.assets_qweb': [
            '/weather_systray/static/src/xml/weather.xml',

        ],
        'web.assets_backend': [
            '/weather_systray/static/src/js/weather.js',
            'https://unpkg.com/sweetalert/dist/sweetalert.min.js'
        ],
    },
}
