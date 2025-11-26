# -*- coding: utf-8 -*-
{
    'name': 'Custom OBIC Denpyou',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'OBIC伝票管理 (Voucher Management)',
    'description': """
        OBIC Denpyou (伝票) Management Module
        =====================================
        - 伝票 (Voucher) management with line items
        - Custom table-based UI with inline labels
        - Bulk billing operations (一括請求/一括解除)
        - Auto-calculation of billing amounts
    """,
    'author': 'Hankan',
    'website': 'https://hankan.co.jp',
    'depends': [
        'base',
        'product',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/obic_denpyou_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_obic_denpyou/static/src/fields/obic_denpyou_line_field/obic_denpyou_line_field.js',
            'custom_obic_denpyou/static/src/fields/obic_denpyou_line_field/obic_denpyou_line_field.xml',
            'custom_obic_denpyou/static/src/fields/obic_denpyou_line_field/obic_denpyou_line_field.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
