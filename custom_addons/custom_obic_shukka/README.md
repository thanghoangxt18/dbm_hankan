# OBIC Shukka Management Module (出荷管理)

## 📋 Mô tả
Module quản lý giao hàng cho hệ thống ERP Odoo 18, được phát triển cho khách hàng Nhật Bản.

## 🏗️ Cấu trúc Module

```
custom_obic_shukka/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── obic_shukka.py          # Model chính (obic.shukka)
│   └── obic_shukka_line.py     # Model chi tiết (obic.shukka.line)
├── views/
│   ├── obic_shukka_views.xml   # Form, List, Search views
│   └── menu_views.xml          # Menu structure
├── security/
│   └── ir.model.access.csv     # Access rights
└── static/src/fields/
    └── obic_shukka_line_field/ # Widget one2many sections
        ├── obic_shukka_line_field.js
        ├── obic_shukka_line_field.xml
        └── obic_shukka_line_field.scss
```

## 🎯 Tính năng chính

### 1. Form nhập liệu gồm 4 phần:

#### **PHẦN 1: TOP (2 cột 4-1)**
- **Bên trái:**
  - 出荷処理番号 (Shukka Process Number)
  - 出荷品番 (Shukka Product Number)
  - 出荷処理区分 (Shukka Process Type) - Radio: 倉庫向け

- **Bên phải:**
  - 基準日 (Reference Date)
  - 前回出荷処理番号 (Previous Shukka Process Number)
  - 前回出荷番号 (Previous Shukka Number)

#### **PHẦN 2: MIDDLE (2 cột 4-8)**

**Bên trái (4/12):**
- 出荷区分 (Shukka Classification)
- 出荷日 (Shukka Date)
- 倉庫 (Warehouse)
- 梱包日 (Packing Date)
- 摘要 (Summary)
- 納期 (Delivery Date)
- 配送業者 (Shipping Company)
- 3 Buttons: 配送業者一括更新, 納期一括上書き, 納期再計算
- 表示単位 (Display Unit) - Radio: 出荷明細 / 梱包明細
- 表示切替 Button
- 明細並び (Sort Details) - Radio: 出荷行番号 / 商品コード / 梱包記号 / 梱包番号

**Bên phải (8/12) - 抽出条件 (Search Conditions):**
- データ区分 (Data Classification) - Radio: 全て / 受注 / 移動指示
- 出荷対象 (Shukka Target) - Radio: 全て / 入金後出荷
- 出荷売上 (Shukka Sales)
- 営業所 (Business Office)
- 出荷予定日 (Shukka Planned Date)
- 納期 (Delivery Date)
- 受注番号 (Sales Order Number)
- 移動指示番号 (Transfer Instruction Number)
- 得意先名 (Customer Name)
- 担当者 (Person in Charge)
- 配送業者 (Shipping Company)
- 客先注文番号 (Customer Order Number)
- 商品名 (Product Name)

#### **PHẦN 3: DANH SÁCH SẢN PHẨM (Sections)**
Hiển thị dạng sections với:
- **Index trái (~80px):** Số thứ tự + Edit/Delete buttons
- **Details phải (3 dòng):**
  - Row 1: 移動指示番号 | 出荷先倉庫 | 最終納入先 | 保留
  - Row 2: 商品 (thẳng hàng với 出荷先倉庫)
  - Row 3: 出荷番号 | 貸出区分 | 納期 | 当初移動数量 | 未出荷数量 | 今回出荷数量

**Control Panel (Top):**
- Nút trái: 出荷明細を追加
- Nút phải (5 nút): 並替表示, 自動採番, 一括採番, 一括保留, 一括解除

#### **PHẦN 4: 2 NÚT Ở GIỮA**
- 詳細分割 (Detail Split)
- 分割解除 (Split Cancel)

### 2. Bulk Operations (In-memory)
- **一括保留:** Set is_reserved=true cho tất cả lines
- **一括解除:** Set is_reserved=false cho tất cả lines
- Chỉ save vào DB khi click Save ở form chính

### 3. Dummy Actions (Notification)
Các nút sau chỉ show notification "この機能は開発中です":
- 配送業者一括更新
- 納期一括上書き
- 納期再計算
- 表示切替
- 詳細分割
- 分割解除
- 並替表示
- 自動採番
- 一括採番

## 🚀 Cài đặt

1. Copy module vào thư mục `custom_addons/`
2. Restart Odoo server
3. Update Apps List
4. Install "OBIC Shukka Management"

```bash
# Restart Odoo
sudo systemctl restart odoo

# Hoặc nếu dùng Docker
docker-compose restart odoo
```

## 📦 Dependencies
- `base`
- `product`
- `stock`

## 🎨 UI Guidelines
- **Tất cả fields cơ bản** có `placeholder` = label
- **Tên biến:** Tiếng Anh, có ý nghĩa
- **Layout:** Tham khảo từ `custom_obic_invoice`
- **Widget sections:** Index trái + 3 dòng details

## ⚙️ Technical Details

### Models
- **obic.shukka:** Model chính quản lý giao hàng
- **obic.shukka.line:** Model chi tiết sản phẩm giao hàng (one2many)

### Widget
- **obic_shukka_line_one2many:** Custom widget hiển thị lines dạng sections
  - Kế thừa từ `X2ManyField`
  - Custom `ListRenderer` để hiển thị layout đặc biệt
  - Hỗ trợ drag & drop reorder (sequence)

## 📝 Notes
- Module chỉ focus vào UI, chưa có logic nghiệp vụ phức tạp
- Dummy actions được implement để chuẩn bị cho giai đoạn sau
- Bulk operations hoạt động in-memory, chỉ save khi user click Save

## 📞 Contact
- **Developer:** Hankan Development Team
- **Version:** 18.0.1.0.0
- **License:** LGPL-3
