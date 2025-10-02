# -*- coding: utf-8 -*-

{
    'name': "LinkedIn Integration",

    'summary': """integrate with linkedin and user can post from odoo to linkedin  """,

    'description': """ """,

    'author': "Tarek Ashry",

    'version': '18.0.1.0.0',

    'depends': [
        'base',

    ],

    'data': [
        'security/ir.model.access.csv',
        'views/linkedin_config_view.xml',
        'views/linkedin_post_view.xml',
        'views/linkedin_template.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
