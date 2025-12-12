# -*- coding: utf-8 -*-
{
    'name': '倉庫移動管理',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'OBIC倉庫移動処理入力システム',
    'description': """
        倉庫移動管理モジュール
        =====================
        倉庫間の商品移動を管理するためのモジュールです。
        
        主な機能:
        * 倉庫移動入力
        * 移動明細管理
        * 出庫・入庫情報管理
    """,
    'author': 'Hankan',
    'website': 'https://www.hankan.co.jp',
    'depends': [
        'base',
        'product',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/obic_warehouse_move_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_obic_warehouse_move/static/src/fields/obic_warehouse_move_line_field/obic_warehouse_move_line_field.js',
            'custom_obic_warehouse_move/static/src/fields/obic_warehouse_move_line_field/obic_warehouse_move_line_field.xml',
            'custom_obic_warehouse_move/static/src/fields/obic_warehouse_move_line_field/obic_warehouse_move_line_field.scss',
            'custom_obic_warehouse_move/static/src/css/obic_warehouse_move.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
