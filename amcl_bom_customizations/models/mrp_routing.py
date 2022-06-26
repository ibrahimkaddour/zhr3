# -*- coding:utf-8 -*-
from odoo import fields, models, api, _


class MrpRouting(models.Model):
    _name = 'mrp.routing'
    _description = 'Routing'

    name = fields.Char(string='Routing Name', required=True)
    bom_id = fields.Many2one('mrp.bom', string='BOM')
    active = fields.Boolean(
        string='Active', default=True,
        help="If the active field is set to False, it will allow you to hide the routing without removing it.")
    code = fields.Char(
        string='Reference',
        copy=False, default=lambda self: _('New'), readonly=True)
    note = fields.Text(string='Description')
    location_id = fields.Many2one(
        'stock.location', string='Raw Materials Location',
        help="Keep empty if you produce at the location where you find the raw materials. "
             "Set a location if you produce at a fixed location. This can be a partner location "
             "if you subcontract the manufacturing operations.")
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if 'code' not in vals or vals['code'] == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('mrp.routing') or _('New')
        return super(MrpRouting, self).create(vals)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
