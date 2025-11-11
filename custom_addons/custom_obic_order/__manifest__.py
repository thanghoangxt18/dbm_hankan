# -*- coding: utf-8 -*-
{
    'name': 'Custom OBIC Order',
    'version': '1.0.1',  # Tăng version để trigger migration
    'category': 'Sales',
    'summary': 'Custom order management module for OBIC system (受注管理)',
    'description': """
        Custom Order Management Module
        ================================
        - Japanese-style order form layout
        - Complex multi-column layout
        - Order tracking and management
        - Integration with customer, supplier, and delivery info
    """,
    'author': 'Hankan',
    'website': 'https://hankan.co.jp',
    'depends': [
        'base',
        'sale',
        'product',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/obic_order_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
         'custom_obic_order/static/src/css/obic_order.css',
            'custom_obic_order/static/src/js/obic_order_form.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
