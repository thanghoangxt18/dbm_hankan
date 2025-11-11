# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Mode control (照会 dropdown)
    view_mode = fields.Selection([
        ('view', '照会'),
        ('edit', '登録'),
    ], string='モード', default='edit', help='Form view mode control')

    # Main order information
    order_number = fields.Char(
        string='受注番号',
        size=20,
        copy=False,
        index=True,
        help='Order number (受注番号)'
    )
    
    quotation_number = fields.Char(
        string='見積番号',
        size=20,
        copy=False,
        help='Quotation number (見積番号)'
    )
    
    source_order_number = fields.Char(
        string='複写元受注番号',
        size=20,
        copy=False,
        help='Source order number for copy (複写元受注番号)'
    )
    
    base_date = fields.Date(
        string='基準日',
        help='Current date display (基準日)'
    )
    
    previous_input_number = fields.Char(
        string='前回入力番号',
        size=20,
        help='Previous input number (前回入力番号)'
    )

    # Checkboxes - Top row
    order_confirmation_not_required = fields.Boolean(
        string='受注確認書不要',
        default=False,
        help='Order confirmation not required'
    )
    
    order_confirmation_immediate = fields.Boolean(
        string='受注確認書即伝',
        default=False,
        help='Order confirmation immediate transmission'
    )
    
    purchase_order_immediate = fields.Boolean(
        string='発注書即伝発行',
        default=False,
        help='Purchase order immediate issuance'
    )

    # Business classification fields
    business_office = fields.Char(
        string='事業所',
        size=20,
        help='Business office (事業所)'
    )
    
    business_category = fields.Char(
        string='業務区分',
        size=20,
        help='Business category (業務区分)'
    )
    
    order_category = fields.Char(
        string='受注区分',
        size=20,
        help='Order category (受注区分)'
    )

    # Checkboxes - Second row
    ship_after_payment = fields.Boolean(
        string='入金後出荷',
        default=False,
        help='Ship after payment received'
    )
    
    ship_by_voucher = fields.Boolean(
        string='伝票単位出荷',
        default=False,
        help='Ship by voucher unit'
    )

    # Date fields
    order_date = fields.Date(
        string='受注日',
        default=fields.Date.context_today,
        help='Order date (受注日)'
    )
    
    shipping_date = fields.Date(
        string='出荷日',
        help='Shipping date (出荷日)'
    )
    
    delivery_deadline = fields.Date(
        string='受注納期',
        help='Order delivery deadline (受注納期)'
    )
    
    sales_scheduled_date = fields.Date(
        string='売上予定日',
        help='Scheduled sales date (売上予定日)'
    )
    
    introduction_category = fields.Char(
        string='導入区分',
        size=20,
        help='Introduction category (導入区分)'
    )
    
    partner_id = fields.Many2one(
      string='得意先',
    )

    # Customer and related parties
    # customer_code = fields.Char(
    #     string='得意先',
    #     size=20,
    #     help='Customer code (得意先)'
    # )
    
    person_in_charge = fields.Char(
        string='担当者',
        size=20,
        help='Person in charge (担当者)'
    )
    
    delivery_destination = fields.Char(
        string='納入先',
        size=20,
        help='Delivery destination (納入先)'
    )
    
    secondary_delivery_destination = fields.Char(
        string='2次納入先',
        size=20,
        help='Secondary delivery destination (2次納入先)'
    )
    
    supplier_code = fields.Char(
        string='仕入先',
        size=20,
        help='Supplier code (仕入先)'
    )
    
    warehouse_code = fields.Char(
        string='倉庫',
        size=20,
        help='Warehouse code (倉庫)'
    )

    # Maintenance and contract fields
    maintenance_advance_category = fields.Char(
        string='保守前受区分',
        size=20,
        help='Maintenance advance category (保守前受区分)'
    )
    
    maintenance_advance_detail = fields.Char(
        string='保守前受詳細',
        size=20,
        help='Maintenance advance detail (保守前受詳細)'
    )
    
    point_back = fields.Char(string='ポイントバック')
    rental_monthly_amount = fields.Float(string='レンタル月額', digits=(16, 2))
    
    rental_start_date = fields.Date(string='レンタル開始日')
    rental_end_date = fields.Date(string='レンタル終了日')
    
    rental_months = fields.Integer(
        string='レンタル期間(月)',
        compute='_compute_rental_months',
        store=True,
        readonly=True,
        help='レンタル開始日と終了日から自動計算されます'
    )
    
    lease_cancellation_destination = fields.Char(
        string='リース解約先',
        size=20,
        help='Lease cancellation destination (リース解約先)'
    )

    # Voucher remarks
    voucher_remark_1 = fields.Char(
        string='伝票摘要①',
        size=50,
        help='Voucher remark 1 (伝票摘要①)'
    )
    
    voucher_remark_2 = fields.Char(
        string='伝票摘要②',
        size=50,
        help='Voucher remark 2 (伝票摘要②)'
    )
    
    lease_contract_number = fields.Char(
        string='リース契約番号',
        size=20,
        help='Lease contract number (リース契約番号)'
    )
    
    quantity = fields.Integer(
        string='台数',
        compute='_compute_quantity',
        store=False,
        help='Quantity (台数)'
    )
    
    transaction_approval_number = fields.Char(
        string='取引承認No.',
        size=20,
        help='Transaction approval number (取引承認No.)'
    )
    
    detail_pattern = fields.Char(
        string='明細パターン',
        size=20,
        help='Detail pattern (明細パターン)'
    )
    
    number_of_detail_patterns = fields.Integer(
        string='明細パターン数',
        store=False,
        help='Number of detail patterns (明細パターン数)'
    )    
    
    project_code = fields.Char(
        string='プロジェクト',
        size=20,
        help='Project code (プロジェクト)'
    )

    # Billing and payment
    billing_destination = fields.Char(
        string='請求先',
        size=20,
        help='Billing destination (請求先)'
    )
    
    department_in_charge = fields.Char(
        string='担当部門',
        size=20,
        help='Department in charge (担当部門)'
    )
    
    billing_information = fields.Char(
        string='請求情報',
        size=20,
        help='Billing information (請求情報)'
    )
    
    account_category_1 = fields.Char(
        string='帳端区分',
        size=20,
        help='Account category 1 (帳端区分)'
    )
    
    payment_destination = fields.Char(
        string='支払先',
        size=50,
        help='Payment destination (支払先)'
    )
    
    customer_main_number = fields.Char(
        string='得意先主文番号',
        size=30,
        help='Customer main document number (得意先主文番号)'
    )
    
    project_number = fields.Char(
        string='案件番号',
        size=30,
        help='Project number (案件番号)'
    )
    
    account_category_2 = fields.Char(
        string='帳端区分',
        size=20,
        help='Account category 2 (帳端区分)'
    )
    
    advance_department = fields.Char(
        string='前受計上部門',
        size=20,
        help='Advance accounting department (前受計上部門)'
    )

    # Rental and lease
    lease_cancellation_fee = fields.Float(
        string='リース解約金(税込)',
        digits=(12, 2),
        help='Lease cancellation fee including tax (リース解約金(税込))'
    )
    
    product_major_category = fields.Char(
        string='品種大分類',
        size=30,
        help='Product major category (品種大分類)'
    )
    
    subject = fields.Char(
        string='件名',
        size=30,
        help='Subject/Title (件名)'
    )

    # Order Totals - Sales Section (税抜売上)
    total_sales_before_tax = fields.Float(
        string='税抜売上',
        compute='_compute_order_totals',
        store=True,
        digits=(12, 2),
        help='Total sales before tax (税抜売上)'
    )
    
    total_sales_tax = fields.Float(
        string='消費税',
        compute='_compute_order_totals',
        store=True,
        digits=(12, 2),
        help='Total sales tax (消費税)'
    )
    
    total_sales_with_tax = fields.Float(
        string='合計',
        compute='_compute_order_totals',
        store=True,
        digits=(12, 2),
        help='Total sales with tax (合計)'
    )

    # Order Totals - Purchase Section (税抜仕入)
    total_purchase_before_tax = fields.Float(
        string='税抜仕入',
        default=0.0,
        digits=(12, 2),
        help='Total purchase before tax (税抜仕入) - TBD'
    )
    
    total_purchase_tax = fields.Float(
        string='消費税',
        default=0.0,
        digits=(12, 2),
        help='Total purchase tax (消費税) - TBD'
    )
    
    total_purchase_with_tax = fields.Float(
        string='合計',
        default=0.0,
        digits=(12, 2),
        help='Total purchase with tax (合計) - TBD'
    )

    # Order Totals - Cost and Profit Section
    total_cost_amount = fields.Float(
        string='原価金額',
        compute='_compute_order_totals',
        store=True,
        digits=(12, 2),
        help='Total cost amount (原価金額)'
    )
    
    total_gross_profit = fields.Float(
        string='粗利',
        compute='_compute_order_totals',
        store=True,
        digits=(12, 2),
        help='Total gross profit (粗利)'
    )
    
    maintenance_advance = fields.Float(
        string='保守前受',
        default=0.0,
        digits=(12, 2),
        help='Maintenance advance (保守前受) - TBD'
    )
    
    maintenance_advance_tax = fields.Float(
        string='保守前受消費税',
        compute='_compute_maintenance_tax',
        store=True,
        digits=(12, 2),
        help='Maintenance advance tax = 10% × 保守前受'
    )

    @api.depends('order_line.obic_sales_amount', 'order_line.obic_sales_tax', 
                 'order_line.obic_cost_amount', 'order_line.obic_gross_profit')
    def _compute_order_totals(self):
        """Calculate order totals from lines"""
        for order in self:
            order.total_sales_before_tax = sum(order.order_line.mapped('obic_sales_amount'))
            order.total_sales_tax = sum(order.order_line.mapped('obic_sales_tax'))
            order.total_sales_with_tax = order.total_sales_before_tax + order.total_sales_tax
            order.total_cost_amount = sum(order.order_line.mapped('obic_cost_amount'))
            order.total_gross_profit = sum(order.order_line.mapped('obic_gross_profit'))

    @api.depends('maintenance_advance')
    def _compute_maintenance_tax(self):
        """Calculate maintenance advance tax (10%)"""
        for order in self:
            order.maintenance_advance_tax = order.maintenance_advance * 0.10

    @api.depends()
    def _compute_base_date(self):
        """Compute base date as today's date"""
        today = fields.Date.context_today(self)
        for record in self:
            record.base_date = today

    @api.depends()
    def _compute_quantity(self):
        """Hardcoded quantity as 1 for now"""
        for record in self:
            record.quantity = 1

    @api.depends('rental_start_date', 'rental_end_date')
    def _compute_rental_months(self):
        """レンタル期間（月数）を開始日と終了日から計算"""
        for record in self:
            if record.rental_start_date and record.rental_end_date:
                if record.rental_end_date < record.rental_start_date:
                    record.rental_months = 0
                else:
                    start = record.rental_start_date
                    end = record.rental_end_date
                    months = (end.year - start.year) * 12 + (end.month - start.month)
                    if end.day >= start.day:
                        months += 1
                    record.rental_months = months
            else:
                record.rental_months = 0

    @api.constrains('order_number')
    def _check_order_number(self):
        """Validate order number is unique"""
        for record in self:
            if record.order_number:
                existing = self.search([
                    ('order_number', '=', record.order_number),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError(_('受注番号 %s は既に存在します。') % record.order_number)

    # Header Action Methods
    def action_new_line(self):
        """行新規 - Tạo dòng mới"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('行新規'),
                'message': _('新しい行を追加します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_delete_line(self):
        """行削除 - Xóa dòng"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('行削除'),
                'message': _('選択した行を削除します（開発中）'),
                'type': 'warning',
                'sticky': False,
            }
        }

    def action_search(self):
        """検索 - Tìm kiếm"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('検索'),
                'message': _('検索機能は開発中です'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_cancel(self):
        """取消 - Hủy bỏ"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('取消'),
                'message': _('操作をキャンセルします'),
                'type': 'warning',
                'sticky': False,
            }
        }

    def action_edit_line(self):
        """行編集 - Sửa dòng"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('行編集'),
                'message': _('行の編集機能は開発中です'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_copy_line(self):
        """行複写 - Copy dòng"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('行複写'),
                'message': _('行を複写します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_register(self):
        """登録 - Đăng ký (Save)"""
        self.ensure_one()
        try:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('登録'),
                    'message': _('保存されました'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            _logger.error('Error in action_register: %s', str(e))
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('エラー'),
                    'message': str(e),
                    'type': 'danger',
                    'sticky': True,
                }
            }

    def action_content_confirmation(self):
        """內容確認 - Xác nhận nội dung"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('內容確認'),
                'message': _('內容確認機能は開発中です'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_close(self):
        """閉じる - Đóng form"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('閉じる'),
                'message': _('フォームを閉じます'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_show_customer_detail(self):
        """Show customer detail modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('得意先詳細'),
                'message': _('得意先の詳細情報を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }
        
    def action_show_billing_information(self):
        """Show billing information modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('請求情報詳細'),
                'message': _('請求情報の詳細を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_show_delivery_detail(self):
        """Show delivery destination detail modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('納入先詳細'),
                'message': _('納入先の詳細情報を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }
    
    def action_show_related_partners(self):     
        """Show related partners modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('関連取引先'),
                'message': _('関連取引先情報を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }
        
    def action_show_secondary_delivery_detail(self):
        """Show secondary delivery destination detail modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('2次納入先詳細'),
                'message': _('2次納入先の詳細情報を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_show_supplier_detail(self):
        """Show supplier detail modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('仕入先詳細'),
                'message': _('仕入先の詳細情報を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_show_payment_info(self):
        """Show payment information modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('支払情報'),
                'message': _('支払情報を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_show_contract_detail(self):
        """Show contract detail modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('契約詳細'),
                'message': _('契約詳細を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_show_analysis(self):
        """Show analysis modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('分析集計'),
                'message': _('分析集計を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_reacquire_unit_price(self):
        """Show unit price reacquisition modal (placeholder)"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('単価再取得'),
                'message': _('単価再取得を表示します（開発中）'),
                'type': 'info',
                'sticky': False,
            }
        }
        
    def action_preview_new_template(self):
          """Mở template PDF mới khi nhấn vào button Preview New"""
          self.ensure_one()
          # Use a public controller URL to render/download the PDF so we don't depend on the report external id
          custom_preview_url = f'/my/orders/{self.id}/download_new_template'
          if self.access_token:
              custom_preview_url += f'?access_token={self.access_token}'
          return {
              'type': 'ir.actions.act_url', 
              'target': 'self',
              'url': custom_preview_url,
          }
