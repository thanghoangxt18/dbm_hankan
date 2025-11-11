from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import re

class CustomSaleOrderPreviewPortal(CustomerPortal):
    def _make_pdf_response(self, order_sudo, pdf_content):
        try:
            company_register = getattr(order_sudo.partner_id, 'company_registry', '') or ''
            anken_bango = getattr(order_sudo, 'anken_bango', '') or ''
            version_part = getattr(order_sudo, 'version_number', '') or '1'
            project_part = getattr(order_sudo, 'project_name', '') or ''
            project_clean = re.sub(r'[\n\r]+', ' ', project_part).strip()
            project_clean = re.sub(r'\s+', ' ', project_clean)
            filename = f"【2_{company_register}_{anken_bango}_v{version_part}】 {project_clean}_受注明細書.pdf"
            filename = re.sub(r'[<>:\"/\\|?*]', '', filename)
            from urllib.parse import quote
            filename_utf8 = quote(filename)
        except Exception:
            from urllib.parse import quote
            filename_utf8 = quote(f"Sale_Order_{order_sudo.id}.pdf")
        headers = [
            ('Content-Type', 'application/pdf; charset=utf-8'),
            ('Content-Length', len(pdf_content)),
            ("Content-Disposition", f"attachment; filename*=UTF-8''{filename_utf8}")
        ]
        return request.make_response(pdf_content, headers=headers)

    @http.route(['/my/orders/<int:order_id>/download_pdf_template'], type='http', auth="public", website=True)
    def download_pdf_template(self, order_id, access_token=None, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except Exception:
            return request.redirect('/my')
        IrActionsReport = request.env['ir.actions.report'].sudo()
        report_name = 'custom_obic_sale_order.report_new_layout'
        pdf_content, _ = IrActionsReport._render_qweb_pdf(report_name, [order_sudo.id], data=None)
        return self._make_pdf_response(order_sudo, pdf_content)
    @http.route(['/my/orders/<int:order_id>/download_new_template'], type='http', auth="public", website=True)
    def download_new_template_pdf(self, order_id, access_token=None, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except Exception:
            return request.redirect('/my')
        IrActionsReport = request.env['ir.actions.report'].sudo()
        report_name = 'custom_obic_sale_order.new_template'
        report_rec = IrActionsReport.search([('report_name', '=', report_name)], limit=1)
        if report_rec:
            pdf_content, _ = IrActionsReport._render_qweb_pdf(report_rec, [order_sudo.id], data=None)
            return self._make_pdf_response(order_sudo, pdf_content)
        else:
            values = {
                'sale_order': order_sudo,
                'token': order_sudo.access_token,
                'page_name': 'custom_order_preview',
            }
            return request.render('custom_obic_sale_order.new_template_portal_template', values)
