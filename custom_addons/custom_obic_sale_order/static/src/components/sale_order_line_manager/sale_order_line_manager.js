/** @odoo-module **/

import { Component, useState, onWillStart, onWillUpdateProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { LineModal } from "../line_modal/line_modal";
import { LineSection } from "../line_section/line_section";
import { _t } from "@web/core/l10n/translation";

/**
 * Main widget để quản lý sale order lines với modal và sections
 * Thay thế list editable view
 */
export class SaleOrderLineManager extends Component {
  static template = "custom_obic_sale_order.SaleOrderLineManager";
  static components = { LineSection, LineModal };
  static props = {
    record: { type: Object, optional: false },
    readonly: { type: Boolean, optional: true },
    name: { type: String, optional: true },
  };

  setup() {
    this.orm = useService("orm");
    this.dialog = useService("dialog");

    // State để quản lý lines và modal
    this.state = useState({
      lines: [],
      productList: [],
      isReady: false, // Flag để check data đã load xong chưa
      currentLineIndex: -1, // Track line đang edit
      showModal: false,
      modalMode: 'create',
      currentLine: null,
      pendingLineData: {}, // Track data cho virtual records: { virtualId: lineData }
      virtualIdCounter: 0, // Counter để tạo unique virtual IDs
    });

    onWillStart(async () => {
      await this.loadInitialData();
      this.state.isReady = true;
    });

    onWillUpdateProps(async (nextProps) => {
      // Khi props thay đổi (record update), reload lines
      if (nextProps.record && nextProps.record.data) {
        await this.loadLines();
      }
    });
  }

  /**
   * Load initial data: lines và product list
   */
  async loadInitialData() {
    await Promise.all([
      this.loadLines(),
      this.loadProducts(),
    ]);
  }

  /**
   * Load lines từ record.data.order_line
   */
  async loadLines() {
    try {
      const record = this.props.record;
      console.log('loadLines - record:', record);
      console.log('loadLines - record.data:', record?.data);
      console.log('loadLines - order_line:', record?.data?.order_line);

      if (!record || !record.data || !record.data.order_line) {
        console.log('loadLines - No order_line data, setting empty array');
        this.state.lines = [];
        return;
      }

      const orderLineData = record.data.order_line;
      console.log('loadLines - orderLineData:', orderLineData);
      console.log('loadLines - orderLineData.currentIds:', orderLineData.currentIds);
      console.log('loadLines - orderLineData.records:', orderLineData.records);

      // Trong Odoo 18, cần xử lý cả real IDs (từ DB) và virtual IDs (in-memory)
      if (orderLineData.currentIds && orderLineData.currentIds.length > 0) {
        const allLines = [];

        // Duyệt qua từng ID và record tương ứng (currentIds[i] <-> records[i])
        for (let i = 0; i < orderLineData.currentIds.length; i++) {
          const id = orderLineData.currentIds[i];
          const record = orderLineData.records[i];

          console.log(`loadLines - Processing index ${i}: id=${id}, record:`, record);

          // Nếu là real ID (number > 0), CHECK pendingLineData trước, nếu không có thì load từ DB
          if (typeof id === 'number' && id > 0) {
            console.log(`loadLines - Real ID ${id}, checking pendingLineData first`);

            // Ưu tiên lấy từ pendingLineData nếu có (đã edit)
            if (this.state.pendingLineData[id]) {
              console.log(`loadLines - Found edited real ID in pendingLineData:`, this.state.pendingLineData[id]);
              allLines.push({
                id: id,
                ...this.state.pendingLineData[id]
              });
            } else {
              // Không có trong pendingLineData, load từ DB
              console.log(`loadLines - Not in pendingLineData, will load from DB`);
              try {
                const dbLine = await this.orm.read(
                  "sale.order.line",
                  [id],
                  [
                    "product_id",
                    "display_name",
                    "obic_order_category",
                    "obic_is_tax_excluded",
                    "obic_specification",
                    "obic_quantity",
                    "obic_list_unit_price",
                    "obic_discount_rate",
                    "obic_sales_unit_price",
                    "obic_sales_amount",
                    "obic_sales_tax",
                    "obic_purchase_temp_unit_price",
                    "obic_purchase_temp_amount",
                    "obic_warehouse_code",
                    "obic_cost_amount",
                    "obic_gross_profit",
                    "obic_shipping_destination",
                    "obic_inventory_warehouse",
                    "obic_line_remark",
                  ]
                );
                if (dbLine && dbLine.length > 0) {
                  console.log(`loadLines - Loaded DB line:`, dbLine[0]);
                  allLines.push(dbLine[0]);
                }
              } catch (error) {
                console.error(`loadLines - Error loading real ID ${id}:`, error);
              }
            }
          }
          // Nếu là virtual ID (string hoặc <= 0), lấy từ pendingLineData HOẶC in-memory record
          else if (record && record.data) {
            console.log(`loadLines - Virtual ID ${id}, checking pendingLineData and record.data`);

            // Ưu tiên lấy từ pendingLineData
            if (this.state.pendingLineData[id]) {
              console.log(`loadLines - Found in pendingLineData:`, this.state.pendingLineData[id]);
              allLines.push({
                id: id,
                ...this.state.pendingLineData[id]
              });
            }
            // Fallback: lấy từ record.data nếu có
            else if (Object.keys(record.data).length > 0) {
              console.log(`loadLines - Getting from record.data:`, record.data);
              const lineData = {
                id: id,
                product_id: record.data.product_id,
                display_name: record.data.name || record.data.display_name,
                obic_order_category: record.data.obic_order_category,
                obic_is_tax_excluded: record.data.obic_is_tax_excluded,
                obic_specification: record.data.obic_specification,
                obic_quantity: record.data.obic_quantity,
                obic_list_unit_price: record.data.obic_list_unit_price,
                obic_discount_rate: record.data.obic_discount_rate,
                obic_sales_unit_price: record.data.obic_sales_unit_price,
                obic_sales_amount: record.data.obic_sales_amount,
                obic_sales_tax: record.data.obic_sales_tax,
                obic_purchase_temp_unit_price: record.data.obic_purchase_temp_unit_price,
                obic_purchase_temp_amount: record.data.obic_purchase_temp_amount,
                obic_warehouse_code: record.data.obic_warehouse_code,
                obic_cost_amount: record.data.obic_cost_amount,
                obic_gross_profit: record.data.obic_gross_profit,
                obic_shipping_destination: record.data.obic_shipping_destination,
                obic_inventory_warehouse: record.data.obic_inventory_warehouse,
                obic_line_remark: record.data.obic_line_remark,
              };
              console.log('loadLines - Virtual line data:', lineData);
              allLines.push(lineData);
            } else {
              console.log(`loadLines - No data available for virtual ID ${id}`);
            }
          } else {
            console.log(`loadLines - Skipping index ${i}: no valid data`);
          }
        }

        this.state.lines = allLines;
        console.log('loadLines - Final state.lines:', this.state.lines);
      } else {
        console.log('loadLines - No IDs found, setting empty array');
        this.state.lines = [];
      }

    } catch (error) {
      console.error("Error loading lines:", error);
      this.state.lines = [];
    }
  }  /**
   * Load danh sách products để hiển thị trong modal
   */
  async loadProducts() {
    try {
      const products = await this.orm.searchRead(
        "product.product",
        [],
        ["id", "name", "list_price"],
        { limit: 1000 } // Giới hạn 1000 products, có thể tăng nếu cần
      );
      this.state.productList = products;
    } catch (error) {
      console.error("Error loading products:", error);
      this.state.productList = [];
    }
  }

  /**
   * Mở modal để thêm line mới
   */
  openAddLineModal() {
    console.log('openAddLineModal called');
    this.state.modalMode = 'create';
    this.state.currentLine = null;
    this.state.currentLineIndex = -1;
    this.state.showModal = true;
  }

  /**
   * Mở modal để edit line
   */
  openEditLineModal(index) {
    console.log('openEditLineModal called, index:', index);
    const lineToEdit = { ...this.state.lines[index] };
    console.log('lineToEdit:', lineToEdit);

    this.state.modalMode = 'edit';
    this.state.currentLine = lineToEdit;
    this.state.currentLineIndex = index;
    this.state.showModal = true;
  }

  /**
   * Handle khi save từ modal
   */
  async onModalSave(lineData) {
    const record = this.props.record;
    console.log('onModalSave - lineData received:', lineData);
    console.log('onModalSave - modalMode:', this.state.modalMode);

    try {
      if (this.state.modalMode === 'create') {
        // Thêm line mới - tạo virtual record với data ngay từ đầu
        console.log('onModalSave - Creating new line with data:', lineData);

        // Tạo virtual record với CHỈ các field bắt buộc
        const basicLineData = {
          product_id: lineData.product_id,
          name: lineData.name,
          product_uom_qty: lineData.product_uom_qty,
          obic_order_category: lineData.obic_order_category || false,
          obic_is_tax_excluded: lineData.obic_is_tax_excluded,
        };
        console.log('onModalSave - Basic line data (minimal fields):', basicLineData);

        await record.update({
          order_line: [[0, 0, basicLineData]]
        });
        console.log('onModalSave - After create with data, order_line currentIds:', record.data.order_line.currentIds);

        // Lấy virtualId
        const actualVirtualId = record.data.order_line.currentIds[record.data.order_line.currentIds.length - 1];
        console.log('onModalSave - Actual virtual ID:', actualVirtualId);

        // Lưu FULL data vào pendingLineData để display, bao gồm name
        const fullLineData = {
          ...lineData,
          name: lineData.name, // Đảm bảo name được lưu
          display_name: lineData.name, // Cũng lưu display_name
        };
        this.state.pendingLineData[actualVirtualId] = fullLineData;
        console.log('onModalSave - Stored full data in pendingLineData:', this.state.pendingLineData);

        // Reload để display - force reactive update
        await this.loadLines();

        console.log('onModalSave - After loadLines, state.lines:', this.state.lines);
      } else if (this.state.modalMode === 'edit' && lineData.id) {
        // Update existing line
        console.log('onModalSave - Updating line ID:', lineData.id, 'with data:', lineData);

        const isVirtualId = typeof lineData.id === 'string';

        if (isVirtualId) {
          // Virtual ID: Update pendingLineData only
          console.log('onModalSave - Virtual ID detected, updating pendingLineData only');
          const fullLineData = {
            ...lineData,
            name: lineData.name,
            display_name: lineData.name,
          };
          this.state.pendingLineData[lineData.id] = fullLineData;
          console.log('onModalSave - Updated pendingLineData:', this.state.pendingLineData);
        } else {
          // Real ID: CŨNG chỉ update pendingLineData, không gọi record.update()
          // Lý do: record.update() luôn gây lỗi field metadata
          // Khi user click Save order, parent form sẽ tự động lấy data từ pendingLineData
          console.log('onModalSave - Real ID detected, updating pendingLineData (no record.update)');
          const fullLineData = {
            ...lineData,
            name: lineData.name,
            display_name: lineData.name,
          };
          this.state.pendingLineData[lineData.id] = fullLineData;
          console.log('onModalSave - Updated pendingLineData:', this.state.pendingLineData);
        }

        // Reload để display
        await this.loadLines();
        console.log('onModalSave - After edit loadLines, state.lines:', this.state.lines);        // Reload lines để lấy updated data
        await this.loadLines();
      }

      // KHÔNG gọi record.save() ở đây!
      // User sẽ click Save button ở header để save toàn bộ order + lines

      // Đóng modal
      this.state.showModal = false;
      this.state.currentLine = null;
      this.state.currentLineIndex = -1;
      console.log('onModalSave - Changes updated in memory (not saved to DB yet)');
    } catch (error) {
      console.error("Error saving line:", error);
      alert("保存中にエラーが発生しました: " + error.message);
    }
  }  /**
   * Handle khi cancel modal
   */
  onModalCancel() {
    this.state.showModal = false;
    this.state.currentLine = null;
    this.state.currentLineIndex = -1;
  }

  /**
   * Handle delete line
   */
  async deleteLine(index) {
    console.log('deleteLine called, index:', index);
    const line = this.state.lines[index];
    console.log('line to delete:', line);

    this.dialog.add(ConfirmationDialog, {
      title: _t("削除確認"),
      body: _t("この明細を削除してもよろしいですか？"),
      confirm: async () => {
        await this.performDelete(line, index);
      },
      cancel: () => { },
    });
  }

  /**
   * Perform actual delete operation
   */
  async performDelete(line, index) {
    const record = this.props.record;
    console.log('performDelete called');

    try {
      if (line.id) {
        // Nếu line đã có ID (đã lưu trong DB), dùng command [2, id] để mark for deletion
        console.log('Marking line for deletion, ID:', line.id);
        await record.update({
          order_line: [
            [2, line.id] // Command [2, id] để delete
          ]
        });

        // KHÔNG save ở đây - chờ user click Save button ở header
        console.log('performDelete - Line marked for deletion (not saved yet)');
      } else {
        // Nếu line chưa lưu (virtual), sẽ tự động bị remove khi reload
        console.log('Removing unsaved virtual line');
      }

      // Reload lines để reflect changes
      await this.loadLines();
      console.log('Line delete operation completed (pending save)');
    } catch (error) {
      console.error("Error deleting line:", error);
      this.dialog.add(ConfirmationDialog, {
        title: _t("エラー"),
        body: _t("削除中にエラーが発生しました: ") + error.message,
        confirmLabel: _t("OK"),
        cancel: () => { },
      });
    }
  }

  /**
   * Get total amount cho summary
   */
  get totalSalesAmount() {
    return this.state.lines.reduce((sum, line) => {
      return sum + (line.obic_sales_amount || 0);
    }, 0);
  }

  get totalSalesTax() {
    return this.state.lines.reduce((sum, line) => {
      return sum + (line.obic_sales_tax || 0);
    }, 0);
  }

  get totalWithTax() {
    return this.totalSalesAmount + this.totalSalesTax;
  }

  /**
   * Format number
   */
  formatNumber(value) {
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
    return '0.00';
  }
}

// Field Component wrapper cho Odoo field system
export const saleOrderLineField = {
  component: SaleOrderLineManager,
  supportedTypes: ["one2many"],
  extractProps({ attrs, field }, dynamicInfo) {
    return {
      record: dynamicInfo.record,
      readonly: attrs.readonly,
      name: attrs.name,
    };
  },
};

// Đăng ký widget vào field registry
registry.category("fields").add("sale_order_line_widget", saleOrderLineField);
