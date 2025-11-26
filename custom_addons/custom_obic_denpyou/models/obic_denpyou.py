# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ObicDenpyou(models.Model):
    """
    OBIC伝票 (Voucher) - Main model
    Quản lý thông tin chung của voucher/denpyou
    """
    _name = 'obic.denpyou'
    _description = 'OBIC Denpyou (伝票)'
    _order = 'denpyou_number desc'
    _rec_name = 'denpyou_number'  # Use denpyou_number as display name

    # ========== BASIC FIELDS ==========
    denpyou_number = fields.Char(
        string='伝票番号',
        size=30,
        required=True,
        index=True,
        copy=False,
        help='伝票番号 (Unique voucher number)'
    )
    
    customer_code = fields.Char(
        string='得意先',
        size=50,
        help='得意先コード (Customer code)'
    )
    
    delivery_destination = fields.Char(
        string='納入先',
        size=50,
        help='納入先 (Delivery destination)'
    )
    
    denpyou_summary = fields.Char(
        string='伝票摘要',
        size=100,
        help='伝票摘要 (Voucher summary)'
    )
    
    subject = fields.Char(
        string='件名',
        size=100,
        help='件名 (Subject)'
    )

    # ========== ONE2MANY FIELD ==========
    line_ids = fields.One2many(
        'obic.denpyou.line',
        'denpyou_id',
        string='明細',
        help='伝票明細 (Voucher lines)'
    )

    # ========== COMPUTED FIELDS ==========
    total_current_billing_amount = fields.Float(
        string='今回請求額合計',
        compute='_compute_total_current_billing_amount',
        store=True,
        digits=(12, 2),
        help='今回請求額合計 = Sum of all lines current_billing_amount'
    )

    # ========== CONSTRAINTS ==========
    _sql_constraints = [
        ('denpyou_number_unique', 'unique(denpyou_number)', 
         '伝票番号は既に存在します。(Denpyou number must be unique)')
    ]

    # ========== COMPUTE METHODS ==========
    @api.depends('line_ids.current_billing_amount')
    def _compute_total_current_billing_amount(self):
        """今回請求額合計を計算 (Calculate total current billing amount)"""
        for record in self:
            total = sum(line.current_billing_amount for line in record.line_ids)
            record.total_current_billing_amount = total
            _logger.info(f'Denpyou {record.denpyou_number}: Total billing amount = {total}')

    # ========== ACTION METHODS ==========
    def action_set_all_billing_true(self):
        """
        一括請求 (Bulk Billing)
        Set tất cả lines' is_billing = True
        """
        self.ensure_one()
        _logger.info(f'Setting billing TRUE for {len(self.line_ids)} lines in denpyou {self.denpyou_number}')
        
        if self.line_ids:
            self.line_ids.write({'is_billing': True})
            _logger.info('Billing set to TRUE successfully')
        else:
            _logger.warning('No lines to set billing')
        
        return True

    def action_set_all_billing_false(self):
        """
        一括解除 (Bulk Remove Billing)
        Set tất cả lines' is_billing = False
        """
        self.ensure_one()
        _logger.info(f'Setting billing FALSE for {len(self.line_ids)} lines in denpyou {self.denpyou_number}')
        
        if self.line_ids:
            self.line_ids.write({'is_billing': False})
            _logger.info('Billing set to FALSE successfully')
        else:
            _logger.warning('No lines to remove billing')
        
        return True
