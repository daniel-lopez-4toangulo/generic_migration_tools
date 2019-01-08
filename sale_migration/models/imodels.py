from odoo import api, fields, models
import re
pattern = re.compile('[-+]?[0-9]*\.?[0-9]*')


class saleOrderMigrationFields(models.Model):
    _inherit = 'sale.order'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class saleOrderLineMigrationFields(models.Model):
    _inherit = 'sale.order.line'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()



