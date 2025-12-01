/** @odoo-module **/

import { registry } from '@web/core/registry';
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { ListRenderer } from "@web/views/list/list_renderer";
import { useX2ManyCrud, useOpenX2ManyRecord } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

/**
 * Custom List Renderer để hiển thị invoice meisai lines dưới dạng table với inline labels
 * Mỗi row có 11 cột: Label-Value-Label-Value pattern
 */
export class ObicInvoiceMeisaiLineListRenderer extends ListRenderer {
  static template = "custom_obic_invoice.ObicInvoiceMeisaiLineListRenderer";
  static recordRowTemplate = "custom_obic_invoice.ObicInvoiceMeisaiLineListRenderer.RecordRow";

  /**
   * Override onDeleteRecord để thêm confirmation dialog
   */
  async onDeleteRecord(record) {
    this.env.services.dialog.add(ConfirmationDialog, {
      body: _t("この明細を削除してもよろしいですか？"),
      title: _t("削除確認"),
      confirm: async () => {
        await super.onDeleteRecord(record);
      },
      cancel: () => { },
    });
  }
}

/**
 * Custom X2Many Field kế thừa từ X2ManyField của Odoo
 * CRITICAL: PHẢI gọi super.setup() và dùng hooks để data lifecycle hoạt động đúng
 */
export class ObicInvoiceMeisaiLineField extends X2ManyField {
  static template = "custom_obic_invoice.ObicInvoiceMeisaiLineField";
  static components = {
    ...X2ManyField.components,
    ListRenderer: ObicInvoiceMeisaiLineListRenderer,
  };

  setup() {
    // CRITICAL: Phải gọi super.setup() trước
    super.setup();

    // Sử dụng hooks có sẵn của Odoo để handle CRUD operations
    const { saveRecord, updateRecord } = useX2ManyCrud(
      () => this.list,
      this.isMany2Many
    );

    // Hook để mở record dialog
    const openRecord = useOpenX2ManyRecord({
      resModel: this.list.resModel,
      activeField: this.activeField,
      activeActions: this.activeActions,
      getList: () => this.list,
      saveRecord: async (record) => {
        await saveRecord(record);
        // Không auto-save parent record, chờ user click Save invoice
      },
      updateRecord: updateRecord,
      withParentId: this.props.widget !== "many2many",
    });

    // Override _openRecord để customize dialog title
    this._openRecord = (params) => {
      params.title = params.mode === 'edit'
        ? _t("明細を編集")
        : _t("明細を追加");
      openRecord({ ...params });
    };
  }

  /**
   * Check if can add new records
   */
  get canAdd() {
    return this.activeActions.create;
  }


  /**
   * Set is_billing for all lines (in-memory only)
   * @param {boolean} value - true for 一括請求, false for 一括解除
   */
  setAllBilling(value) {
    if (!this.list || !this.list.records) {
      console.warn('No records to update');
      return;
    }

    const records = this.list.records;
    console.log(`Updating is_billing=${value} for ${records.length} lines`);

    // Loop through all records and update in-memory
    records.forEach(record => {
      record.update({ is_billing: value });
    });

    console.log(`Updated ${records.length} lines successfully`);
  }

  /**
   * 一括請求 - Set all lines to is_billing=true
   */
  onBulkBillingTrue() {
    console.log('Bulk Billing True triggered');
    this.setAllBilling(true);
  }

  /**
   * 一括解除 - Set all lines to is_billing=false
   */
  onBulkBillingFalse() {
    console.log('Bulk Billing False triggered');
    this.setAllBilling(false);
  }
}

/**
 * Field descriptor để đăng ký với Odoo registry
 */
export const obicInvoiceMeisaiLineField = {
  ...x2ManyField,
  component: ObicInvoiceMeisaiLineField,
};

// Đăng ký field widget với Odoo
registry.category("fields").add("obic_invoice_meisai_line_one2many", obicInvoiceMeisaiLineField);
