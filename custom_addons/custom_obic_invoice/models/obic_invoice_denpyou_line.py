# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ObicInvoiceDenpyouLine(models.Model):
    """
    伝票単位 Mode - Invoice Denpyou Lines
    Hiển thị dưới dạng SECTION/CARD (tương tự sale_order_line)
    """
    _name = 'obic.invoice.denpyou.line'
    _description = 'OBIC Invoice Denpyou Line'
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
    
    denpyou_id = fields.Many2one(
        'obic.denpyou',
        string='伝票番号',
        required=True,
        help='Related denpyou from custom_obic_denpyou module'
    )
    
    denpyou_number = fields.Char(
        string='伝票番号',
        related='denpyou_id.denpyou_number',
        store=True,
        readonly=True,
        help='Denpyou number from related denpyou'
    )
    
    customer_code = fields.Char(
        string='得意先',
        size=50,
        help='Customer code - auto-filled from denpyou, editable'
    )
    
    denpyou_date = fields.Date(
        string='伝票日付',
        help='Denpyou date'
    )
    
    collection_date = fields.Date(
        string='回収予定日',
        help='Collection date'
    )
    
    denpyou_amount = fields.Float(
        string='伝票金額',
        digits=(12, 2),
        help='Denpyou amount - auto-filled from denpyou, editable'
    )
    
    current_billing_amount = fields.Float(
        string='今回請求額',
        digits=(12, 2),
        help='Current billing amount - auto-filled from denpyou, editable'
    )
    
    person_in_charge = fields.Char(
        string='担当者',
        size=50,
        help='Person in charge'
    )
    
    denpyou_summary = fields.Char(
        string='伝票摘要',
        size=100,
        help='Denpyou summary - auto-filled from denpyou, editable'
    )
    
    is_billing_target = fields.Boolean(
        string='請求対象',
        default=False,
        help='Is billing target'
    )
    
    # ==================== ONCHANGE METHODS ====================
    
    @api.onchange('denpyou_id')
    def _onchange_denpyou_id(self):
        """
        伝票選択時に自動入力
        Auto-fill fields when denpyou is selected
        """
        if self.denpyou_id:
            _logger.info(f'Denpyou selected: {self.denpyou_id.denpyou_number}')
            
            # Auto-fill từ denpyou
            self.customer_code = self.denpyou_id.customer_code
            self.denpyou_date = fields.Date.today()  # Default to today
            self.denpyou_amount = self.denpyou_id.total_current_billing_amount
            self.current_billing_amount = self.denpyou_id.total_current_billing_amount
            self.denpyou_summary = self.denpyou_id.denpyou_summary
            
            _logger.info(f'Auto-filled: customer={self.customer_code}, '
                        f'amount={self.denpyou_amount}, '
                        f'billing={self.current_billing_amount}')
