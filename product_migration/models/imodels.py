from odoo import api, fields, models
import re
pattern = re.compile('[-+]?[0-9]*\.?[0-9]*')


class productProductMigrationFields(models.Model):
    _inherit = 'product.product'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class productTemplateMigrationFields(models.Model):
    _inherit = 'product.template'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class productCategoryMigrationFields(models.Model):
    _inherit = 'product.category'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()



