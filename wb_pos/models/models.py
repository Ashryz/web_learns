#-*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    visible_backspace_btn = fields.Boolean('Visible Backspace Button?')
    no_negative_sale = fields.Boolean('NO Negative Sale?')

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_data_process(self, loaded_data):
        res = super(PosSession, self)._pos_data_process(loaded_data)
        loaded_data['visible_backspace_btn'] = self.config_id.visible_backspace_btn
        loaded_data.update({
            'visible_backspace_btn': self.config_id.visible_backspace_btn,
            'no_negative_sale': self.config_id.no_negative_sale,
            'default_location_src_id': self.config_id.picking_type_id.default_location_src_id.id
        })
        return res


