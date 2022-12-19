{
    'name': "Hotel Management",
    'version': '15.01.0.0   ',
    'depends': ['base', 'mail', 'account'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "Hotel Room Management",
    'application': True,

    'assets': {
        'web.assets_backend': [
            'hotel_room/static/src/js/action_manager.js'],
    },

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'view/hotel_room.xml',
        'view/hotel_room_facility.xml',
        'view/hotel_room_accommodation.xml',
        'view/hotel_room_food_order.xml',
        'view/hotel_room_food_category.xml',
        'view/hotel_room_food_items.xml',
        'view/report_hotel.xml',
        'website/hotel_website.xml',
        'website/hotel_website_temp.xml',
        'report/report_temp.xml',
        'wizard/hotel_report.xml',

        # 'report/report_excel.xml',
        # 'report/action_manager.js'
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
}
