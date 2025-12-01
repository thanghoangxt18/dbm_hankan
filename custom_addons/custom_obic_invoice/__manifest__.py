# -*- coding: utf-8 -*-
{
    'name': 'Custom OBIC Invoice',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'OBIC 請求管理 (Invoice Management)',
    'description': """
        OBIC Invoice Management System
        ==============================
        * Extend account.move with custom fields
        * Two modes: 伝票単位 (Denpyou) and 明細単位 (Meisai)
        * Custom widgets for each mode
        * Integration with custom_obic_denpyou module
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'account',
        'product',
        'custom_obic_denpyou',  # CRITICAL: Depend on denpyou module
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/obic_invoice_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_obic_invoice/static/src/css/obic_invoice.css',
            # Denpyou line widget (SECTION/CARD format)
            'custom_obic_invoice/static/src/fields/obic_invoice_denpyou_line_field/obic_invoice_denpyou_line_field.js',
            'custom_obic_invoice/static/src/fields/obic_invoice_denpyou_line_field/obic_invoice_denpyou_line_field.xml',
            'custom_obic_invoice/static/src/fields/obic_invoice_denpyou_line_field/obic_invoice_denpyou_line_field.scss',
            
            # Meisai line widget (TABLE format)
            'custom_obic_invoice/static/src/fields/obic_invoice_meisai_line_field/obic_invoice_meisai_line_field.js',
            'custom_obic_invoice/static/src/fields/obic_invoice_meisai_line_field/obic_invoice_meisai_line_field.xml',
            'custom_obic_invoice/static/src/fields/obic_invoice_meisai_line_field/obic_invoice_meisai_line_field.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
