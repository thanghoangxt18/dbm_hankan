/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

/**
 * Modal component để thêm/sửa sale order line
 * Được mở qua dialog service, không cần Dialog component wrapper
 * Props:
 * - lineData: Object chứa data của line (empty nếu tạo mới)
 * - mode: 'create' hoặc 'edit'
 * - onSave: Function callback khi save
 * - onCancel: Function callback khi cancel
 * - productList: Danh sách products để select
 * - close: Function từ dialog service để đóng modal
 */
export class LineModal extends Component {
  static template = "custom_obic_sale_order.LineModal";
  static components = {};
  static props = {
    lineData: { type: Object, optional: true },
    mode: { type: String },
    onSave: { type: Function },
    onCancel: { type: Function },
    productList: { type: Array, optional: true },
  };

  setup() {
    // Initialize state với data từ props hoặc giá trị mặc định
    // Extract product_id correctly: có thể là [id, name] array hoặc số
    let productId = false;
    let productName = '';

    if (this.props.lineData?.product_id) {
      if (Array.isArray(this.props.lineData.product_id)) {
        // Format [id, name] từ ORM
        productId = this.props.lineData.product_id[0];
        productName = this.props.lineData.product_id[1];
      } else {
        // Số ID trực tiếp
        productId = this.props.lineData.product_id;
        productName = this.props.lineData.name || '';
      }
    }

    this.state = useState({
      product_id: productId,
      product_name: productName,
      obic_order_category: this.props.lineData?.obic_order_category || '',
      obic_is_tax_excluded: this.props.lineData?.obic_is_tax_excluded ?? true,
      obic_specification: this.props.lineData?.obic_specification || '',

      obic_quantity: this.props.lineData?.obic_quantity || 1,
      obic_list_unit_price: this.props.lineData?.obic_list_unit_price || 0,
      obic_discount_rate: this.props.lineData?.obic_discount_rate || 100.00,
      obic_sales_unit_price: this.props.lineData?.obic_sales_unit_price || 0,
      obic_sales_amount: this.props.lineData?.obic_sales_amount || 0,
      obic_sales_tax: this.props.lineData?.obic_sales_tax || 0,

      obic_purchase_temp_unit_price: this.props.lineData?.obic_purchase_temp_unit_price || 0,
      obic_purchase_temp_amount: this.props.lineData?.obic_purchase_temp_amount || 0,
      obic_warehouse_code: this.props.lineData?.obic_warehouse_code || '',
      obic_cost_amount: this.props.lineData?.obic_cost_amount || 0,
      obic_gross_profit: this.props.lineData?.obic_gross_profit || 0,

      obic_shipping_destination: this.props.lineData?.obic_shipping_destination || '',
      obic_inventory_warehouse: this.props.lineData?.obic_inventory_warehouse || '',
      obic_line_remark: this.props.lineData?.obic_line_remark || '',
    });

    this.title = this.props.mode === 'create' ? _t('新しい明細を追加') : _t('明細を編集');
  }

  /**
   * Handle khi chọn product - giống _onchange_obic_product_id
   */
  onProductChange(ev) {
    const productId = parseInt(ev.target.value);
    if (!productId) {
      this.state.product_id = false;
      this.state.product_name = '';
      return;
    }

    const product = this.props.productList?.find(p => p.id === productId);
    if (product) {
      this.state.product_id = productId;
      this.state.product_name = product.name;
      // Auto-fill prices từ product
      this.state.obic_list_unit_price = product.list_price || 0;
      this.state.obic_sales_unit_price = product.list_price || 0;
      // Trigger recalculation
      this.calculateSalesAmount();
    }
  }

  /**
   * Handle khi thay đổi list price hoặc discount rate
   * Giống _onchange_obic_calculate_sales_price
   */
  onPriceOrDiscountChange() {
    if (this.state.obic_list_unit_price && this.state.obic_discount_rate) {
      this.state.obic_sales_unit_price =
        this.state.obic_list_unit_price * (this.state.obic_discount_rate / 100.0);
    }
    this.calculateSalesAmount();
  }

  /**
   * Tính toán sales amount khi quantity hoặc unit price thay đổi
   */
  calculateSalesAmount() {
    // Sales amount = unit price × quantity
    this.state.obic_sales_amount =
      this.state.obic_sales_unit_price * this.state.obic_quantity;

    // Sales tax = 10% × sales amount (nếu external tax)
    if (this.state.obic_is_tax_excluded) {
      this.state.obic_sales_tax = this.state.obic_sales_amount * 0.10;
    } else {
      this.state.obic_sales_tax = 0;
    }

    this.calculateGrossProfit();
  }

  /**
   * Tính gross profit
   */
  calculateGrossProfit() {
    this.state.obic_gross_profit =
      this.state.obic_sales_amount - this.state.obic_cost_amount;
  }

  /**
   * Handle khi thay đổi cost amount
   */
  onCostAmountChange() {
    this.calculateGrossProfit();
  }

  /**
   * Handle khi thay đổi tax excluded checkbox
   */
  onTaxExcludedChange() {
    this.calculateSalesAmount();
  }

  /**
   * Validate form trước khi save
   */
  validate() {
    if (!this.state.product_id) {
      alert(_t('商品を選択してください')); // Vui lòng chọn sản phẩm
      return false;
    }
    if (this.state.obic_quantity <= 0) {
      alert(_t('総数は0より大きくなければなりません')); // Số lượng phải lớn hơn 0
      return false;
    }
    return true;
  }

  /**
   * Handle save button
   */
  onSaveClick() {
    if (!this.validate()) {
      return;
    }

    // Chuẩn bị data để trả về - include cả standard Odoo fields
    const lineData = {
      product_id: this.state.product_id,
      name: this.state.product_name || '[No description]', // Required field
      product_uom_qty: this.state.obic_quantity || 1, // Standard Odoo field for quantity

      // OBIC custom fields
      obic_order_category: this.state.obic_order_category,
      obic_is_tax_excluded: this.state.obic_is_tax_excluded,
      obic_specification: this.state.obic_specification,

      obic_quantity: this.state.obic_quantity,
      obic_list_unit_price: this.state.obic_list_unit_price,
      obic_discount_rate: this.state.obic_discount_rate,
      obic_sales_unit_price: this.state.obic_sales_unit_price,
      obic_sales_amount: this.state.obic_sales_amount,
      obic_sales_tax: this.state.obic_sales_tax,

      obic_purchase_temp_unit_price: this.state.obic_purchase_temp_unit_price,
      obic_purchase_temp_amount: this.state.obic_purchase_temp_amount,
      obic_warehouse_code: this.state.obic_warehouse_code,
      obic_cost_amount: this.state.obic_cost_amount,
      obic_gross_profit: this.state.obic_gross_profit,

      obic_shipping_destination: this.state.obic_shipping_destination,
      obic_inventory_warehouse: this.state.obic_inventory_warehouse,
      obic_line_remark: this.state.obic_line_remark,
    };

    console.log('LineModal - onSaveClick - lineData to save:', lineData);

    // Nếu edit mode, giữ nguyên ID
    if (this.props.mode === 'edit' && this.props.lineData?.id) {
      lineData.id = this.props.lineData.id;
    }

    this.props.onSave(lineData);
  }

  /**
   * Handle cancel button
   */
  onCancelClick() {
    this.props.onCancel();
  }
}
