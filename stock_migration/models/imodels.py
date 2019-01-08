from odoo import api, fields, models
import re
pattern = re.compile('[-+]?[0-9]*\.?[0-9]*')

class stockWarehouseMigrationFields(models.Model):
    _inherit = 'stock.warehouse'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class stockWarehouseOrderPointMigrationFields(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class stockLocationMigrationFields(models.Model):
    _inherit = 'stock.location'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class stockLocationRouteMigrationFields(models.Model):
    _inherit = 'stock.location.route'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class stockPickingMigrationFields(models.Model):
    _inherit = 'stock.picking'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class stockMoveMigrationFields(models.Model):
    _inherit = 'stock.move'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class stockMoveLineMigrationFields(models.Model):
    _inherit = 'stock.move.line'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class stockProductionLotMigrationFields(models.Model):
    _inherit = 'stock.production.lot'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class stockQuantMigrationFields(models.Model):
    _inherit = 'stock.quant'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class stockQuantPackageFields(models.Model):
    _inherit = 'stock.quant.package'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()



