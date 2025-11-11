/** @odoo-module **/

import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";

class ObicOrderFormController extends FormController {
  setup() {
    super.setup();
  }

  /**
   * Override to handle view mode changes
   */
  async onViewModeChange(mode) {
    const record = this.model.root;
    if (record && record.data.view_mode) {
      if (mode === 'view') {
        // Switch to readonly mode
        await this.model.root.switchMode('readonly');
      } else if (mode === 'edit') {
        // Switch to edit mode
        await this.model.root.switchMode('edit');
      }
    }
  }
}

registry.category("views").add("obic_sale_order_form", {
  ...formView,
  Controller: ObicOrderFormController,
});
