# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ObicShukka(models.Model):
    _name = 'obic.shukka'
    _description = '出荷処理入力 (Shipping Process Entry)'
    _order = 'reference_date desc, id desc'
    _rec_name = 'shukka_number'  # Use shukka_process_number as display name

    # ====================
    # PHẦN TOP (Phần 1)
    # ====================
    # Bên Trái
    shukka_process_number = fields.Char(
        string='出荷処理番号',
        size=30,
        placeholder='出荷処理番号'
    )
    shukka_number = fields.Char(
        string='出荷番号',
        size=30,
        placeholder='出荷番号'
    )
    shukka_process_type = fields.Selection([
        ('warehouse', '倉庫向け'),
    ],
        string='出荷処理区分',
        default='warehouse',
        placeholder='出荷処理区分'
    )
    
    # Bên Phải
    reference_date = fields.Date(
        string='基準日',
        default=fields.Date.context_today,
        placeholder='基準日'
    )
    previous_shukka_process_number = fields.Char(
        string='前回出荷処理番号',
        size=30,
        placeholder='前回出荷処理番号'
    )
    previous_shukka_number = fields.Char(
        string='前回出荷番号',
        size=30,
        placeholder='前回出荷番号'
    )

    # ====================
    # PHẦN GIỮA - LEFT SIDE (Phần 2 - tỷ lệ 5)
    # ====================
    shukka_classification = fields.Char(
        string='出荷区分',
        size=30,
        placeholder='出荷区分'
    )
    shukka_date = fields.Date(
        string='出荷日',
        placeholder='出荷日'
    )
    warehouse = fields.Char(
        string='倉庫',
        size=30,
        placeholder='倉庫'
    )
    packing_date = fields.Date(
        string='梱包日',
        placeholder='梱包日'
    )
    summary = fields.Char(
        string='摘要',
        size=100,
        placeholder='摘要'
    )
    delivery_date = fields.Date(
        string='納期',
        placeholder='納期'
    )
    shipping_company = fields.Char(
        string='配送業者',
        size=50,
        placeholder='配送業者'
    )
    
    # Radio options
    display_unit = fields.Selection([
        ('shipping_detail', '出荷明細'),
        ('packing_detail', '梱包明細'),
    ],
        string='表示単位',
        default='shipping_detail',
        placeholder='表示単位'
    )
    
    sort_details = fields.Selection([
        ('shukka_line', '出荷行番号'),
        ('product_code', '商品コード'),
        ('packing_symbol', '梱包記号'),
        ('packing_number', '梱包番号'),
    ],
        string='明細並び',
        default='shukka_line',
        placeholder='明細並び'
    )

    # ====================
    # PHẦN GIỮA - RIGHT SIDE (Phần 2 - 抽出条件, tỷ lệ 7)
    # ====================
    data_classification = fields.Selection([
        ('all', '全て'),
        ('order', '受注'),
        ('transfer_instruction', '移動指示'),
    ],
        string='データ区分',
        default='all',
        placeholder='データ区分'
    )
    shukka_target = fields.Selection([
        ('all', '全て'),
        ('after_payment', '入金後出荷'),
    ],
        string='出荷対象',
        default='all',
        placeholder='出荷対象'
    )
    shukka_sales = fields.Float(
        string='出荷売上',
        placeholder='出荷売上'
    )
    business_office = fields.Char(
        string='営業所',
        size=50,
        placeholder='営業所'
    )
    shukka_planned_date = fields.Date(
        string='出荷予定日',
        placeholder='出荷予定日'
    )
    delivery_date_search = fields.Date(
        string='納期',
        placeholder='納期'
    )
    sales_order_number = fields.Char(
        string='受注番号',
        size=30,
        placeholder='受注番号'
    )
    transfer_instruction_number = fields.Char(
        string='移動指示番号',
        size=30,
        placeholder='移動指示番号'
    )
    customer_name = fields.Char(
        string='得意先名',
        size=30,
        placeholder='得意先名'
    )
    person_in_charge = fields.Char(
        string='担当者',
        size=30,
        placeholder='担当者'
    )
    shipping_company_search = fields.Char(
        string='配送業者',
        size=30,
        placeholder='配送業者'
    )
    customer_order_number = fields.Char(
        string='客先注文番号',
        size=30,
        placeholder='客先注文番号'
    )
    product_name = fields.Char(
        string='商品名',
        size=30,
        placeholder='商品名'
    )

    # ====================
    # ONE2MANY RELATIONSHIP
    # ====================
    shukka_line_ids = fields.One2many(
        'obic.shukka.line',
        'shukka_id',
        string='出荷明細'
    )

    # ====================
    # DUMMY ACTION METHODS (chỉ show notification)
    # ====================
    def action_bulk_update_shipping_company(self):
        """配送業者一括更新"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '配送業者一括更新',
                'message': 'この機能は開発中です',
                'type': 'warning',
                'sticky': False,
            }
        }
    
    def action_bulk_overwrite_delivery_date(self):
        """納期一括上書き"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '納期一括上書き',
                'message': 'この機能は開発中です',
                'type': 'warning',
                'sticky': False,
            }
        }
    
    def action_recalculate_delivery_date(self):
        """納期再計算"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '納期再計算',
                'message': 'この機能は開発中です',
                'type': 'warning',
                'sticky': False,
            }
        }
    
    def action_display_switch(self):
        """表示切替"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '表示切替',
                'message': 'この機能は開発中です',
                'type': 'warning',
                'sticky': False,
            }
        }
    
    def action_parallel_split(self):
        """詳細分割"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '詳細分割',
                'message': 'この機能は開発中です',
                'type': 'warning',
                'sticky': False,
            }
        }
    
    def action_split_cancel(self):
        """分割解除"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '分割解除',
                'message': 'この機能は開発中です',
                'type': 'warning',
                'sticky': False,
            }
        }
