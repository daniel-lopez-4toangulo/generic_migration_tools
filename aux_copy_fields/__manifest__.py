# -*- coding: utf-8 -*-
# Marcap Sale Exe
{
    'name' : 'Migration Aux Fields',
    'version' : '1.0',
    'summary': 'For storing important fields for the Localization Migration process',
    'description': """
    """,
    'category': 'Tools',
    'website': 'https://www.odoo.com',
    'images' : [],
    'depends' : ['base_setup', 'account'],
    'data': [
        'views/nviews.xml',
        'views/iviews.xml'
    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
