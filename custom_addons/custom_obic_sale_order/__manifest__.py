# -*- coding: utf-8 -*-
{
    'name': 'Custom OBIC Sale Order',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'OBIC custom UI for Odoo Sale Order (受注管理)',
    'description': """
        Custom Sale Order Module with OBIC UI
        ======================================
        - Extends standard Odoo sale.order and sale.order.line
        - Japanese-style order form layout
        - Complex multi-column layout
        - Integration with customer, supplier, and delivery info
        - All OBIC custom fields and logic
    """,
    'author': 'Hankan',
    'website': 'https://hankan.co.jp',
    'depends': [
        'base',
        'sale',
        'sale_management',
        'product',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/modal_views.xml',
        'views/menu_views.xml',
        'reports/new_template_report.xml',
		    'views/new_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_obic_sale_order/static/src/css/obic_order.css',
            'custom_obic_sale_order/static/src/js/obic_order_form.js',
            # Sale Order Line Manager Components
            'custom_obic_sale_order/static/src/components/line_modal/line_modal.js',
            'custom_obic_sale_order/static/src/components/line_modal/line_modal.xml',
            'custom_obic_sale_order/static/src/components/line_section/line_section.js',
            'custom_obic_sale_order/static/src/components/line_section/line_section.xml',
            'custom_obic_sale_order/static/src/components/sale_order_line_manager/sale_order_line_manager.js',
            'custom_obic_sale_order/static/src/components/sale_order_line_manager/sale_order_line_manager.xml',
            'custom_obic_sale_order/static/src/components/sale_order_line_manager/sale_order_line_manager.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
