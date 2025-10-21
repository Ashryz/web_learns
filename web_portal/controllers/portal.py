from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager

class WbCustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        patients_count = len(
            request.env['res.partner'].search([]).filtered(lambda p: any(c.name == 'patient' for c in p.category_id)))
        values['patients_count'] = patients_count
        return values

    @http.route(['/my/patients', '/my/patients/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_patients(self, page=1,**kwargs):
        values = self._prepare_portal_layout_values()
        partners = request.env['res.partner'].search([])
        partner_patients = partners.search([]).filtered(
            lambda p: any(c.name == 'patient' for c in p.category_id))
        pager_details = pager(url='/my/patients',
                              total=len(partner_patients),
                              page=page,
                              step=10,
                              )
        patient_category = request.env['res.partner.category'].search([('name', '=', 'patient')], limit=1)
        domain = [('category_id', 'in', patient_category.ids)]
        patients = partners.search(domain,limit=10,offset=pager_details['offset'])
        values.update({
            'patients': patients,
            'page_name': 'patients',
            'pager': pager_details,
        })
        return request.render('web_portal.portal_my_patients_list',values)

    @http.route(['/my/patient/<int:patient_id>'], type='http', auth='user', website=True)
    def portal_my_patients_form(self, patient_id,**kwargs):
        patient = request.env['res.partner'].browse(patient_id)
        values ={
            'patient': patient,
            'page_name': 'patient'
        }
        return request.render('web_portal.portal_my_patients_form', values)