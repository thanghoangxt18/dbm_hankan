/** @odoo-module **/

import { registry } from '@web/core/registry';
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { ListRenderer } from "@web/views/list/list_renderer";
import { useX2ManyCrud, useOpenX2ManyRecord } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

/**
 * Custom List Renderer để hiển thị shukka lines dưới dạng sections
 * Layout: Index trái (60px) + 3 dòng details phải:
 * - Row 1: 移動指示番号 | 出荷先倉庫 | 最終納入先 | 保留
 * - Row 2: 商品 (thẳng hàng với 出荷先倉庫)
 * - Row 3: 出荷番号 | 貸出区分 | 納期 | 当初移動数量 | 未出荷数量 | 今回出荷数量
 */
export class ObicShukkaLineListRenderer extends ListRenderer {
  static template = "custom_obic_shukka.ObicShukkaLineListRenderer";
  static recordRowTemplate = "custom_obic_shukka.ObicShukkaLineListRenderer.RecordRow";

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
 * Sử dụng ObicShukkaLineListRenderer để hiển thị dạng sections
 */
export class ObicShukkaLineField extends X2ManyField {
  static template = "custom_obic_shukka.ObicShukkaLineField";
  static components = {
    ...X2ManyField.components,
    ListRenderer: ObicShukkaLineListRenderer,
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
        // Không auto-save parent record, chờ user click Save
      },
      updateRecord: updateRecord,
      withParentId: this.props.widget !== "many2many",
    });

    // Override _openRecord để customize dialog title
    this._openRecord = (params) => {
      params.title = params.mode === 'edit'
        ? _t("出荷明細を編集")
        : _t("出荷明細を追加");
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
   * Set is_reserved for all lines (in-memory only)
   * @param {boolean} value - true for 一括保留, false for 一括解除
   */
  setAllReserved(value) {
    if (!this.list || !this.list.records) {
      console.warn('No records to update');
      return;
    }

    const records = this.list.records;
    console.log(`Updating is_reserved=${value} for ${records.length} lines`);

    // Loop through all records and update in-memory
    records.forEach(record => {
      record.update({ is_reserved: value });
    });

    console.log(`Updated ${records.length} lines successfully`);
  }

  /**
   * 一括保留 - Set all lines to is_reserved=true
   */
  onBulkReserveTrue() {
    console.log('Bulk Reserve True triggered');
    this.setAllReserved(true);
  }

  /**
   * 一括解除 - Set all lines to is_reserved=false
   */
  onBulkReserveFalse() {
    console.log('Bulk Reserve False triggered');
    this.setAllReserved(false);
  }

  /**
   * 並替表示 - Sort display (dummy)
   */
  onSortDisplay() {
    this.env.services.notification.add(
      _t("この機能は開発中です"),
      { type: "warning", title: _t("並替表示") }
    );
  }

  /**
   * 自動採番 - Auto numbering (dummy)
   */
  onAutoNumbering() {
    this.env.services.notification.add(
      _t("この機能は開発中です"),
      { type: "warning", title: _t("自動採番") }
    );
  }

  /**
   * 一括採番 - Bulk numbering (dummy)
   */
  onBulkNumbering() {
    this.env.services.notification.add(
      _t("この機能は開発中です"),
      { type: "warning", title: _t("一括採番") }
    );
  }
}

/**
 * Field descriptor để đăng ký với Odoo registry
 */
export const obicShukkaLineField = {
  ...x2ManyField,
  component: ObicShukkaLineField,
};

// Đăng ký field widget với Odoo
registry.category("fields").add("obic_shukka_line_one2many", obicShukkaLineField);
