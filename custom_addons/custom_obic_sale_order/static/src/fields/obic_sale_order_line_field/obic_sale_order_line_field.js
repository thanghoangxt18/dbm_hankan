/** @odoo-module **/

import { registry } from '@web/core/registry';
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { ListRenderer } from "@web/views/list/list_renderer";
import { useX2ManyCrud, useOpenX2ManyRecord } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";

/**
 * Custom List Renderer để hiển thị order lines dưới dạng sections/cards
 * thay vì table rows
 */
export class ObicSaleOrderLineListRenderer extends ListRenderer {
  static template = "custom_obic_sale_order.ObicSaleOrderLineListRenderer";
  static recordRowTemplate = "custom_obic_sale_order.ObicSaleOrderLineListRenderer.RecordRow";
}

/**
 * Custom X2Many Field kế thừa từ X2ManyField của Odoo
 * Sử dụng ObicSaleOrderLineListRenderer để hiển thị dạng sections
 */
export class ObicSaleOrderLineField extends X2ManyField {
  static template = "custom_obic_sale_order.ObicSaleOrderLineField";
  static components = {
    ...X2ManyField.components,
    ListRenderer: ObicSaleOrderLineListRenderer,
  };

  setup() {
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
        // Không auto-save parent record, chờ user click Save order
      },
      updateRecord: updateRecord,
      withParentId: this.props.widget !== "many2many",
    });

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
}

/**
 * Field descriptor để đăng ký với Odoo registry
 */
export const obicSaleOrderLineField = {
  ...x2ManyField,
  component: ObicSaleOrderLineField,
};

// Đăng ký field widget với Odoo
registry.category("fields").add("obic_sale_order_line_one2many", obicSaleOrderLineField);
