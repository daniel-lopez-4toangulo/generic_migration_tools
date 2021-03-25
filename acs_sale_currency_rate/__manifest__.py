# -*- coding: utf-8 -*-
#╔══════════════════════════════════════════════════════════════════╗
#║                                                                  ║
#║                ╔═══╦╗       ╔╗  ╔╗     ╔═══╦═══╗                 ║
#║                ║╔═╗║║       ║║ ╔╝╚╗    ║╔═╗║╔═╗║                 ║
#║                ║║ ║║║╔╗╔╦╦══╣╚═╬╗╔╬╗ ╔╗║║ ╚╣╚══╗                 ║
#║                ║╚═╝║║║╚╝╠╣╔╗║╔╗║║║║║ ║║║║ ╔╬══╗║                 ║
#║                ║╔═╗║╚╣║║║║╚╝║║║║║╚╣╚═╝║║╚═╝║╚═╝║                 ║
#║                ╚╝ ╚╩═╩╩╩╩╩═╗╠╝╚╝╚═╩═╗╔╝╚═══╩═══╝                 ║
#║                          ╔═╝║     ╔═╝║                           ║
#║                          ╚══╝     ╚══╝                           ║
#║ SOFTWARE DEVELOPED AND SUPPORTED BY ALMIGHTY CONSULTING SERVICES ║
#║                   COPYRIGHT (C) 2016 - TODAY                     ║
#║                   http://www.almightycs.com                      ║
#║                                                                  ║
#╚══════════════════════════════════════════════════════════════════╝
{
    'name': 'Manual Currency rate in Sale Orders',
    'summary': 'Manual Currency rate in Sale Orders',
    'description': """
Sale Currency Rate
    """,
    'version': '1.0.2',
    'category': 'Accounting',
    'author': 'Almighty Consulting Services',
    'website': 'http://www.almightycs.com',
    'depends': ['sale', 'acs_invoice_currency_rate'],
    'data': [
        'views/sale_view.xml',
    ],
    'images': [
        'static/description/acs_record_currency_rate_almightycs_cover.jpg',
    ],
    'installable': True,
    'sequence': 1,
    'price': 15,
    'currency': 'EUR',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
