/** @odoo-module **/

import { Component, useState, onWillStart, onWillUpdateProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { LineModal } from "../line_modal/line_modal";
import { LineSection } from "../line_section/line_section";

/**
 * Component quản lý sale order lines với UI dạng sections và modal
 * Thay thế cho list editable view mặc định
 */
class SaleOrderLineManager extends Component {
  static template = "custom_obic_sale_order.SaleOrderLineManager";
  static components = { LineSection };

  setup() {
    console.log("SaleOrderLineManager setup");
    this.dialog = useService("dialog");
    this.orm = useService("orm");

    // State quản lý danh sách lines
    this.state = useState({
      lines: [],
      isLoading: false,
    });

    // Load initial data
    onWillStart(() => this.loadInitialData());
    onWillUpdateProps((nextProps) => this.onPropsUpdate(nextProps));
  }

  /**
   * Load dữ liệu ban đầu từ props
   */
  async loadInitialData() {
    console.log("Loading initial data, props.value:", this.props.value);
    if (this.props.value) {
      // Parse existing lines từ value
      const lines = await this._parseLines(this.props.value);
      this.state.lines = lines;
      console.log("Loaded lines:", lines);
    }
  }

  /**
   * Handle khi props thay đổi
   */
  async onPropsUpdate(nextProps) {
    console.log("Props updating:", nextProps);
    if (nextProps.value !== this.props.value) {
      const lines = await this._parseLines(nextProps.value);
      this.state.lines = lines;
    }
  }

  /**
   * Parse lines từ Odoo command format
   * @param {Array} value - Array of commands [[0, 0, {...}], [1, id, {...}], ...]
   */
  async _parseLines(value) {
    if (!value || !Array.isArray(value)) return [];

    const lines = [];
    for (const command of value) {
      if (!Array.isArray(command)) continue;

      const [cmd, id, data] = command;

      // Command 0: Create new record
      if (cmd === 0) {
        lines.push({
          ...data,
          _isNew: true,
          _virtualId: id || `virtual_${Date.now()}_${Math.random()}`
        });
      }
      // Command 1: Update existing record
      else if (cmd === 1) {
        // Nếu đã có data
        if (data && Object.keys(data).length > 0) {
          lines.push({
            ...data,
            id: id,
            _isNew: false
          });
        } else {
          // Load từ server nếu chưa có data
          try {
            const record = await this.orm.read('sale.order.line', [id], []);
            if (record && record[0]) {
              lines.push({
                ...record[0],
                _isNew: false
              });
            }
          } catch (error) {
            console.error("Error loading line:", error);
          }
        }
      }
      // Command 4: Link existing record (chỉ có id)
      else if (cmd === 4) {
        try {
          const record = await this.orm.read('sale.order.line', [id], []);
          if (record && record[0]) {
            lines.push({
              ...record[0],
              _isNew: false
            });
          }
        } catch (error) {
          console.error("Error loading line:", error);
        }
      }
    }

    return lines;
  }

  /**
   * Mở modal để thêm sản phẩm mới
   */
  onAddProduct() {
    console.log("Opening add product modal");

    this.dialog.add(LineModal, {
      title: _t("Thêm sản phẩm mới"),
      mode: 'create',
      lineData: this._getEmptyLineData(),
      onSave: async (data) => {
        console.log("Adding new line with data:", data);
        await this._addLine(data);
      },
    });
  }

  /**
   * Mở modal để edit line
   * @param {Number} index - Index của line cần edit
   */
  onEditLine(index) {
    console.log("Opening edit modal for line:", index);
    const lineData = { ...this.state.lines[index] };

    this.dialog.add(LineModal, {
      title: _t("Chỉnh sửa sản phẩm"),
      mode: 'edit',
      lineData: lineData,
      onSave: async (data) => {
        console.log("Updating line at index", index, "with data:", data);
        await this._updateLine(index, data);
      },
    });
  }

  /**
   * Xóa line với confirmation
   * @param {Number} index - Index của line cần xóa
   */
  onDeleteLine(index) {
    console.log("Request delete line:", index);

    this.dialog.add(ConfirmationDialog, {
      title: _t("Xác nhận xóa"),
      body: _t("Bạn có chắc chắn muốn xóa sản phẩm này?"),
      confirm: async () => {
        console.log("Confirmed delete line:", index);
        await this._deleteLine(index);
      },
      cancel: () => {
        console.log("Cancelled delete");
      },
    });
  }

  /**
   * Thêm line mới vào danh sách
   */
  async _addLine(lineData) {
    // Prepare full data với tất cả fields
    const fullData = this._prepareFullLineData(lineData);

    // Thêm vào state
    const newLine = {
      ...fullData,
      _isNew: true,
      _virtualId: `virtual_${Date.now()}_${Math.random()}`
    };

    this.state.lines = [...this.state.lines, newLine];

    // Update value cho form
    await this._updateFormValue();
  }

  /**
   * Update line trong danh sách
   */
  async _updateLine(index, lineData) {
    const currentLine = this.state.lines[index];
    const fullData = this._prepareFullLineData(lineData);

    // Update trong state
    const updatedLine = {
      ...currentLine,
      ...fullData
    };

    const newLines = [...this.state.lines];
    newLines[index] = updatedLine;
    this.state.lines = newLines;

    // Update value cho form
    await this._updateFormValue();
  }

  /**
   * Xóa line khỏi danh sách
   */
  async _deleteLine(index) {
    const newLines = [...this.state.lines];
    newLines.splice(index, 1);
    this.state.lines = newLines;

    // Update value cho form
    await this._updateFormValue();
  }

  /**
   * Update value cho form với format commands đúng
   * ĐÂY LÀ PHẦN QUAN TRỌNG NHẤT - PHẢI FORMAT ĐÚNG COMMANDS
   */
  async _updateFormValue() {
    const commands = [];

    // Clear all existing lines first (để tránh duplicate)
    if (this.props.value && this.props.value.length > 0) {
      // Xóa tất cả lines cũ
      for (const existingCommand of this.props.value) {
        if (Array.isArray(existingCommand)) {
          const [cmd, id] = existingCommand;
          if (cmd === 1 || cmd === 4) {
            // Delete existing record
            commands.push([2, id, 0]);
          }
        }
      }
    }

    // Add all current lines
    for (const line of this.state.lines) {
      const lineData = this._extractLineData(line);

      if (line._isNew) {
        // Create new record - PHẢI CÓ ĐẦY ĐỦ DATA
        commands.push([0, line._virtualId || 0, lineData]);
      } else if (line.id) {
        // Link existing and update
        commands.push([1, line.id, lineData]);
      }
    }

    console.log("Updating form with commands:", commands);

    // Update value - QUAN TRỌNG: phải dùng update method của props
    if (this.props.update) {
      await this.props.update(commands);
    }
  }

  /**
   * Extract data từ line để gửi lên server
   * PHẢI BAO GỒM TẤT CẢ FIELDS CẦN THIẾT
   */
  _extractLineData(line) {
    const data = {};

    // Required fields
    if (line.product_id) {
      // Xử lý product_id có thể là array [id, name] hoặc chỉ id
      data.product_id = Array.isArray(line.product_id) ? line.product_id[0] : line.product_id;
    }

    // Copy ALL fields (không chỉ những field thay đổi)
    const fieldsToExtract = [
      'name', 'product_uom_qty', 'price_unit', 'tax_id', 'discount',
      'obic_order_category', 'obic_is_tax_excluded', 'obic_specification',
      'obic_quantity', 'obic_list_unit_price', 'obic_discount_rate',
      'obic_sales_unit_price', 'obic_sales_amount', 'obic_sales_tax',
      'obic_purchase_temp_unit_price', 'obic_purchase_temp_amount',
      'obic_warehouse_code', 'obic_cost_amount', 'obic_gross_profit',
      'obic_shipping_destination', 'obic_inventory_warehouse', 'obic_line_remark'
    ];

    for (const field of fieldsToExtract) {
      if (line[field] !== undefined && line[field] !== null) {
        data[field] = line[field];
      }
    }

    // Đảm bảo có ít nhất product_uom_qty
    if (!data.product_uom_qty) {
      data.product_uom_qty = 1;
    }

    return data;
  }

  /**
   * Prepare full line data với default values
   */
  _prepareFullLineData(lineData) {
    const fullData = {
      // Default values
      product_uom_qty: 1,
      obic_quantity: 1,
      obic_is_tax_excluded: true,
      obic_discount_rate: 100.00,
      ...lineData
    };

    return fullData;
  }

  /**
   * Get empty line data với default values
   */
  _getEmptyLineData() {
    return {
      product_id: null,
      name: '',
      product_uom_qty: 1,
      price_unit: 0,

      // OBIC fields với defaults
      obic_order_category: '',
      obic_is_tax_excluded: true,
      obic_specification: '',
      obic_quantity: 1,
      obic_list_unit_price: 0,
      obic_discount_rate: 100.00,
      obic_sales_unit_price: 0,
      obic_sales_amount: 0,
      obic_sales_tax: 0,
      obic_purchase_temp_unit_price: 0,
      obic_purchase_temp_amount: 0,
      obic_warehouse_code: '',
      obic_cost_amount: 0,
      obic_gross_profit: 0,
      obic_shipping_destination: '',
      obic_inventory_warehouse: '',
      obic_line_remark: ''
    };
  }

  /**
   * Check if in edit mode
   */
  get isEditMode() {
    // Check mode từ props hoặc record
    return this.props.record ?
      this.props.record.mode === 'edit' :
      this.props.mode === 'edit';
  }
}

// Đăng ký widget vào registry
registry.category("fields").add("sale_order_line_widget", {
  component: SaleOrderLineManager,
});

export { SaleOrderLineManager };