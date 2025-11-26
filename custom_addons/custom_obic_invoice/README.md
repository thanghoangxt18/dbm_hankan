# OBIC Invoice Module - Installation Guide

## 📦 Module Information
- **Name**: custom_obic_invoice
- **Version**: 1.0.0
- **Category**: Accounting
- **Odoo Version**: 18.0
- **Dependencies**: account, product, custom_obic_denpyou

## 🎯 Module Overview

Module này extend `account.move` để thêm chức năng 請求管理 (Invoice Management) của OBIC với 2 modes:

### Mode 1: 伝票単位 (Denpyou-based)
- Hiển thị lines dưới dạng **SECTION/CARD** (giống custom_obic_sale_order)
- Mỗi card có 2 rows với thông tin từ 伝票
- Auto-fill từ module custom_obic_denpyou
- Bulk operations: 一括請求/一括解除

### Mode 2: 明細単位 (Meisai-based)
- Hiển thị lines dưới dạng **TABLE 11 cột** (giống custom_obic_denpyou)
- Không có thead, labels inline trong tbody
- Auto-calculation: 今回請求額 = 明細金額 × 数量
- Bulk operations: 一括請求/一括解除

## 🚀 Installation Steps

### 1. Prerequisites
```bash
# CRITICAL: Phải cài custom_obic_denpyou trước
# Module này depend vào custom_obic_denpyou
```

### 2. Install Module
```bash
# Trong Docker container
docker compose exec web python3 odoo-bin -c /etc/odoo/odoo.conf \
  -i custom_obic_invoice -d dbm_hankan \
  --db_host=db --db_user=odoo --db_password=myodoo \
  --stop-after-init
```

### 3. Verify Installation
1. Menu "OBIC請求" xuất hiện ở top menu
2. Click "請求管理" để mở list view
3. Tạo invoice mới để test 2 modes

## 📋 Module Structure

```
custom_obic_invoice/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── obic_invoice.py                    # Extend account.move
│   ├── obic_invoice_denpyou_line.py       # Denpyou lines
│   └── obic_invoice_meisai_line.py        # Meisai lines
├── views/
│   ├── obic_invoice_views.xml             # Form/List/Search views
│   └── menu_views.xml                     # Menu structure
├── security/
│   └── ir.model.access.csv
└── static/src/fields/
    ├── obic_invoice_denpyou_line_field/   # Widget 1: SECTION format
    │   ├── obic_invoice_denpyou_line_field.js
    │   ├── obic_invoice_denpyou_line_field.xml
    │   └── obic_invoice_denpyou_line_field.scss
    └── obic_invoice_meisai_line_field/    # Widget 2: TABLE format
        ├── obic_invoice_meisai_line_field.js
        ├── obic_invoice_meisai_line_field.xml
        └── obic_invoice_meisai_line_field.scss
```

## 🎯 Key Features

### Extended account.move Fields

**Basic Fields:**
- 請求番号 (invoice_number)
- 基準日 (reference_date)
- 前回入力番号 (previous_input_number)
- 事業所 (business_office)
- 請求先 (billing_destination)
- 請求日 (invoice_date_custom)
- 回収予定日 (collection_date)
- 請求単位 (invoice_unit) - Radio: 伝票単位/明細単位
- 請求件名 (invoice_subject)
- 伝票摘要 (denpyou_summary)
- 部門 (department)

**抽出条件 (Search Criteria) Fields:**
- 部門グループ1 (department_group_1)
- 計上部門 (accounting_department)
- 得意先 (customer)
- 担当者 (person_in_charge)
- 売上日 (sales_date)
- 売上番号 (sales_number)
- オペレータ (operator)
- 変更日 (change_date)

**Other Fields:**
- 消費税調整金額 (tax_adjustment_amount)
- Button: 調整明細入力 (placeholder notification)

### Model 1: obic.invoice.denpyou.line (伝票単位 Mode)

**UI Format:** SECTION/CARD với 2 rows

**Fields:**
- denpyou_id → obic.denpyou (Required, trigger onchange)
- customer_code (auto-filled, editable)
- denpyou_date
- collection_date
- denpyou_amount (auto-filled, editable)
- current_billing_amount (auto-filled, editable)
- person_in_charge
- denpyou_summary (auto-filled, editable)
- is_billing_target (Boolean)

**Auto-fill Logic:**
```python
@api.onchange('denpyou_id')
def _onchange_denpyou_id(self):
    # Chọn 伝票 → auto-fill từ custom_obic_denpyou
    self.customer_code = self.denpyou_id.customer_code
    self.denpyou_amount = self.denpyou_id.total_current_billing_amount
    self.current_billing_amount = self.denpyou_id.total_current_billing_amount
    self.denpyou_summary = self.denpyou_id.denpyou_summary
```

### Model 2: obic.invoice.meisai.line (明細単位 Mode)

**UI Format:** TABLE với 11 cột, no thead, labels inline

**Fields:**
- product_id (Required, trigger onchange)
- detail_amount (auto-filled, editable)
- quantity (Default: 1)
- current_billing_amount (Computed, editable)
- is_billing (Boolean)

**Auto-calculation:**
```python
@api.depends('detail_amount', 'quantity')
def _compute_current_billing_amount(self):
    line.current_billing_amount = line.detail_amount * line.quantity

@api.onchange('product_id')
def _onchange_product_id(self):
    # Chọn product → auto-fill detail_amount
    self.detail_amount = self.product_id.list_price
```

### Bulk Operations

**伝票単位 Mode:**
- `action_set_all_denpyou_billing_true()` - Set tất cả is_billing_target = True
- `action_set_all_denpyou_billing_false()` - Set tất cả is_billing_target = False

**明細単位 Mode:**
- `action_set_all_meisai_billing_true()` - Set tất cả is_billing = True
- `action_set_all_meisai_billing_false()` - Set tất cả is_billing = False

### Computed Totals

```python
# 伝票単位 mode
total_current_billing_amount_denpyou = sum(invoice_denpyou_line_ids.current_billing_amount)

# 明細単位 mode
total_current_billing_amount_meisai = sum(invoice_meisai_line_ids.current_billing_amount)
```

## 🧪 Testing Checklist

### Basic Tests
- [ ] Module install thành công (check dependency custom_obic_denpyou)
- [ ] Extend account.move thành công
- [ ] Menu "OBIC請求" > "請求管理" hiển thị
- [ ] Tạo được Invoice mới
- [ ] Radio button 請求単位 hoạt động
- [ ] Switch giữa 2 modes show/hide đúng pages

### Mode 伝票単位 Tests (SECTION Format)
- [ ] Thêm được 伝票 line qua button "伝票明細を追加"
- [ ] Chọn 伝票 → auto-fill: customer_code, denpyou_amount, current_billing_amount, denpyou_summary
- [ ] Section/card hiển thị đúng với 2 rows:
  - Row 1: 伝票番号 | 伝票日付 | 回収予定日 | 伝票金額 | 今回請求額 | 請求対象
  - Row 2: 得意先 | 担当者 | 伝票摘要
- [ ] Edit line mở dialog và save thành công
- [ ] Delete line hiển thị confirm và xóa thành công
- [ ] Button 一括請求: Set tất cả is_billing_target = True
- [ ] Button 一括解除: Set tất cả is_billing_target = False
- [ ] 今回請求額合計 tính đúng = sum của các lines

### Mode 明細単位 Tests (TABLE Format)
- [ ] Thêm được product line qua button "明細を追加"
- [ ] Chọn product → auto-fill 明細金額 từ list_price
- [ ] Table hiển thị đúng (11 cột, NO thead):
  - Col 1-2: 行番号 label + Index
  - Col 3-4: 商品名 label + Product
  - Col 5-6: 明細金額 label + Amount
  - Col 7-8: 今回請求額 label + Billing amount
  - Col 9-10: 請求 label + Checkbox
  - Col 11: Edit/Delete buttons
- [ ] Edit line mở dialog và save thành công
- [ ] Delete line hiển thị confirm và xóa thành công
- [ ] 今回請求額 auto-compute = 明細金額 × 数量
- [ ] Button 一括請求: Set tất cả is_billing = True
- [ ] Button 一括解除: Set tất cả is_billing = False
- [ ] 今回請求額合計 tính đúng = sum của các lines

### Integration Tests
- [ ] Có thể reference 伝票 từ custom_obic_denpyou
- [ ] Data từ 伝票 sync đúng vào denpyou line
- [ ] Button 調整明細入力 show notification "この機能は開発中です"
- [ ] Drag-drop reorder lines (sequence field)

## 🐛 Debugging Tips

### Debug Point 1: Extend account.move không hoạt động
```python
# Check trong Python shell
invoice = self.env['account.move'].search([], limit=1)
print(hasattr(invoice, 'invoice_unit'))  # Should be True
print(hasattr(invoice, 'invoice_denpyou_line_ids'))  # Should be True
```

### Debug Point 2: Conditional pages không show/hide
```xml
<!-- Kiểm tra syntax invisible -->
<page invisible="invoice_unit != 'denpyou'">  <!-- ✅ ĐÚNG -->
<page attrs="{'invisible': ...}">  <!-- ❌ SAI (Odoo 18) -->
```

### Debug Point 3: Onchange không trigger
```python
# Thêm logging vào _onchange_denpyou_id
@api.onchange('denpyou_id')
def _onchange_denpyou_id(self):
    _logger.info(f'Denpyou selected: {self.denpyou_id.denpyou_number}')
    if self.denpyou_id:
        _logger.info(f'Auto-filling: {self.denpyou_id.total_current_billing_amount}')
```

Check logs:
```bash
docker compose logs -f web | grep "Denpyou selected"
```

### Debug Point 4: Widget không render
```javascript
// Trong browser console
console.log('Denpyou widget:', 
  odoo.__DEBUG__.services['@web/core/registry']
    .category('fields').content.obic_invoice_denpyou_line_one2many
);

console.log('Meisai widget:', 
  odoo.__DEBUG__.services['@web/core/registry']
    .category('fields').content.obic_invoice_meisai_line_one2many
);
```

Check assets loaded:
- F12 → Network → JS files
- Search for: obic_invoice_denpyou_line_field.js
- Search for: obic_invoice_meisai_line_field.js

### Debug Point 5: Tổng không tính đúng
```python
@api.depends('invoice_denpyou_line_ids.current_billing_amount')
def _compute_total_denpyou(self):
    for record in self:
        amounts = record.invoice_denpyou_line_ids.mapped('current_billing_amount')
        _logger.info(f'Amounts: {amounts}')
        record.total_current_billing_amount_denpyou = sum(amounts)
        _logger.info(f'Total: {record.total_current_billing_amount_denpyou}')
```

## 📚 Reference Files

### Denpyou Lines Widget (SECTION format)
Copied and adapted from:
- `custom_obic_sale_order/static/src/fields/obic_sale_order_line_field/`

Key changes:
- 4 rows → 2 rows
- Sale order fields → Denpyou fields
- Registry name: obic_invoice_denpyou_line_one2many

### Meisai Lines Widget (TABLE format)
Copied and adapted from:
- `custom_obic_denpyou/static/src/fields/obic_denpyou_line_field/`

Key changes:
- Model: obic.denpyou.line → obic.invoice.meisai.line
- Field names adjusted
- Registry name: obic_invoice_meisai_line_one2many

## ⚠️ Common Issues

### Issue 1: "Module custom_obic_denpyou not found"
**Solution:** Install custom_obic_denpyou first
```bash
docker compose exec web python3 odoo-bin -c /etc/odoo/odoo.conf \
  -i custom_obic_denpyou -d dbm_hankan --stop-after-init
```

### Issue 2: Widget không hiển thị
**Solution:** 
- Clear browser cache (Ctrl+F5)
- Restart Odoo: `docker compose restart web`
- Check JS console for errors

### Issue 3: Access rights error
**Solution:** 
- Update module: `-u custom_obic_invoice`
- Check ir.model.access.csv có đúng format

### Issue 4: 伝票 không chọn được
**Solution:**
- Kiểm tra custom_obic_denpyou đã cài chưa
- Tạo test data trong module custom_obic_denpyou trước

## 📝 Technical Notes

### About Extending account.move
```python
# ✅ ĐÚNG - Extend existing model
class ObicInvoice(models.Model):
    _inherit = 'account.move'
    invoice_unit = fields.Selection(...)

# ❌ SAI - Tạo model mới
class ObicInvoice(models.Model):
    _name = 'obic.invoice'  # WRONG!
```

### About Conditional Visibility
```xml
<!-- ✅ ĐÚNG - Odoo 18 -->
<page invisible="invoice_unit != 'denpyou'">

<!-- ❌ SAI - Old syntax -->
<page attrs="{'invisible': [('invoice_unit', '!=', 'denpyou')]}">
```

### About Widget Registration
```javascript
// Widget 1: Denpyou lines (SECTION)
registry.category("fields").add("obic_invoice_denpyou_line_one2many", ...);

// Widget 2: Meisai lines (TABLE)
registry.category("fields").add("obic_invoice_meisai_line_one2many", ...);
```

## 🎯 Success Criteria

Module thành công khi:
- ✅ Extend account.move không lỗi
- ✅ 2 modes UI hoạt động độc lập
- ✅ Switch mode show/hide đúng pages
- ✅ Có thể chọn 伝票 từ custom_obic_denpyou
- ✅ Auto-fill từ 伝票 hoạt động
- ✅ Cả 2 widgets render đúng (section + table)
- ✅ All buttons hoạt động (add, edit, delete, bulk)
- ✅ Tổng tính đúng cho cả 2 modes
- ✅ Confirmation dialog hiển thị khi delete

## 📞 Support

For issues:
- Check logs: `docker compose logs -f web`
- Review Odoo logs: Settings > Technical > Logging
- Check browser console for JS errors
