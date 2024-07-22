# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    sap_doc_number = fields.Char(string='SAP Doc Number')
    sap_invoice_number = fields.Char(string='SAP Invoice Number')

    def action_post(self):
        res = super(AccountMoveInherit, self).action_post()
        company_id = self.env['ir.config_parameter'].sudo().get_param('sap_connector.company_id')
        if str(self.env.user.company_id.id) == company_id:
            if self.move_type == 'out_invoice':
                self.env['sap.integration'].create_invoice_on_sap(self)
            if self.move_type == 'out_refund':
                self.env['sap.integration'].create_credit_note_on_sap(res)
        return res


    def button_draft(self):
        company_id = self.env['ir.config_parameter'].sudo().get_param('sap_connector.company_id')
        if str(self.env.user.company_id.id) == company_id and self.state == 'posted':
            raise UserError('Editing a posted Invoice is not allowed. Please pass Credit Note and create a new Invoice')

        return super().button_draft()


    def button_cancel(self):
        company_id = self.env['ir.config_parameter'].sudo().get_param('sap_connector.company_id')
        if str(self.env.user.company_id.id) == company_id and self.state == 'posted':
            raise UserError('Invoice cancellation is not allowed. Please pass Credit Note')
        return super().button_cancel()