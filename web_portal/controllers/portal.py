from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.http import request


class WbCustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        patients = request.env['res.partner']
        patients_count = patients.search_count([])
        values['patients_count'] = patients_count
        return  values

    @http.route(['/my/patients', '/my/patients/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_patients(self, **kwargs):
        values = self._prepare_sale_portal_rendering_values(quotation_page=False, **kwargs)
        request.session['my_orders_history'] = values['orders'].ids[:100]
        return request.render("sale.portal_my_orders", values)