/** @odoo-module **/

import { registry } from '@web/core/registry';
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { ListRenderer } from "@web/views/list/list_renderer";
import { useX2ManyCrud, useOpenX2ManyRecord } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

/**
 * Custom List Renderer để hiển thị warehouse move lines dưới dạng sections
 * Layout: Index trái (~80px) + 4 dòng details phải:
 * - Row 1: 商品 | 規格 (mã sản phẩm)
 * - Row 2: 総数 (=数量) | 引当数 (=数量) | 原価単価 (=移動単価) | 原価金額 (=移動金額)
 * - Row 3: 出庫事業所 | 出庫倉庫 | 出庫在庫場所
 * - Row 4: 入庫事業所 | 入庫倉庫 | 入庫在庫場所
 */
export class ObicWarehouseMoveLineListRenderer extends ListRenderer {
  static template = "custom_obic_warehouse_move.ObicWarehouseMoveLineListRenderer";
  static recordRowTemplate = "custom_obic_warehouse_move.ObicWarehouseMoveLineListRenderer.RecordRow";

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
 * Sử dụng ObicWarehouseMoveLineListRenderer để hiển thị dạng sections
 */
export class ObicWarehouseMoveLineField extends X2ManyField {
  static template = "custom_obic_warehouse_move.ObicWarehouseMoveLineField";
  static components = {
    ...X2ManyField.components,
    ListRenderer: ObicWarehouseMoveLineListRenderer,
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
        ? _t("倉庫移動明細を編集")
        : _t("倉庫移動明細を追加");
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
export const obicWarehouseMoveLineField = {
  ...x2ManyField,
  component: ObicWarehouseMoveLineField,
};

// Đăng ký field widget với Odoo
registry.category("fields").add("obic_warehouse_move_line_one2many", obicWarehouseMoveLineField);
