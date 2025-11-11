# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # OBIC specific fields (prefix with obic_ to avoid conflicts)
    obic_order_category = fields.Char(
        string='受注区分',
        size=20,
        help='Order category (受注区分)'
    )
    
    obic_is_tax_excluded = fields.Boolean(
        string='外税',
        default=True,
        help='Tax excluded (外税)'
    )
    
    obic_specification = fields.Char(
        string='規格',
        size=20,
        help='Specification (規格)'
    )

    # Row 2 fields
    obic_quantity = fields.Integer(
        string='総数',
        default=1,
        help='Total quantity (総数)'
    )
    
    obic_list_unit_price = fields.Float(
        string='上代単価',
        digits=(12, 2),
        help='List unit price (上代単価)'
    )
    
    obic_discount_rate = fields.Float(
        string='掛率',
        digits=(5, 2),
        default=100.00,
        help='Discount rate in percentage (掛率)'
    )
    
    obic_sales_unit_price = fields.Float(
        string='売上単価',
        digits=(12, 2),
        help='Sales unit price (売上単価)'
    )
    
    obic_sales_amount = fields.Float(
        string='売上金額',
        compute='_compute_obic_sales_amount',
        store=True,
        digits=(12, 2),
        help='Sales amount = 売上単価 × 総数'
    )
    
    obic_sales_tax = fields.Float(
        string='売上消費税',
        compute='_compute_obic_sales_tax',
        store=True,
        digits=(12, 2),
        help='Sales tax = 10% × 売上金額'
    )

    # Row 3 fields
    obic_purchase_temp_unit_price = fields.Float(
        string='発注仮単価',
        digits=(12, 2),
        help='Purchase temporary unit price (発注仮単価)'
    )
    
    obic_purchase_temp_amount = fields.Float(
        string='発注仮金額',
        digits=(12, 2),
        help='Purchase temporary amount (発注仮金額)'
    )
    
    obic_warehouse_code = fields.Char(
        string='倉庫',
        size=20,
        help='Warehouse code (倉庫)'
    )
    
    obic_cost_amount = fields.Float(
        string='原価金額',
        digits=(12, 2),
        help='Cost amount (原価金額)'
    )
    
    obic_gross_profit = fields.Float(
        string='粗利',
        compute='_compute_obic_gross_profit',
        store=True,
        digits=(12, 2),
        help='Gross profit = 売上金額 - 原価金額'
    )

    # Row 4 fields
    obic_shipping_destination = fields.Char(
        string='出荷先',
        size=20,
        help='Shipping destination (出荷先)'
    )
    
    obic_inventory_warehouse = fields.Char(
        string='在庫管理倉庫',
        size=20,
        help='Inventory management warehouse (在庫管理倉庫)'
    )
    
    obic_line_remark = fields.Char(
        string='明細摘要',
        size=100,
        help='Line remark (明細摘要)'
    )

    @api.depends('obic_sales_unit_price', 'obic_quantity')
    def _compute_obic_sales_amount(self):
        """Calculate sales amount"""
        for line in self:
            line.obic_sales_amount = line.obic_sales_unit_price * line.obic_quantity

    @api.depends('obic_sales_amount', 'obic_is_tax_excluded')
    def _compute_obic_sales_tax(self):
        """Calculate sales tax (10%)"""
        for line in self:
            if line.obic_is_tax_excluded:
                line.obic_sales_tax = line.obic_sales_amount * 0.10
            else:
                line.obic_sales_tax = 0.0

    @api.depends('obic_sales_amount', 'obic_cost_amount')
    def _compute_obic_gross_profit(self):
        """Calculate gross profit"""
        for line in self:
            line.obic_gross_profit = line.obic_sales_amount - line.obic_cost_amount

    @api.onchange('product_id')
    def _onchange_obic_product_id(self):
        """Auto-fill prices when product is selected"""
        if self.product_id:
            self.obic_list_unit_price = self.product_id.list_price
            self.obic_sales_unit_price = self.product_id.list_price

    @api.onchange('obic_list_unit_price', 'obic_discount_rate')
    def _onchange_obic_calculate_sales_price(self):
        """Calculate sales unit price from list price and discount rate"""
        if self.obic_list_unit_price and self.obic_discount_rate:
            self.obic_sales_unit_price = self.obic_list_unit_price * (self.obic_discount_rate / 100.0)
