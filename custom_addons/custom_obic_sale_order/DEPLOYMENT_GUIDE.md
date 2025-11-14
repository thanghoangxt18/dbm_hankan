# Hướng dẫn Deploy Sale Order Line Manager

## Các bước thực hiện

### 1. Backup hiện tại (Khuyến nghị)
```bash
cd /home/thanghoang/programming/hankan/dbm_hankan/odoo
# Backup database
docker compose exec db pg_dump -U odoo odoo > backup_before_linemanager_$(date +%Y%m%d).sql
```

### 2. Verify cấu trúc files
Đảm bảo các files sau đã được tạo đúng:

```bash
custom_addons/custom_obic_sale_order/
├── static/src/components/
│   ├── line_modal/
│   │   ├── line_modal.js
│   │   └── line_modal.xml
│   ├── line_section/
│   │   ├── line_section.js
│   │   └── line_section.xml
│   └── sale_order_line_manager/
│       ├── sale_order_line_manager.js
│       ├── sale_order_line_manager.xml
│       └── sale_order_line_manager.scss
├── views/
│   └── sale_order_views.xml (đã update)
├── __manifest__.py (đã update assets)
└── README_LINE_MANAGER.md
```

### 3. Restart Odoo
```bash
cd /home/thanghoang/programming/hankan/dbm_hankan/odoo
docker compose restart web
```

### 4. Update Module trong Odoo

#### Option A: Qua UI (Recommended)
1. Login vào Odoo
2. Bật Developer Mode:
   - Settings → Activate Developer Mode
3. Vào Apps
4. Remove filter "Apps" trong search bar
5. Search "Custom OBIC Sale Order"
6. Click button "Upgrade"

#### Option B: Qua Command Line
```bash
docker compose exec web odoo -u custom_obic_sale_order -d odoo --stop-after-init
docker compose restart web
```

### 5. Clear Browser Cache
- Chrome: Ctrl + Shift + Delete
- Firefox: Ctrl + Shift + Delete
- Hoặc dùng Incognito/Private mode

### 6. Verify Installation

#### Check Assets Loaded
1. Mở Chrome DevTools (F12)
2. Vào tab Network
3. Filter: JS
4. Reload page
5. Verify các files sau được load:
   - `line_modal.js`
   - `line_section.js`
   - `sale_order_line_manager.js`
   - `sale_order_line_manager.scss` (compiled to CSS)

#### Check Widget Registered
1. Mở Console trong DevTools
2. Gõ:
   ```javascript
   odoo.__DEBUG__.services['@web/core/registry'].category('fields').content
   ```
3. Tìm `sale_order_line_widget` trong list

#### Test Functionality
1. Vào Sales → Orders
2. Vào OBIC受注 → 受注管理
3. Tạo hoặc mở một Sale Order
4. Scroll xuống phần "受注明細"
5. Kiểm tra:
   - ✓ Hiển thị button "明細を追加"
   - ✓ Existing lines hiển thị dưới dạng cards
   - ✓ Click "明細を追加" mở modal
   - ✓ Có thể thêm line mới
   - ✓ Có thể edit line
   - ✓ Có thể delete line
   - ✓ Summary hiển thị đúng

## Troubleshooting

### Lỗi: "Cannot add key ... in the views registry"
**Nguyên nhân**: Conflict với existing widget
**Giải pháp**: 
1. Clear browser cache hoàn toàn
2. Restart Odoo
3. Nếu vẫn lỗi, check có module nào khác đăng ký cùng tên

### Lỗi: Modal không mở
**Nguyên nhân**: Dialog service không available
**Giải pháp**:
1. Check console có error không
2. Verify `@web/core/dialog/dialog` được import đúng
3. Check OWL version compatibility

### Lỗi: Fields không save
**Nguyên nhân**: Field names không match model
**Giải pháp**:
1. Check Python model có đủ fields không
2. Verify field names trong JS match với Python
3. Check user có quyền write không

### Lỗi: Styles không apply
**Nguyên nhân**: SCSS chưa compile
**Giải pháp**:
```bash
# Restart với assets rebuild
docker compose restart web
# Trong Odoo, vào Settings → Technical → Views → Clear assets cache
```

### Lỗi: "Cannot read property 'order_line'"
**Nguyên nhân**: Record chưa load đủ data
**Giải pháp**:
1. Check `onWillStart` hook
2. Add defensive checks trong code
3. Ensure record.data.order_line exists

## Performance Tuning

### Nếu có nhiều products (>1000)
Edit `sale_order_line_manager.js`:
```javascript
async loadProducts() {
    // Thay vì load tất cả, implement search
    // Hoặc tăng limit
    const products = await this.orm.searchRead(
        "product.product",
        [],
        ["id", "name", "list_price"],
        { limit: 5000 }  // Tăng limit
    );
    this.state.productList = products;
}
```

### Nếu lines render chậm
Edit `sale_order_line_manager.scss`:
```scss
.order-lines-container {
    max-height: 400px;  // Giảm height
    // Enable virtual scrolling nếu cần
}
```

## Rollback Plan

Nếu cần rollback về list editable cũ:

### 1. Restore view XML
Edit `views/sale_order_views.xml`, replace:
```xml
<field name="order_line" widget="sale_order_line_widget" nolabel="1"/>
```
Với old code (có backup trong git)

### 2. Comment out assets trong manifest
```python
'assets': {
    'web.assets_backend': [
        'custom_obic_sale_order/static/src/css/obic_order.css',
        'custom_obic_sale_order/static/src/js/obic_order_form.js',
        # Comment out new components
        # 'custom_obic_sale_order/static/src/components/...',
    ],
},
```

### 3. Upgrade module lại
```bash
docker compose exec web odoo -u custom_obic_sale_order -d odoo --stop-after-init
docker compose restart web
```

## Monitoring

### Check logs khi có issue
```bash
# Real-time logs
docker compose logs -f web

# Grep specific errors
docker compose logs web | grep -i "error\|exception"
```

### Check JS errors
1. Mở Chrome DevTools Console
2. Look for red errors
3. Check Network tab cho failed requests

## Next Steps

1. ✓ Deploy to development
2. ⏳ Test thoroughly với real data
3. ⏳ Train users
4. ⏳ Deploy to staging
5. ⏳ User acceptance testing
6. ⏳ Deploy to production

## Support

Nếu gặp vấn đề:
1. Check README_LINE_MANAGER.md
2. Review code comments
3. Check Odoo logs
4. Search Odoo forums
5. Contact developer
