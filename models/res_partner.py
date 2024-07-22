# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    sap_reference = fields.Char(string='SAP Reference')

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)
        company_id = self.env['ir.config_parameter'].sudo().get_param('sap_connector.company_id')
        if str(self.env.user.company_id.id) == company_id and partner.is_company:
            self.env['sap.integration'].create_customer_on_sap(partner)
        return partner

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        # for partner in self:
        #     if partner.is_company and len(vals) != 0:
        #         self.env['sap.integration'].update_customer_in_sap(partner)
        return res
