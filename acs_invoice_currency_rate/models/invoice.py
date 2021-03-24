# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    @api.depends('currency_id', 'company_id.currency_id')
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

    @api.one
    @api.depends('currency_id', 'not_company_currency', 'use_custom_rate', 'date_invoice')
    def _compute_currency_rate(self):
        rate = self.currency_id.with_context(data=self.date_invoice).rate
        self.currency_rate = 1 / (rate or self.currency_id.rate)

    @api.onchange('currency_id','use_custom_rate')
    def onchange_currency(self):
        self.custom_rate = 1 / self.currency_id.with_context(data=self.date_invoice).rate

    @api.one
    @api.depends('amount_total', 'custom_rate')
    def _compute_amount_total_company_currency(self):
        if self.not_company_currency:
            self.amount_total_company_currency = self.amount_total * self.custom_rate
        else:
            self.amount_total_company_currency = self.amount_total

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        if not self.use_custom_rate and self.journal_id:
            self.currency_id = self.journal_id.currency_id.id or self.journal_id.company_id.currency_id.id

    @api.multi
    def action_move_create(self):
        return super(AccountInvoice, self.with_context(
            use_custom_rate=self.use_custom_rate,
            custom_rate=self.custom_rate,
            rate_date=self.date_invoice,
            company_id=self.company_id.id)).action_move_create()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def compute_amount_fields(self, amount, src_currency, company_currency, invoice_currency=False):
        """ Helper function to compute value for fields debit/credit/amount_currency based on an amount and the currencies given in parameter"""
        amount_currency = False
        currency_id = False
        invoice = self.env['account.invoice'].browse(self.env.context.get('active_id'))
        context = self._context.copy()
        if invoice :
            context.update({
                'use_custom_rate':invoice.use_custom_rate,
                'custom_rate':invoice.custom_rate
                })
        if src_currency and src_currency != company_currency:
            amount_currency = amount
            amount = src_currency.with_context(context).compute(amount, company_currency)
            currency_id = src_currency.id
        debit = amount > 0 and amount or 0.0
        credit = amount < 0 and -amount or 0.0
        if invoice_currency and invoice_currency != company_currency and not amount_currency:
            amount_currency = src_currency.with_context(self._context).compute(amount, invoice_currency)
            currency_id = invoice_currency.id
        return debit, credit, amount_currency, currency_id