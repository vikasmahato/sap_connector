# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sap_domain = fields.Char("Sap Domain", help="The Domain of your SAP Instance",
                           default=False, config_parameter='sap_connector.sap_domain')
    sap_db = fields.Char("Sap DB", help="The Database name of your SAP Instance",
                         default=False, config_parameter='sap_connector.sap_db')
    sap_username = fields.Char("Sap Username", help="The Username of your SAP Instance",
                         default=False, config_parameter='sap_connector.sap_username')
    sap_password = fields.Char("Sap Password", help="The Password of your SAP Instance",
                         default=False, config_parameter='sap_connector.sap_password')

    access_token = fields.Char("Sap Access Token", help="This is set automatically on successfull login to SAP. Do not change this manually.",
                         default=False, config_parameter='sap_connector.access_token')

    company_id = fields.Many2one('res.company', string="Applicable to Company",
                                   help="Select which company uses SAP Connector", config_parameter='sap_connector.company_id')

    bypass = fields.Boolean(string="Bypass SAP", default=False, config_parameter='sap_connector.bypass', required=True)

    invoice_series = fields.Integer(string="Invoice Series", default=1012, config_parameter='sap_connector.invoice_series', required=True)
    estimates_series = fields.Integer(string="Estimates Series", default=1020, config_parameter='sap_connector.estimates_series', required=True)
    payments_series = fields.Integer(string="Payments Series", default=1030, config_parameter='sap_connector.payments_series', required=True)

