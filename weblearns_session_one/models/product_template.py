from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    equipment_category_id = fields.Many2one('equipment.category')