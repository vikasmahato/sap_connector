# -*- coding: utf-8 -*-

from odoo import models


class CustomerJsonBuilder(models.AbstractModel):
    _name = 'sap.customer.json.builder'
    _description = 'Customer JSON Builder'

    def build(self, partner):
        customer =  {
            'CardCode': partner.id,
            'CardName': partner.name,
            'CardType': 'C',
            'Address': partner.street,
            'City': partner.city,
            'ZipCode': partner.zip,
            'MailAddress': partner.street,
            'MailCity': partner.city,
            'MailZipCode': partner.zip,
            'Cellular': partner.phone,
            'EmailAddress': partner.email,
            'BPAddresses': [
                {
                    'AddressName': partner.city,
                    'ZipCode': partner.zip,
                    'City': partner.city,
                    'State': partner.state_id.code,
                    'BuildingFloorRoom': partner.street,
                    'AddressType': 'bo_BillTo',
                    'BPCode': partner.id,
                    'GSTIN': '29AABCI2526F2ZR',
                    'GstType': 'gstRegularTDSISD'
                },
                {
                    'AddressName': partner.city,
                    'ZipCode': partner.zip,
                    'City': partner.city,
                    'State': partner.state_id.code,
                    'BuildingFloorRoom': partner.street,
                    'AddressType': 'bo_ShipTo',
                    'BPCode': partner.id,
                    'GSTIN': '29AABCI2526F2ZR',
                    'GstType': 'gstRegularTDSISD'
                }
            ],
            'ShipToDefault' : partner.city,
            'BilltoDefault' : partner.city
        }

        if not partner.vat: #TODO: replace with gstn
            customer['UseBillToAddrToDetermineTax'] = 'tYES'
            customer['U_UTL_SUBGROUP'] = 'C'
            customer['SubjectToWithholdingTax'] = 'boNO'
        else:
            customer['BPFiscalTaxIDCollection'] = [
                {
                    'TaxId0': partner.vat,
                    'BPCode': partner.id
                }
            ]


        return customer
