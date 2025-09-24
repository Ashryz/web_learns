from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    equipment_category_id = fields.Many2one('equipment.category')

    @api.onchange('product_id')
    def _onchange_product_for_equipment_category(self):
        for line in self:
            if line.product_id:
                line.equipment_category_id = line.product_id.equipment_category_id
