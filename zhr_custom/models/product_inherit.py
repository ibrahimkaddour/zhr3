from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_group_id = fields.Many2one(comodel_name='product.group', string='Group')

    def change_policy(self):
        for product in self:

            if product.invoice_policy == 'order':
                product.write({'invoice_policy': 'delivery'})
            elif product.invoice_policy == 'delivery':
                product.write({'invoice_policy': 'order'})
            else:
                raise UserWarning('WARNING')

