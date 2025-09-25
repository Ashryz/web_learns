from odoo import models, fields


class ProcurementManagerWizad(models.TransientModel):
    _name = 'procurement.manager.wizard'
    _description = 'Procurement Manager Wizad'

    name = fields.Many2many('res.users',domain=[('share','=',False)])


    def action_open_procurement_report(self):
        return{
            'name':'Procurement Manager Report',
            'type':'ir.actions.act_window',
            'res_model':'purchase.order',
            'view_mode':'list',
            'domain':[('user_id','in',self.name.ids)]
        }