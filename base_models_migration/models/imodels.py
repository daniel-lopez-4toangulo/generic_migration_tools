from odoo import api, fields, models
import re
pattern = re.compile('[-+]?[0-9]*\.?[0-9]*')


### Base Setup ###
class resUsersMigrationFields(models.Model):
    _inherit = 'res.users'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()

class resPartnerMigrationFields(models.Model):
    _inherit = 'res.partner'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()

class resCompanyMigrationFields(models.Model):
    _inherit = 'res.company'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


### Base ###
class irPropertyMigrationFields(models.Model):
    _inherit = 'ir.property'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()



