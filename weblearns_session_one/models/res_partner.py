import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    filter_products_in_po_based_on_category = fields.Boolean(default=False)
    product_lst_ids = fields.Many2many('product.product')
    vendor_priority = fields.Selection([
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
        ("strategic", "Strategic"),
    ],default='medium')

    @api.constrains('mobile')
    def _check_mobile_number(self):
        for rec in self:
            if rec.mobile:
                cleaned_mobile = self._clean_mobile_number(rec.mobile)
                if not cleaned_mobile.isdigit() or len(cleaned_mobile) !=10:
                    raise ValidationError("Mobile must be exactly 10 digits")

    def _clean_mobile_number(self,mobile):
        return mobile.replace('+','').replace('-','').replace(' ', '')


    def _format_mobile_number(self, mobile):
        if mobile:
            mobile_date = re.sub('[^\d]','',mobile)
            if len(mobile_date) == 10:
                return f"+{mobile_date}"
            else:
                return mobile

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'mobile' in vals and vals['mobile']:
                vals['mobile'] = self._format_mobile_number(vals['mobile'])
        return super(ResPartner,self).create(vals_list)

    def write(self,vals):
        if 'mobile' in vals and vals['mobile']:
            vals['mobile'] = self._format_mobile_number(vals['mobile'])
        return super(ResPartner, self).write(vals)
