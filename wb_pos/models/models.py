#-*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    visible_backspace_btn = fields.Boolean('Visible Backspace Button?')

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_data_process(self, loaded_data):
        res = super(PosSession, self)._pos_data_process(loaded_data)
        loaded_data['visible_backspace_btn'] = self.config_id.visible_backspace_btn
        return res


