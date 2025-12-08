# -*- coding: utf-8 -*-
{
    'name': 'OBIC Shukka Management',
    'version': '1.0',
    'category': 'Inventory',
    'summary': '出荷管理 - OBIC Shipping Management for Japanese ERP',
    'description': """
        OBIC Shukka (Shipping) Management Module
        =========================================
        - Manage shipping process (出荷処理入力)
        - Product line management with sections display
        - Search conditions (抽出条件)
        - Bulk operations for shipping data
    """,
    'author': 'Hankan',
    'website': 'https://www.hankan.com',
    'depends': [
        'base',
        'product',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/obic_shukka_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_obic_shukka/static/src/fields/obic_shukka_line_field/obic_shukka_line_field.js',
            'custom_obic_shukka/static/src/fields/obic_shukka_line_field/obic_shukka_line_field.xml',
            'custom_obic_shukka/static/src/fields/obic_shukka_line_field/obic_shukka_line_field.scss',
            'custom_obic_shukka/static/src/css/obic_shukka.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
