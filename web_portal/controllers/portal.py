from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager
from odoo.osv.expression import AND


class WbCustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        patients_count = len(
            request.env['res.partner'].search([]).filtered(lambda p: any(c.name == 'patient' for c in p.category_id)))
        values['patients_count'] = patients_count
        return values

    @http.route(['/my/patients', '/my/patients/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_patients(self, page=1,sortby='name',search=None, search_in='all',**kwargs):
        partners = request.env['res.partner'].search([])
        partner_patients = partners.search([]).filtered(
            lambda p: any(c.name == 'patient' for c in p.category_id))
        searchbar_sortings = {
            'name': {'label': 'Name','order':'name'},
            'city': {'label':'City','order':'city'},
            'country_id': {'label':'Country','order':'country_id'}
        }
        sort_patient = searchbar_sortings[sortby]['order']

        searchbar_inputs = {
            'all': {'label': 'All', 'input': 'all','domain':[]},
            'name': {'label': 'Name', 'input': 'name','domain': [('name','ilike',search)]},
            'country_id': {'label': 'Country', 'input': 'country_id','domain':[('country_id.name','ilike',search)]}
        }
        search_domain = searchbar_inputs[search_in]['domain']

        pager_details = pager(url='/my/patients',
                              total=len(partner_patients),
                              page=page,
                              step=10,
                              url_args={'sortby': sortby,'search':search,'search_in':search_in},
                              )
        patient_category = request.env['res.partner.category'].search([('name', '=', 'patient')], limit=1)
        domain = [('category_id', 'in', patient_category.ids)]
        if search_in:
            domain = AND([domain, search_domain])

        patients = partners.search(domain,limit=10,order=sort_patient,offset=pager_details['offset'])
        values = {
            'patients': patients,
            'page_name': 'patients',
            'pager': pager_details,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
        }
        return request.render('web_portal.portal_my_patients_list',values)

    @http.route(['/my/patients/<int:patient_id>'], type='http', auth='user', website=True)
    def portal_my_patients_form(self, patient_id,**kwargs):
        patient = request.env['res.partner'].browse(patient_id)
        patient_category = request.env['res.partner.category'].search([('name', '=', 'patient')], limit=1)
        domain = [('category_id', 'in', patient_category.ids)]
        patient_ids = request.env['res.partner'].search(domain).ids
        current_idx = patient_ids.index(patient_id)
        prev_record = current_idx != 0 and patient_ids[current_idx - 1]
        next_record = current_idx < len(patient_ids) - 1 and patient_ids[current_idx + 1]
        values ={
            'patient': patient,
            'page_name': 'patients',
            'prev_record': f'/my/patients/{prev_record}' if prev_record else None,
            'next_record': f'/my/patients/{next_record}' if next_record else None,
        }
        return request.render('web_portal.portal_my_patients_form', values)

    @http.route(['/my/patients/print/<int:patient_id>'], type='http', auth='user', website=True)
    def portal_print_patient(self,patient_id,**kwargs):
        print("print called successfully")
        return
