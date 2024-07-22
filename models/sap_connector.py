# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class SapConnector(models.TransientModel):
    _name = 'sap.integration'
    _inherit = ['sap.customer.json.builder', 'sap.invoice.json.builder']
    _description = 'SAP Integration'

    def _get_headers(self):
        access_token = self.env['ir.config_parameter'].sudo().get_param('sap_connector.access_token')
        if not access_token:
            _logger.info(f"access_token: msg=No access token found, getting new one")
            self.get_access_token()
            access_token = self.env['ir.config_parameter'].sudo().get_param('sap_connector.access_token')
        else:
            _logger.info(f"access_token: msg=Using existing access token")

        return {
            'Content-Type': 'application/json',
            'Cookie': f'B1SESSION={access_token}'
        }

    @api.model
    def get_access_token(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        sap_domain = get_param('sap_connector.sap_domain')
        sap_db = get_param('sap_connector.sap_db')
        sap_username = get_param('sap_connector.sap_username')
        sap_password = get_param('sap_connector.sap_password')

        url = f'https://{sap_domain}/b1s/v1/Login'
        payload = json.dumps({
            'CompanyDB': sap_db,
            'UserName': sap_username,
            'Password': sap_password
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, data=payload, headers=headers, verify=False)
        _logger.info(f"REQUEST: {payload} RESPONSE: {response.text}")
        if response.status_code == 200:
            self.env['ir.config_parameter'].sudo().set_param('sap_connector.access_token', response.json()['SessionId'])
        else:
            message = response.json()['error']['message']['value']
            code = response.json()['error']['code']
            _logger.error(response.json()['error']['message']['value'])
            raise UserError(f'Failed to authenticate with SAP: {code} - {message}  ')


    @api.model
    def _make_request(self, endpoint, method, data):
        sap_domain = self.env['ir.config_parameter'].sudo().get_param('sap_connector.sap_domain')
        url = f'https://{sap_domain}/b1s/v1/{endpoint}'
        response = requests.request(method, url, json=data, headers=self._get_headers(), verify=False)
        if response.status_code != 201:
            _logger.error(f'{response.text} {str(self._get_headers())}')
            message = response.json()['error']['message']['value']
            code = response.json()['error']['code']
            _logger.error(response.json()['error']['message']['value'])
            raise UserError(f'Failed to create customer on SAP: {code} - {message}  ')
        return response

    @api.model
    def create_customer_on_sap(self, partner):
        bypass = self.env['ir.config_parameter'].sudo().get_param('sap_connector.bypass')
        if bypass:
            return

        builder = self.env['sap.customer.json.builder']
        customer_data = builder.build(partner)
        response = self._make_request('BusinessPartners', 'POST', customer_data)
        sap_reference = response.json().get('CardCode')
        partner.write({'sap_reference': sap_reference})

    @api.model
    def create_invoice_on_sap(self, invoice):
        bypass = self.env['ir.config_parameter'].sudo().get_param('sap_connector.bypass')
        if bypass:
            return

        builder = self.env['sap.invoice.json.builder']
        invoice_data = builder.build(invoice)
        response = self._make_request('Invoices', 'POST', invoice_data).json()
        sap_doc_number = response.get('DocNumber')
        sap_invoice_number = response.get('InvoiceNumber')
        invoice.write({'sap_doc_number': sap_doc_number})
        invoice.write({'sap_invoice_number': sap_invoice_number})

    @api.model
    def create_credit_note_on_sap(self, invoice):
        bypass = self.env['ir.config_parameter'].sudo().get_param('sap_connector.bypass')
        if bypass:
            return

        builder = self.env['sap.invoice.json.builder']
        invoice_data = builder.build(invoice)
        response = self._make_request('CreditNotes', 'POST', invoice_data).json()
        sap_doc_number = response.get('DocNumber')
        sap_invoice_number = response.get('InvoiceNumber')
        invoice.write({'sap_doc_number': sap_doc_number})
        invoice.write({'sap_invoice_number': sap_invoice_number})

    # Define similar methods for invoices, credit notes, and journal entries
