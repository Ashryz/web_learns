# -*- coding: utf-8 -*-

{
    'name': "Weblearns Session One",

    'summary': """ """,

    'description': """ """,

    'author': "Tarek Ashry",

    'version': '18.0.1.0.0',

    'depends': [
        'base',
        'stock',
        'purchase',
    ],

    'data': [
        'security/ir.model.access.csv',
        'security/equipment_category_security.xml',
        'views/equipment_category_view.xml',
        'views/product_template_view.xml',
        'views/purchase_order_view.xml',
        'views/res_partner_view.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
