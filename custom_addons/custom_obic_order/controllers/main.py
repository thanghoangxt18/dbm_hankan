# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class ObicOrderController(http.Controller):
    
    @http.route('/custom_obic_order', type='http', auth='user', website=False)
    def custom_obic_order(self, **kwargs):
        """
        Route to OBIC Order management page
        Path: /custom_obic_order
        """
        return request.redirect('/web#action=custom_obic_order.action_obic_order&model=obic.order&view_type=list')
    
    @http.route('/custom_obic_order/new', type='http', auth='user', website=False)
    def custom_obic_order_new(self, **kwargs):
        """
        Route to create new OBIC Order
        Path: /custom_obic_order/new
        """
        return request.redirect('/web#action=custom_obic_order.action_obic_order&model=obic.order&view_type=form')
