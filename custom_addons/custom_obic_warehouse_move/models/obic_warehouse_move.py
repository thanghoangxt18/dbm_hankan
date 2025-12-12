# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ObicWarehouseMove(models.Model):
    _name = 'obic.warehouse.move'
    _description = '倉庫移動入力'
    _order = 'reference_date desc, id desc'
    _rec_name = 'move_number'

    # ====================
    # PHẦN HEADER (Layout 6 cột)
    # ====================
    # Cột 1: view_mode (compute field)
    view_mode = fields.Selection(
        [('inquiry', '照会')],
        string='',
        default='inquiry',
        store=False
    )

    # Cột 2: move_number, copy_source_move_number
    move_number = fields.Char(
        string='移動番号',
        size=30,
        placeholder='移動番号'
    )
    copy_source_move_number = fields.Char(
        string='複写元移動番号',
        size=30,
        placeholder='複写元移動番号'
    )

    # Cột 6: reference_date, previous_move_number
    reference_date = fields.Date(
        string='基準日',
        default=fields.Date.context_today,
        placeholder='基準日'
    )
    previous_move_number = fields.Char(
        string='前回移動番号',
        size=30,
        placeholder='前回移動番号'
    )

    # ====================
    # PHẦN MAIN (Layout 12 cột, mỗi field 3 cột)
    # ====================
    # Dòng 1
    business_office = fields.Char(
        string='事業所',
        size=30,
        placeholder='事業所'
    )
    transaction_classification = fields.Char(
        string='取引区分',
        size=30,
        placeholder='取引区分'
    )

    # Dòng 2
    move_date = fields.Date(
        string='移動日',
        placeholder='移動日'
    )
    project_number = fields.Char(
        string='案件番号',
        size=30,
        placeholder='案件番号'
    )

    # Dòng 3
    person_in_charge = fields.Char(
        string='担当者',
        size=30,
        placeholder='担当者'
    )
    person_in_charge_department = fields.Char(
        string='担当者部門',
        size=30,
        placeholder='担当者部門'
    )

    # Dòng 4
    outgoing_warehouse = fields.Char(
        string='出庫倉庫',
        size=30,
        placeholder='出庫倉庫'
    )
    incoming_warehouse = fields.Char(
        string='入庫倉庫',
        size=30,
        placeholder='入庫倉庫'
    )

    # Dòng 5
    outgoing_stock_location = fields.Char(
        string='出庫在庫場所',
        size=30,
        placeholder='出庫在庫場所'
    )
    incoming_stock_location = fields.Char(
        string='入庫在庫場所',
        size=30,
        placeholder='入庫在庫場所'
    )

    # Dòng 6
    shipping_company = fields.Char(
        string='配送業者',
        size=30,
        placeholder='配送業者'
    )
    slip_summary = fields.Char(
        string='伝票摘要',
        size=100,
        placeholder='伝票摘要'
    )

    # ====================
    # ONE2MANY
    # ====================
    move_line_ids = fields.One2many(
        'obic.warehouse.move.line',
        'move_id',
        string='倉庫移動明細'
    )

    # ====================
    # COMPUTED FIELDS
    # ====================
    total_move_amount = fields.Float(
        string='合計金額',
        compute='_compute_total_move_amount',
        store=True,
        digits=(16, 2)
    )

    @api.depends('move_line_ids.move_amount')
    def _compute_total_move_amount(self):
        """合計金額 = 全ての移動明細の移動金額の合計"""
        for record in self:
            record.total_move_amount = sum(record.move_line_ids.mapped('move_amount'))
    
    # ====================
    # DUMMY ACTIONS
    # ====================
    def action_arrangement_deployment(self):
        """手配展開ボタン - Dummy action"""
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
