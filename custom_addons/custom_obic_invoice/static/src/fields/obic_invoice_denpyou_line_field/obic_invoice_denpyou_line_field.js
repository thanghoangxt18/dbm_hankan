/** @odoo-module **/

import { registry } from '@web/core/registry';
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { ListRenderer } from "@web/views/list/list_renderer";
import { useX2ManyCrud, useOpenX2ManyRecord } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

/**
 * Custom List Renderer để hiển thị invoice denpyou lines dưới dạng sections/cards
 * Hiển thị 2 rows: 
 * - Row 1: 伝票番号 | 伝票日付 | 回収予定日 | 伝票金額 | 今回請求額 | 請求対象
 * - Row 2: 得意先 | 担当者 | 伝票摘要
 */
export class ObicInvoiceDenpyouLineListRenderer extends ListRenderer {
  static template = "custom_obic_invoice.ObicInvoiceDenpyouLineListRenderer";
  static recordRowTemplate = "custom_obic_invoice.ObicInvoiceDenpyouLineListRenderer.RecordRow";

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
 * Sử dụng ObicInvoiceDenpyouLineListRenderer để hiển thị dạng sections
 */
export class ObicInvoiceDenpyouLineField extends X2ManyField {
  static template = "custom_obic_invoice.ObicInvoiceDenpyouLineField";
  static components = {
    ...X2ManyField.components,
    ListRenderer: ObicInvoiceDenpyouLineListRenderer,
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
        ? _t("伝票明細を編集")
        : _t("伝票明細を追加");
      openRecord({ ...params });
    };
  }

  /**
   * Check if can add new records
   */
  get canAdd() {
    return this.activeActions.create;
  }
}

/**
 * Field descriptor để đăng ký với Odoo registry
 */
export const obicInvoiceDenpyouLineField = {
  ...x2ManyField,
  component: ObicInvoiceDenpyouLineField,
};

// Đăng ký field widget với Odoo
registry.category("fields").add("obic_invoice_denpyou_line_one2many", obicInvoiceDenpyouLineField);
