from odoo import models, fields



class ResPartner(models.Model):
    _inherit = 'res.partner'

    filter_products_in_po_based_on_category = fields.Boolean(default=False)
    product_lst_ids = fields.Many2many('product.product')