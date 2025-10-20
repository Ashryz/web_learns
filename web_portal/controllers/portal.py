from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.http import request


class WbCustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        patients_count = len(
            request.env['res.partner'].search([]).filtered(lambda p: any(c.name == 'patient' for c in p.category_id)))
        values['patients_count'] = patients_count
        return values

    @http.route(['/my/patients', '/my/patients/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_patients(self, **kwargs):
        values = self._prepare_portal_layout_values()
        patients = request.env['res.partner'].search([]).filtered(
            lambda p: any(c.name == 'patient' for c in p.category_id))

        values.update({
            'patients': patients,
            'page_name': 'patients'
        })
        return request.render('web_portal.portal_my_patients_list',values)
