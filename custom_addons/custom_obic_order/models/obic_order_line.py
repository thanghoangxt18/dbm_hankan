# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ObicOrderLine(models.Model):
    _name = 'obic.order.line'
    _description = 'OBIC Order Line (受注明細)'
    _order = 'order_id, sequence, id'

    # Link to order
    order_id = fields.Many2one(
        'obic.order',
        string='受注',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    sequence = fields.Integer(
        string='順序',
        default=10,
        help='Display order sequence'
    )

    # Row 1 fields
    order_category = fields.Char(
        string='受注区分',
        size=20,
        help='Order category (受注区分)'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='商品',
        help='Product selection (商品)'
    )
    
    product_name = fields.Char(
        string='商品名',
        related='product_id.name',
        readonly=True
    )
    
    is_tax_excluded = fields.Boolean(
        string='外税',
        default=True,
        help='Tax excluded (外税)'
    )
    
    specification = fields.Char(
        string='規格',
        size=20,
        help='Specification (規格)'
    )

    # Row 2 fields
    quantity = fields.Integer(
        string='総数',
        default=1,
        help='Total quantity (総数)'
    )
    
    list_unit_price = fields.Float(
        string='上代単価',
        digits=(12, 2),
        help='List unit price (上代単価)'
    )
    
    discount_rate = fields.Float(
        string='掛率',
        digits=(5, 2),
        default=100.00,
        help='Discount rate in percentage (掛率)'
    )
    
    sales_unit_price = fields.Float(
        string='売上単価',
        digits=(12, 2),
        help='Sales unit price (売上単価)'
    )
    
    sales_amount = fields.Float(
        string='売上金額',
        compute='_compute_sales_amount',
        store=True,
        digits=(12, 2),
        help='Sales amount = 売上単価 × 総数'
    )
    
    sales_tax = fields.Float(
        string='売上消費税',
        compute='_compute_sales_tax',
        store=True,
        digits=(12, 2),
        help='Sales tax = 10% × 売上金額'
    )

    # Row 3 fields
    purchase_temp_unit_price = fields.Float(
        string='発注仮単価',
        digits=(12, 2),
        help='Purchase temporary unit price (発注仮単価)'
    )
    
    purchase_temp_amount = fields.Float(
        string='発注仮金額',
        digits=(12, 2),
        help='Purchase temporary amount (発注仮金額)'
    )
    
    warehouse_code = fields.Char(
        string='倉庫',
        size=20,
        help='Warehouse code (倉庫)'
    )
    
    cost_amount = fields.Float(
        string='原価金額',
        digits=(12, 2),
        help='Cost amount (原価金額)'
    )
    
    gross_profit = fields.Float(
        string='粗利',
        compute='_compute_gross_profit',
        store=True,
        digits=(12, 2),
        help='Gross profit = 売上金額 - 原価金額'
    )

    # Row 4 fields
    shipping_destination = fields.Char(
        string='出荷先',
        size=20,
        help='Shipping destination (出荷先)'
    )
    
    inventory_warehouse = fields.Char(
        string='在庫管理倉庫',
        size=20,
        help='Inventory management warehouse (在庫管理倉庫)'
    )
    
    line_remark = fields.Char(
        string='明細摘要',
        size=100,
        help='Line remark (明細摘要)'
    )

    @api.depends('sales_unit_price', 'quantity')
    def _compute_sales_amount(self):
        """Calculate sales amount"""
        for line in self:
            line.sales_amount = line.sales_unit_price * line.quantity

    @api.depends('sales_amount', 'is_tax_excluded')
    def _compute_sales_tax(self):
        """Calculate sales tax (10%)"""
        for line in self:
            if line.is_tax_excluded:
                line.sales_tax = line.sales_amount * 0.10
            else:
                line.sales_tax = 0.0

    @api.depends('sales_amount', 'cost_amount')
    def _compute_gross_profit(self):
        """Calculate gross profit"""
        for line in self:
            line.gross_profit = line.sales_amount - line.cost_amount

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Auto-fill prices when product is selected"""
        if self.product_id:
            self.list_unit_price = self.product_id.list_price
            self.sales_unit_price = self.product_id.list_price
            # self.cost_amount = self.product_id.standard_price * self.quantity

    @api.onchange('list_unit_price', 'discount_rate')
    def _onchange_calculate_sales_price(self):
        """Calculate sales unit price from list price and discount rate"""
        if self.list_unit_price and self.discount_rate:
            self.sales_unit_price = self.list_unit_price * (self.discount_rate / 100.0)
