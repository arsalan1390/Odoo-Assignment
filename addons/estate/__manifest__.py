{
    'name': "Real-Estate Management",
    'version': '1.0',
    'depends': ['base'],
    'author': "Muhammad Arsalan",
    'category': 'Category',
    'description': """
     This is a test module of Real-Estate Management! 
     Written for the Odoo Quickstart Tutorial.  
    """,
    # data file always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'data/estate_data.xml',
        'data/estate_property_tag_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
