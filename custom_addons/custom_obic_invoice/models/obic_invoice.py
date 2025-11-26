# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ObicInvoice(models.Model):
    """
    Extend account.move để thêm custom fields cho OBIC Invoice Management
    CRITICAL: Dùng _inherit, KHÔNG dùng _name
    """
    _inherit = 'account.move'

    # ==================== BASIC FIELDS ====================
    
    invoice_number = fields.Char(
        string='請求番号',
        size=30,
        help='Invoice number'
    )
    
    reference_date = fields.Date(
        string='基準日',
        help='Reference date'
    )
    
    previous_input_number = fields.Char(
        string='前回入力番号',
        size=30,
        help='Previous input number'
    )
    
    business_office = fields.Char(
        string='事業所',
        size=50,
        help='Business office'
    )
    
    billing_destination = fields.Char(
        string='請求先',
        size=50,
        help='Billing destination'
    )
    
    invoice_date_custom = fields.Date(
        string='請求日',
        help='Invoice date'
    )
    
    collection_date = fields.Date(
        string='回収予定日',
        help='Collection date'
    )
    
    invoice_unit = fields.Selection([
        ('denpyou', '伝票単位'),
        ('meisai', '明細単位'),
    ], string='請求単位', required=True, default='denpyou',
       help='Invoice unit: Denpyou-based or Meisai-based'
    )
    
    invoice_subject = fields.Char(
        string='請求件名',
        size=50,
        help='Invoice subject'
    )
    
    denpyou_summary = fields.Char(
        string='伝票摘要',
        size=100,
        help='Denpyou summary'
    )
    
    department = fields.Char(
        string='部門',
        size=30,
        help='Department'
    )
    
    # ==================== 抽出条件 (SEARCH CRITERIA) FIELDS ====================
    
    department_group_1 = fields.Char(
        string='部門グループ1',
        size=30,
        help='Department group 1'
    )
    
    accounting_department = fields.Char(
        string='計上部門',
        size=30,
        help='Accounting department'
    )
    
    customer = fields.Char(
        string='得意先',
        size=30,
        help='Customer'
    )
    
    person_in_charge = fields.Char(
        string='担当者',
        size=30,
        help='Person in charge'
    )
    
    sales_date = fields.Date(
        string='売上日',
        help='Sales date'
    )
    
    sales_number = fields.Char(
        string='売上番号',
        size=30,
        help='Sales number'
    )
    
    operator = fields.Char(
        string='オペレータ',
        size=30,
        help='Operator'
    )
    
    change_date = fields.Date(
        string='変更日',
        help='Change date'
    )
    
    # ==================== OTHER FIELDS ====================
    
    tax_adjustment_amount = fields.Float(
        string='消費税調整金額',
        digits=(12, 2),
        help='Tax adjustment amount'
    )
    
    # ==================== ONE2MANY FIELDS (CONDITIONAL) ====================
    
    # Mode 伝票単位
    invoice_denpyou_line_ids = fields.One2many(
        'obic.invoice.denpyou.line',
        'invoice_id',
        string='伝票明細',
        help='Denpyou lines for 伝票単位 mode'
    )
    
    # Mode 明細単位
    invoice_meisai_line_ids = fields.One2many(
        'obic.invoice.meisai.line',
        'invoice_id',
        string='明細',
        help='Meisai lines for 明細単位 mode'
    )
    
    # ==================== COMPUTED TOTALS ====================
    
    # For 伝票単位 mode
    total_current_billing_amount_denpyou = fields.Float(
        string='今回請求額合計',
        compute='_compute_total_denpyou',
        store=True,
        digits=(12, 2),
        help='Total current billing amount for Denpyou mode'
    )
    
    # For 明細単位 mode
    total_current_billing_amount_meisai = fields.Float(
        string='今回請求額合計',
        compute='_compute_total_meisai',
        store=True,
        digits=(12, 2),
        help='Total current billing amount for Meisai mode'
    )
    
    # ==================== COMPUTED METHODS ====================
    
    @api.depends('invoice_denpyou_line_ids.current_billing_amount')
    def _compute_total_denpyou(self):
        """計算 伝票単位 mode 的總金額"""
        for record in self:
            amounts = record.invoice_denpyou_line_ids.mapped('current_billing_amount')
            record.total_current_billing_amount_denpyou = sum(amounts)
            _logger.info(f'[Denpyou Mode] Invoice {record.id}: Total = {record.total_current_billing_amount_denpyou}')
    
    @api.depends('invoice_meisai_line_ids.current_billing_amount')
    def _compute_total_meisai(self):
        """計算 明細単位 mode 的總金額"""
        for record in self:
            amounts = record.invoice_meisai_line_ids.mapped('current_billing_amount')
            record.total_current_billing_amount_meisai = sum(amounts)
            _logger.info(f'[Meisai Mode] Invoice {record.id}: Total = {record.total_current_billing_amount_meisai}')
    
    # ==================== BULK ACTION METHODS ====================
    
    # For 伝票単位 mode
    def action_set_all_denpyou_billing_true(self):
        """一括請求 - Set all denpyou lines as billing target"""
        self.ensure_one()
        _logger.info(f'[Denpyou Mode] Setting all {len(self.invoice_denpyou_line_ids)} lines as billing target')
        self.invoice_denpyou_line_ids.write({'is_billing_target': True})
        return True
    
    def action_set_all_denpyou_billing_false(self):
        """一括解除 - Unset all denpyou lines as billing target"""
        self.ensure_one()
        _logger.info(f'[Denpyou Mode] Unsetting all {len(self.invoice_denpyou_line_ids)} lines as billing target')
        self.invoice_denpyou_line_ids.write({'is_billing_target': False})
        return True
    
    # For 明細単位 mode
    def action_set_all_meisai_billing_true(self):
        """一括請求 - Set all meisai lines as billing"""
        self.ensure_one()
        _logger.info(f'[Meisai Mode] Setting all {len(self.invoice_meisai_line_ids)} lines as billing')
        self.invoice_meisai_line_ids.write({'is_billing': True})
        return True
    
    def action_set_all_meisai_billing_false(self):
        """一括解除 - Unset all meisai lines as billing"""
        self.ensure_one()
        _logger.info(f'[Meisai Mode] Unsetting all {len(self.invoice_meisai_line_ids)} lines as billing')
        self.invoice_meisai_line_ids.write({'is_billing': False})
        return True
    
    # ==================== OTHER METHODS ====================
    
    def action_adjustment_detail_input(self):
        """調整明細入力 - Placeholder for future implementation"""
        _logger.info(f'Adjustment detail input called for invoice {self.id}')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('調整明細入力'),
                'message': _('この機能は開発中です'),
                'type': 'info',
                'sticky': False,
            }
        }
