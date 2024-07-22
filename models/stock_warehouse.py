# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    sap_reference = fields.Char(string='SAP Reference')
    sap_location_id = fields.Char(string='SAP Location ID')
    sap_rental_invoice_series = fields.Char(string='SAP Rental Invoice Series')
    bp_code = fields.Char(string='BP Code')
    vendor_code = fields.Char(string='Vendor Code')

    def _compute_show_custom_fields(self):
        company_id = self.env['ir.config_parameter'].sudo().get_param('sap_connector.company_id')
        for location in self:
            location.show_custom_fields = location.company_id == company_id

    show_custom_fields = fields.Boolean(compute='_compute_show_custom_fields')
