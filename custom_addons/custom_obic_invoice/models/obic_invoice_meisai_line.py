# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ObicInvoiceMeisaiLine(models.Model):
    """
    明細単位 Mode - Invoice Meisai Lines
    Hiển thị dưới dạng TABLE với 11 columns (tương tự denpyou_line)
    """
    _name = 'obic.invoice.meisai.line'
    _description = 'OBIC Invoice Meisai Line'
    _order = 'sequence, id'

    # ==================== BASIC FIELDS ====================
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Used for ordering lines'
    )
    
    invoice_id = fields.Many2one(
        'account.move',
        string='請求',
        required=True,
        ondelete='cascade',
        help='Related invoice'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='商品名',
        required=True,
        help='Product'
    )
    
    detail_amount = fields.Float(
        string='明細金額',
        digits=(12, 2),
        help='Detail amount - auto-filled from product.list_price, editable'
    )
    
    quantity = fields.Integer(
        string='数量',
        required=True,
        default=1,
        help='Quantity'
    )
    
    current_billing_amount = fields.Float(
        string='今回請求額',
        compute='_compute_current_billing_amount',
        store=True,
        readonly=False,  # Allow manual edit
        digits=(12, 2),
        help='Current billing amount = detail_amount × quantity'
    )
    
    is_billing = fields.Boolean(
        string='請求',
        default=False,
        help='Is billing'
    )
    
    # ==================== COMPUTED METHODS ====================
    
    @api.depends('detail_amount', 'quantity')
    def _compute_current_billing_amount(self):
        """
        計算 今回請求額 = 明細金額 × 数量
        Compute current billing amount
        """
        for line in self:
            line.current_billing_amount = line.detail_amount * line.quantity
            _logger.info(f'Line {line.id}: {line.detail_amount} × {line.quantity} = {line.current_billing_amount}')
    
    # ==================== ONCHANGE METHODS ====================
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
        商品選択時に明細金額を自動入力
        Auto-fill detail_amount when product is selected
        """
        if self.product_id:
            self.detail_amount = self.product_id.list_price
            _logger.info(f'Product {self.product_id.name} selected: '
                        f'detail_amount = {self.detail_amount}')
