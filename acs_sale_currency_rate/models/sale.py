# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.one
    @api.depends('pricelist_id', 'currency_id', 'company_id.currency_id')
    def _compute_not_company_currency(self):
        self.not_company_currency = self.currency_id and self.currency_id != self.company_id.currency_id

    not_company_currency = fields.Boolean('Use Custom Currency Rate', compute='_compute_not_company_currency')
    currency_rate = fields.Float(string='System Currency Rate',compute='_compute_currency_rate',
        digits=(12, 6), readonly=True, store=True,help="Currency rate of this invoice")
    use_custom_rate = fields.Boolean('Use Custom Rate', readonly=True, 
        states={'draft': [('readonly', False)]})
    custom_rate = fields.Float(string='Custom Rate', digits=(12, 6), readonly=True)

    amount_total_company_currency = fields.Float(
        compute='_compute_amount_total_company_currency')
    company_currency_id = fields.Many2one("res.currency", compute='get_company_currency',
        string="Currency")

    @api.one
    @api.depends('company_id')
    def get_company_currency(self):
        self.company_currency_id = self.company_id.currency_id

    @api.one
    @api.depends('currency_id', 'not_company_currency', 'use_custom_rate', 'date_order')
    def _compute_currency_rate(self):
        rate = self.currency_id.with_context(data=self.date_order).rate
        self.currency_rate = 1 / (rate or (self.currency_id and self.currency_id.rate) or 1)

    @api.onchange('pricelist_id', 'currency_id', 'use_custom_rate')
    def onchange_currency(self):
        self.custom_rate = 1 / (self.currency_id and self.currency_id.with_context(data=self.date_order).rate or 1)

    @api.one
    @api.depends('amount_total', 'custom_rate')
    def _compute_amount_total_company_currency(self):
        if self.not_company_currency and self.custom_rate > 0.0:
            self.amount_total_company_currency = self.amount_total * self.custom_rate
        else:
            self.amount_total_company_currency = self.amount_total

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create(grouped=grouped, final=final)
        if res:
            self.env['account.invoice'].browse(res).write({'custom_rate': self.custom_rate, 'use_custom_rate': self.use_custom_rate, 'custom_rate': self.custom_rate})
        return res
 

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        # invoice.qb_invoice = order.qb_invoice
        invoice.custom_rate = order.custom_rate
        invoice.use_custom_rate = order.use_custom_rate
        return invoice