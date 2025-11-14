/** @odoo-module **/

import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

/**
 * Component hiển thị một sale order line dưới dạng section (card)
 * Props:
 * - lineData: Object chứa data của line
 * - index: Index của line trong danh sách
 * - onEdit: Function callback khi click Edit
 * - onDelete: Function callback khi click Delete
 */
export class LineSection extends Component {
  static template = "custom_obic_sale_order.LineSection";
  static props = {
    lineData: { type: Object },
    index: { type: Number },
    onEdit: { type: Function },
    onDelete: { type: Function },
  };

  /**
   * Format number thành string với 2 chữ số thập phân
   */
  formatNumber(value) {
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
    return '0.00';
  }

  /**
   * Get product name từ lineData
   */
  get productName() {
    if (this.props.lineData.product_id) {
      // Nếu product_id là array [id, name]
      if (Array.isArray(this.props.lineData.product_id)) {
        return this.props.lineData.product_id[1] || '';
      }
      // Nếu có display_name riêng
      return this.props.lineData.display_name || this.props.lineData.product_id || '';
    }
    return '';
  }

  /**
   * Handle click Edit button
   */
  onEditClick() {
    console.log('LineSection onEditClick, index:', this.props.index);
    this.props.onEdit(this.props.index);
  }

  /**
   * Handle click Delete button - parent sẽ handle confirmation dialog
   */
  onDeleteClick() {
    console.log('LineSection onDeleteClick, index:', this.props.index);
    this.props.onDelete(this.props.index);
  }
}
