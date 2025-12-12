# OBIC倉庫移動管理モジュール

## 概要
倉庫間の商品移動を管理するためのOdoo 18カスタムモジュールです。

## 機能

### 主要機能
- **倉庫移動入力**: 倉庫間の商品移動処理を入力・管理
- **移動明細管理**: 商品ごとの詳細な移動情報を管理
- **出庫・入庫情報**: 出庫倉庫・入庫倉庫の詳細情報を記録

### カスタムウィジェット
- セクションレイアウト表示
- 行番号インデックス表示
- 編集・削除ボタン付き
- 4行の詳細情報表示

## モジュール構成

```
custom_obic_warehouse_move/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── obic_warehouse_move.py          # メインモデル
│   └── obic_warehouse_move_line.py     # 明細モデル
├── views/
│   ├── obic_warehouse_move_views.xml   # ビュー定義
│   └── menu_views.xml                  # メニュー定義
├── security/
│   └── ir.model.access.csv             # アクセス権限
└── static/src/
    └── fields/
        └── obic_warehouse_move_line_field/
            ├── obic_warehouse_move_line_field.js      # カスタムウィジェット
            ├── obic_warehouse_move_line_field.xml     # QWebテンプレート
            └── obic_warehouse_move_line_field.scss    # スタイル

```

## データモデル

### obic.warehouse.move (倉庫移動)
**ヘッダー情報:**
- `view_mode`: 照会モード
- `move_number`: 移動番号
- `copy_source_move_number`: 複写元移動番号
- `reference_date`: 基準日
- `previous_move_number`: 前回移動番号

**メイン情報:**
- `business_office`: 事業所
- `transaction_classification`: 取引区分
- `move_date`: 移動日
- `project_number`: 案件番号
- `person_in_charge`: 担当者
- `person_in_charge_department`: 担当者部門
- `outgoing_warehouse`: 出庫倉庫
- `incoming_warehouse`: 入庫倉庫
- `outgoing_stock_location`: 出庫在庫場所
- `incoming_stock_location`: 入庫在庫場所
- `shipping_company`: 配送業者
- `slip_summary`: 伝票摘要

### obic.warehouse.move.line (倉庫移動明細)
**基本情報:**
- `line_number`: 行番号
- `move_classification`: 移動区分
- `continuous_input`: 連続入力フラグ
- `sort_order`: 並び順

**事業所・倉庫情報:**
- `outgoing_business_office`: 出庫事業所
- `incoming_business_office`: 入庫事業所
- `outgoing_warehouse_line`: 出庫倉庫
- `incoming_warehouse_line`: 入庫倉庫
- `outgoing_stock_location_line`: 出庫在庫場所
- `incoming_stock_location_line`: 入庫在庫場所

**商品情報:**
- `product_id`: 商品
- `package_form`: 荷姿
- `quantity_per_package`: 入数
- `number_of_packages`: 荷数
- `loose_quantity`: バラ数
- `total_quantity`: 数量
- `move_unit_price`: 移動単価
- `move_amount`: 移動金額（自動計算）

**棚番情報:**
- `specify_outgoing_shelf_breakdown`: 出庫棚番を内訳で指定する
- `specify_incoming_shelf_breakdown`: 入庫棚番を内訳で指定する
- `outgoing_shelf_number`: 出庫棚番
- `incoming_shelf_number`: 入庫棚番

**その他:**
- `detail_summary`: 移動明細摘要

## インストール

1. モジュールをOdooの`custom_addons`ディレクトリに配置
2. Odooサーバーを再起動
3. アプリメニューから「倉庫移動管理」を検索してインストール

## 使用方法

### 倉庫移動の作成
1. メニュー「OBIC倉庫移動」→「倉庫移動処理」を開く
2. 「新規作成」ボタンをクリック
3. ヘッダー情報とメイン情報を入力
4. 「倉庫移動明細を追加」ボタンをクリックして商品を追加
5. 明細情報を入力して保存

### カスタムウィジェット機能
- **セクション表示**: 各明細が見やすいセクションレイアウトで表示
- **編集**: 各セクションの編集ボタンでモーダル編集
- **削除**: 削除ボタンで確認ダイアログ付き削除
- **自動計算**: 移動金額 = 数量 × 移動単価

### 開発中機能
以下の機能は現在開発中です：
- 手配展開
- 出庫内訳入力
- 分析コード
- 入庫内訳入力

## 技術仕様

### フレームワーク
- Odoo 18.0
- OWL (Odoo Web Library)
- Bootstrap 5

### 依存モジュール
- `base`: 基本モジュール
- `product`: 商品管理
- `stock`: 在庫管理

### カスタムウィジェット
- X2ManyFieldを拡張
- ListRendererをオーバーライド
- QWebテンプレートでセクションレイアウト
- SCSSでカスタムスタイリング

## ライセンス
LGPL-3

## 作成者
Hankan Co., Ltd.

## バージョン履歴
- **1.0.0** (2025-12-09): 初回リリース
  - 基本的な倉庫移動管理機能
  - カスタムセクションレイアウト
  - モーダル編集・削除機能
