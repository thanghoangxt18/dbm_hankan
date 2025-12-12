# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ObicWarehouseMoveLine(models.Model):
    _name = 'obic.warehouse.move.line'
    _description = '倉庫移動明細'
    _order = 'line_number, sequence, id'

    # ====================
    # BASIC FIELDS
    # ====================
    move_id = fields.Many2one(
        'obic.warehouse.move',
        string='倉庫移動',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )

    # ====================
    # MODAL FORM FIELDS (Layout 12 cột)
    # ====================
    # Dòng 1 (2-3-3)
    continuous_input = fields.Boolean(
        string='連続入力',
        default=False
    )
    move_classification = fields.Char(
        string='移動区分',
        size=30,
        placeholder='移動区分'
    )

    # Dòng 2 (2-3-3)
    line_number = fields.Integer(
        string='行番号',
        placeholder='行番号'
    )
    outgoing_business_office = fields.Char(
        string='出庫事業所',
        size=30,
        placeholder='出庫事業所'
    )
    incoming_business_office = fields.Char(
        string='入庫事業所',
        size=30,
        placeholder='入庫事業所'
    )

    # Dòng 3 (2-3-3)
    sort_order = fields.Integer(
        string='並び順',
        placeholder='並び順'
    )
    outgoing_warehouse_line = fields.Char(
        string='出庫倉庫',
        size=30,
        placeholder='出庫倉庫'
    )
    incoming_warehouse_line = fields.Char(
        string='入庫倉庫',
        size=30,
        placeholder='入庫倉庫'
    )

    # Dòng 4 (skip 2, 3-3)
    outgoing_stock_location_line = fields.Char(
        string='出庫在庫場所',
        size=30,
        placeholder='出庫在庫場所'
    )
    incoming_stock_location_line = fields.Char(
        string='入庫在庫場所',
        size=30,
        placeholder='入庫在庫場所'
    )

    # Dòng 5 (skip 2, 6)
    product_id = fields.Many2one(
        'product.product',
        string='商品',
        placeholder='商品'
    )

    # Dòng 6 (skip 2, 3-3)
    specify_outgoing_shelf_breakdown = fields.Boolean(
        string='出庫棚番を内訳で指定する',
        default=False
    )
    specify_incoming_shelf_breakdown = fields.Boolean(
        string='入庫棚番を内訳で指定する',
        default=False
    )

    # Dòng 7 (skip 2, 3-3)
    outgoing_shelf_number = fields.Char(
        string='出庫棚番',
        size=30,
        placeholder='出庫棚番'
    )
    incoming_shelf_number = fields.Char(
        string='入庫棚番',
        size=30,
        placeholder='入庫棚番'
    )

    # Dòng 8 (skip 2, mỗi field 2 cột)
    package_form = fields.Integer(
        string='荷姿',
        default=0,
        placeholder='荷姿'
    )
    quantity_per_package = fields.Integer(
        string='入数',
        default=0,
        placeholder='入数'
    )
    number_of_packages = fields.Integer(
        string='荷数',
        default=0,
        placeholder='荷数'
    )
    loose_quantity = fields.Integer(
        string='バラ数',
        default=0,
        placeholder='バラ数'
    )
    total_quantity = fields.Integer(
        string='数量',
        default=0,
        placeholder='数量'
    )

    # Dòng 9 (skip 2, 3-3)
    move_unit_price = fields.Float(
        string='移動単価',
        digits=(16, 2),
        default=0.0,
        placeholder='移動単価'
    )
    move_amount = fields.Float(
        string='移動金額',
        digits=(16, 2),
        compute='_compute_move_amount',
        store=True,
        placeholder='移動金額'
    )

    # Dòng 10 (skip 2, 2 cột)
    detail_summary = fields.Char(
        string='移動明細摘要',
        size=100,
        placeholder='移動明細摘要'
    )

    # ====================
    # COMPUTE METHODS
    # ====================
    @api.depends('total_quantity', 'move_unit_price')
    def _compute_move_amount(self):
        """移動金額 = 数量 × 移動単価"""
        for record in self:
            record.move_amount = record.total_quantity * record.move_unit_price

    # ====================
    # DUMMY ACTIONS
    # ====================
    def action_outgoing_breakdown_input(self):
        """出庫内訳入力ボタン - Dummy action"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '開発中',
                'message': 'この機能は開発中です',
                'type': 'warning',
                'sticky': False,
            }
        }

    def action_analysis_code(self):
        """分析コードボタン - Dummy action"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '開発中',
                'message': 'この機能は開発中です',
                'type': 'warning',
                'sticky': False,
            }
        }

    def action_incoming_breakdown_input(self):
        """入庫内訳入力ボタン - Dummy action"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '開発中',
                'message': 'この機能は開発中です',
                'type': 'warning',
                'sticky': False,
            }
        }
