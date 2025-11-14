# Sale Order Line Manager - OWL Component Implementation

## Tổng quan
Module này đã được cập nhật để thay thế list editable view của sale order lines bằng OWL components với modal và sections.

## Cấu trúc Files

```
custom_addons/custom_obic_sale_order/
├── static/src/components/
│   ├── line_modal/
│   │   ├── line_modal.js          # Modal component để thêm/sửa line
│   │   └── line_modal.xml         # Template cho modal
│   ├── line_section/
│   │   ├── line_section.js        # Component hiển thị một line dưới dạng card
│   │   └── line_section.xml       # Template cho section
│   └── sale_order_line_manager/
│       ├── sale_order_line_manager.js    # Main widget quản lý lines
│       ├── sale_order_line_manager.xml   # Template chính
│       └── sale_order_line_manager.scss  # Styles
├── views/
│   └── sale_order_views.xml       # Updated để dùng widget mới
└── __manifest__.py                # Updated assets

## Tính năng

### 1. LineModal Component
- **Mục đích**: Modal để thêm mới hoặc chỉnh sửa sale order line
- **Props**:
  - `lineData`: Dữ liệu line (rỗng nếu tạo mới)
  - `mode`: 'create' hoặc 'edit'
  - `productList`: Danh sách products
  - `onSave`, `onCancel`: Callbacks
  
- **Features**:
  - Auto-fill prices khi chọn product
  - Auto-calculate sales amount và tax
  - Auto-calculate gross profit
  - Validation trước khi save
  - Responsive layout 4 rows

### 2. LineSection Component
- **Mục đích**: Hiển thị một line dưới dạng readonly card
- **Props**:
  - `lineData`: Dữ liệu line
  - `index`: Vị trí trong list
  - `onEdit`, `onDelete`: Callbacks

- **Features**:
  - Card layout đẹp mắt với borders
  - Hiển thị đầy đủ thông tin theo 4 rows
  - Buttons Edit và Delete
  - Hover effects
  - Color coding cho các giá trị quan trọng

### 3. SaleOrderLineManager Component
- **Mục đích**: Main widget quản lý toàn bộ lines
- **Features**:
  - Hiển thị danh sách lines dưới dạng sections
  - Button "明細を追加" để thêm line mới
  - Summary section hiển thị tổng
  - Auto-sync với backend
  - Handle create/update/delete operations

## Logic Business

### Computed Fields
Các computed fields được tính tự động:

1. **obic_sales_amount**:
   ```
   sales_amount = sales_unit_price × quantity
   ```

2. **obic_sales_tax**:
   ```
   sales_tax = sales_amount × 0.10 (nếu is_tax_excluded = true)
   ```

3. **obic_gross_profit**:
   ```
   gross_profit = sales_amount - cost_amount
   ```

### Onchange Events

1. **onProductChange**: Khi chọn product
   - Auto-fill `obic_list_unit_price` và `obic_sales_unit_price`
   - Trigger recalculate

2. **onPriceOrDiscountChange**: Khi thay đổi list price hoặc discount
   ```
   sales_unit_price = list_unit_price × (discount_rate / 100)
   ```
   - Trigger recalculate

3. **onTaxExcludedChange**: Khi thay đổi checkbox tax excluded
   - Recalculate tax amount

### Data Sync với Backend

Widget sử dụng Odoo ORM commands để sync:

- **Create**: `[0, 0, values]`
- **Update**: `[1, id, values]`
- **Delete**: `[2, id]`

## Hướng dẫn Sử dụng

### Cho End Users

1. **Thêm Line Mới**:
   - Click button "明細を追加"
   - Điền thông tin trong modal
   - Click "保存"

2. **Chỉnh Sửa Line**:
   - Click button "編集" trên card của line
   - Sửa thông tin trong modal
   - Click "保存"

3. **Xóa Line**:
   - Click button "削除" trên card
   - Confirm trong dialog

### Cho Developers

#### Modify Modal Layout
Edit file: `static/src/components/line_modal/line_modal.xml`

#### Modify Section Display
Edit file: `static/src/components/line_section/line_section.xml`

#### Add New Fields
1. Thêm field vào modal template
2. Thêm field vào state trong `line_modal.js`
3. Update `onSave` method để include field mới
4. Thêm hiển thị trong `line_section.xml`

#### Customize Styles
Edit file: `static/src/components/sale_order_line_manager/sale_order_line_manager.scss`

## Testing

### Test Cases

1. **Create New Line**:
   - ✓ Modal mở ra với form trống
   - ✓ Product selection hoạt động
   - ✓ Auto-calculate prices
   - ✓ Validation hoạt động
   - ✓ Save thành công và line xuất hiện

2. **Edit Existing Line**:
   - ✓ Modal mở ra với data có sẵn
   - ✓ Có thể modify các fields
   - ✓ Save update thành công

3. **Delete Line**:
   - ✓ Confirm dialog xuất hiện
   - ✓ Line bị xóa sau khi confirm

4. **Computed Fields**:
   - ✓ Sales amount tính đúng
   - ✓ Tax tính đúng
   - ✓ Gross profit tính đúng

5. **Summary**:
   - ✓ Tổng sales amount đúng
   - ✓ Tổng tax đúng
   - ✓ Tổng including tax đúng

## Troubleshooting

### Modal không mở
- Check console cho errors
- Verify assets đã được load
- Check Dialog service available

### Data không save
- Check ORM service đang hoạt động
- Verify record có update permission
- Check field names match với Python model

### Computed fields không update
- Verify event handlers được bind đúng
- Check calculation logic trong JS
- Ensure state updates trigger re-render

### Styling không apply
- Clear browser cache
- Restart Odoo với --dev=all
- Check SCSS compilation

## Performance Considerations

1. **Product List Loading**:
   - Hiện tại limit 1000 products
   - Có thể tăng hoặc implement search on-demand

2. **Lines Rendering**:
   - Container có max-height với scroll
   - Mỗi line là một component riêng

3. **State Management**:
   - State được manage bởi OWL reactive system
   - Tránh deep nesting trong state

## Future Enhancements

1. **Search Products**: Thêm search box thay vì dropdown
2. **Bulk Operations**: Select multiple lines để delete
3. **Drag & Drop**: Reorder lines bằng drag-drop
4. **Templates**: Save line templates để reuse
5. **Import/Export**: Import lines từ CSV/Excel
6. **Duplicate Line**: Clone existing line
7. **Line Notes**: Thêm rich text editor cho remarks

## Maintenance Notes

- OWL version: Odoo 18
- All components follow Odoo 18 best practices
- Code có comments tiếng Việt để dễ maintain
- Tuân thủ existing business logic từ Python models
