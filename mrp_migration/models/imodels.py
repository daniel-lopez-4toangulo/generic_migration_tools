from odoo import api, fields, models
import re
pattern = re.compile('[-+]?[0-9]*\.?[0-9]*')

class mrpBomMigrationFields(models.Model):
    _inherit = 'mrp.bom'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class mrpBomLineMigrationFields(models.Model):
    _inherit = 'mrp.bom.line'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class mrpSubproductMigrationFields(models.Model):
    _inherit = 'mrp.subproduct'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class mrpRoutingMigrationFields(models.Model):
    _inherit = 'mrp.routing'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class mrpRoutingWorkcenterMigrationFields(models.Model):
    _inherit = 'mrp.routing.workcenter'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class mrpRoutingWorkcenterMigrationFields(models.Model):
    _inherit = 'mrp.workcenter'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class mrpProductionMigrationFields(models.Model):
    _inherit = 'mrp.production'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class mrpWorkOrderMigrationFields(models.Model):
    _inherit = 'mrp.workorder'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()





