from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    product_lst_ids = fields.Many2many('product.product',compute='_get_partner_product_lst')


    @api.depends('partner_id')
    def _get_partner_product_lst(self):
        for po in self:
            if po.partner_id and po.partner_id.filter_products_in_po_based_on_category and po.partner_id.product_lst_ids:
                po.product_lst_ids = po.partner_id.product_lst_ids
            else:
                po.product_lst_ids = self.env['product.product'].search([('purchase_ok','=',True)])