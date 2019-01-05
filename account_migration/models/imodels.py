from odoo import api, fields, models
import re
pattern = re.compile('[-+]?[0-9]*\.?[0-9]*')

class accountAccountMigrationFieldSat(models.Model):
    _inherit = 'account.account'

    sat_code_aux = fields.Char('Aux Sat Code')



class accountAccountTagMigrationFields(models.Model):
    _inherit = 'account.account.tag'

    sat_code_aux = fields.Char('Aux Sat Code', compute='_get_sat_only_code', store=True)
    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()

    @api.multi
    @api.depends('name')
    def _get_sat_only_code(self):
        for record in self:
            sat_code_aux = ''
            result = pattern.findall(record.name)
            for ret in result:
                if ret:
                    sat_code_aux = ret
                    break
            record.sat_code_aux = sat_code_aux



class accountInvoiceMigrationFields(models.Model):
    _inherit = 'account.invoice'

    uuid_aux = fields.Char('Old UUID')
    sat_signed_date_aux = fields.Char('Signed Date')
    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class accountInvoiceLineMigrationFields(models.Model):
    _inherit = 'account.invoice.line'

    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()


class accountPaymentMigrationFields(models.Model):
    _inherit = 'account.payment'

    uuid_aux = fields.Char('Old UUID')
    sat_signed_date_aux = fields.Char('Signed Date')
    only_query = fields.Boolean(default=False)
    old_db_id = fields.Integer()

