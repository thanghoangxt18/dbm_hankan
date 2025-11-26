# OBIC Denpyou Module - Installation Guide

## 📦 Module Information
- **Name**: custom_obic_denpyou
- **Version**: 1.0.0
- **Category**: Sales
- **Odoo Version**: 18.0

## 🚀 Installation Steps

### 1. Copy Module to Addons Directory
```bash
# Module đã được tạo tại:
/home/thanghoang/programming/hankan/dbm_hankan/odoo/custom_addons/custom_obic_denpyou
```

### 2. Update Module List
```bash
# Trong Docker container
docker compose exec web python3 odoo-bin -c /etc/odoo/odoo.conf \
  --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons \
  -u all -d dbm_hankan --stop-after-init
```

Hoặc từ Odoo UI:
1. Settings > Apps > Update Apps List
2. Remove "Apps" filter
3. Search "custom_obic_denpyou"
4. Click "Install"

### 3. Verify Installation
1. Menu "OBIC伝票" xuất hiện ở top menu
2. Click "伝票管理" để mở list view
3. Tạo 伝票 mới để test

## 📋 Module Structure

```
custom_obic_denpyou/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── obic_denpyou.py          # Main model (伝票)
│   └── obic_denpyou_line.py     # Line model (明細)
├── views/
│   ├── obic_denpyou_views.xml   # Form, List, Search views
│   └── menu_views.xml           # Menu definitions
├── security/
│   └── ir.model.access.csv      # Access rights
└── static/src/
    └── fields/
        └── obic_denpyou_line_field/
            ├── obic_denpyou_line_field.js    # Custom widget JS
            ├── obic_denpyou_line_field.xml   # Widget templates
            └── obic_denpyou_line_field.scss  # Styling
```

## 🎯 Key Features

### 1. Main Model (obic.denpyou)
- **伝票番号** (denpyou_number): Unique voucher number
- **得意先** (customer_code): Customer code
- **納入先** (delivery_destination): Delivery destination
- **伝票摘要** (denpyou_summary): Voucher summary
- **件名** (subject): Subject
- **明細** (line_ids): One2many to lines
- **今回請求額合計** (total_current_billing_amount): Computed total

### 2. Line Model (obic.denpyou.line)
- **商品名** (product_id): Product selection
- **明細金額** (detail_amount): Detail amount (auto-filled from product.list_price)
- **数量** (quantity): Quantity
- **今回請求額** (current_billing_amount): Computed = detail_amount × quantity
- **請求** (is_billing): Billing flag

### 3. Custom Widget Features
- ✅ Table format với inline labels (11 columns per row)
- ✅ KHÔNG có thead (hidden completely)
- ✅ Edit/Delete buttons cho mỗi line
- ✅ Add button "明細を追加"
- ✅ Dialog form khi add/edit
- ✅ Auto-calculation of amounts

### 4. Bulk Operations
- **一括請求** (action_set_all_billing_true): Set all lines' is_billing = True
- **一括解除** (action_set_all_billing_false): Set all lines' is_billing = False

## 🧪 Testing Checklist

After installation, test these features:

- [ ] Module install thành công không lỗi
- [ ] Menu "OBIC伝票" > "伝票管理" hiển thị
- [ ] Tạo được 伝票 mới
- [ ] Thêm được 明細 qua button "明細を追加"
- [ ] Table hiển thị KHÔNG có thead
- [ ] Table có đủ 11 cột với labels inline:
  - [ ] 行番号 + Index
  - [ ] 商品名 + Product name
  - [ ] 明細金額 + Amount
  - [ ] 今回請求額 + Billing amount
  - [ ] 請求 + Checkbox
  - [ ] Edit/Delete buttons
- [ ] Edit line mở dialog và save thành công
- [ ] Delete line hiển thị confirm và xóa thành công
- [ ] Chọn product auto-fill 明細金額 từ list_price
- [ ] 今回請求額 tự động = 明細金額 × 数量
- [ ] 今回請求額合計 tính đúng = sum của các lines
- [ ] Nút "一括請求" set tất cả checkbox = True
- [ ] Nút "一括解除" set tất cả checkbox = False
- [ ] Drag-drop reorder lines (sequence field)

## 🐛 Debugging Tips

### Debug Point 1: Table không hiển thị đúng format
```javascript
// Thêm vào obic_denpyou_line_field.js
console.log('RecordRow rendering:', record.data);
```

### Debug Point 2: Data không save
```javascript
// Check trong setup()
console.log('X2Many setup completed');
console.log('saveRecord available:', !!saveRecord);
```

### Debug Point 3: Computed field không update
```python
# Thêm vào _compute_current_billing_amount
_logger.info(f'Computing: {line.detail_amount} × {line.quantity}')
```

### Debug Point 4: Bulk actions không hoạt động
```python
# Thêm vào action_set_all_billing_true
_logger.info(f'Setting billing for {len(self.line_ids)} lines')
```

## 🔧 Known Issues & Solutions

### Issue 1: Module không xuất hiện trong Apps list
**Solution**: 
- Update apps list: Settings > Apps > Update Apps List
- Remove "Apps" filter
- Search by technical name: "custom_obic_denpyou"

### Issue 2: Access rights error
**Solution**: 
- Check ir.model.access.csv có đúng format
- Restart Odoo sau khi install

### Issue 3: Widget không render
**Solution**:
- Clear browser cache (Ctrl+F5)
- Check console for JS errors
- Verify assets được load: Developer Tools > Network

## 📝 Notes

- UI toàn tiếng Nhật
- Field names trong DB tiếng Anh có ý nghĩa
- Code có comments tiếng Việt
- Follow Odoo 18 best practices
- Kế thừa X2ManyField (KHÔNG viết lại từ đầu)

## 📞 Support

For issues or questions:
- Check logs: `docker compose logs -f web`
- Review Odoo logs in UI: Settings > Technical > Logging
