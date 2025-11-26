# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ObicDenpyouLine(models.Model):
    """
    OBIC伝票明細 (Voucher Line) - Line model
    Quản lý từng dòng chi tiết của voucher
    """
    _name = 'obic.denpyou.line'
    _description = 'OBIC Denpyou Line (伝票明細)'
    _order = 'sequence, id'

    # ========== BASIC FIELDS ==========
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Thứ tự hiển thị (for drag-drop ordering)'
    )
    
    denpyou_id = fields.Many2one(
        'obic.denpyou',
        string='伝票',
        required=True,
        ondelete='cascade',
        index=True,
        help='伝票 (Parent voucher)'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='商品名',
        required=True,
        help='商品名 (Product)'
    )
    
    detail_amount = fields.Float(
        string='明細金額',
        digits=(12, 2),
        help='明細金額 (Detail amount) - Editable'
    )
    
    quantity = fields.Integer(
        string='数量',
        required=True,
        default=1,
        help='数量 (Quantity)'
    )
    
    current_billing_amount = fields.Float(
        string='今回請求額',
        compute='_compute_current_billing_amount',
        store=True,
        readonly=False,  # Allow manual edit
        digits=(12, 2),
        help='今回請求額 = 明細金額 × 数量 (Computed but editable)'
    )
    
    is_billing = fields.Boolean(
        string='請求',
        default=False,
        help='請求 (Billing flag)'
    )

    # ========== COMPUTE METHODS ==========
    @api.depends('detail_amount', 'quantity')
    def _compute_current_billing_amount(self):
        """
        今回請求額を計算 (Calculate current billing amount)
        Formula: current_billing_amount = detail_amount × quantity
        """
        for line in self:
            amount = line.detail_amount * line.quantity
            line.current_billing_amount = amount
            _logger.debug(f'Line {line.id}: {line.detail_amount} × {line.quantity} = {amount}')

    # ========== ONCHANGE METHODS ==========
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
        商品選択時に明細金額を自動入力
        Auto-fill detail_amount from product.list_price when product is selected
        """
        if self.product_id:
            self.detail_amount = self.product_id.list_price
            _logger.info(f'Product {self.product_id.name} selected: detail_amount = {self.detail_amount}')
