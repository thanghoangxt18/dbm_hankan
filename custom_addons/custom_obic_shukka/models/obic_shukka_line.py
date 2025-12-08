# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ObicShukkaLine(models.Model):
    _name = 'obic.shukka.line'
    _description = '出荷明細 (Shipping Detail Line)'
    _order = 'sequence, id'

    # Link to parent
    shukka_id = fields.Many2one(
        'obic.shukka',
        string='出荷処理',
        required=True,
        ondelete='cascade'
    )
    
    # Sequence for reordering
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )

    # ====================
    # FIELDS - ROW 1
    # ====================
    transfer_instruction_number_line = fields.Char(
        string='移動指示番号',
        size=30,
        placeholder='移動指示番号'
    )
    shukka_destination_warehouse = fields.Char(
        string='出荷先倉庫',
        size=30,
        placeholder='出荷先倉庫'
    )
    final_delivery_destination = fields.Char(
        string='最終納入先',
        size=30,
        placeholder='最終納入先'
    )
    is_reserved = fields.Boolean(
        string='保留',
        default=False
    )

    # ====================
    # FIELDS - ROW 2
    # ====================
    product_id = fields.Many2one(
        'product.product',
        string='商品',
        placeholder='商品'
    )

    # ====================
    # FIELDS - ROW 3
    # ====================
    shukka_number = fields.Char(
        string='出荷番号',
        size=30,
        placeholder='出荷番号'
    )
    loan_classification = fields.Char(
        string='貸出区分',
        size=30,
        placeholder='貸出区分'
    )
    delivery_date_line = fields.Date(
        string='納期',
        placeholder='納期'
    )
    initial_transfer_quantity = fields.Integer(
        string='当初移動数量',
        default=0,
        placeholder='当初移動数量'
    )
    unshipped_quantity = fields.Integer(
        string='未出荷数量',
        default=0,
        placeholder='未出荷数量'
    )
    current_shukka_quantity = fields.Integer(
        string='今回出荷数量',
        default=0,
        placeholder='今回出荷数量'
    )
