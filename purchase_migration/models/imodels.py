from odoo import api, fields, models
import re
pattern = re.compile('[-+]?[0-9]*\.?[0-9]*')


class purchaseOrderMigrationFields(models.Model):
    _inherit = 'purchase.order'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class purchaseOrderLineMigrationFields(models.Model):
    _inherit = 'purchase.order.line'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()



