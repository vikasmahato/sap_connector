# -*- coding: utf-8 -*-

from odoo import models
import datetime

class InvoiceJsonBuilder(models.AbstractModel):
    _name = 'sap.invoice.json.builder'
    _description = 'Invoice JSON Builder'

    def build(self, invoice):
        source_orders = invoice.line_ids.sale_line_ids.order_id

        if len(source_orders) > 1:
            raise ValueError("Invoice must have only one source order")

        #state_id = self.env['res.country.state'].search([('code', '=', 'California')]).id # search based on gstn numeric code

        return {
            "CardCode": invoice.partner_id.sap_reference,
            "NumAtCard": "4400139261", # $order->po_no
            "U_UTL_ORDR": source_orders.name, # what if there is no source order
            "DocDate":  invoice.date.strftime('%Y-%m-%d') if invoice.date else False,
            "TaxDate": invoice.date.strftime('%Y-%m-%d') if invoice.date else False,
            "DocType": "dDocument_Service",
            "Series": False,#source_orders.warehouse_id.sap_rental_invoice_series,
            "BPL_IDAssignedToInvoice": source_orders.warehouse_id.sap_reference,
            "DocumentLines": [
                {
                    "U_UNE_QTY": "2",
                    "U_UNIT_RATE": "8400.00",
                    "TaxCode": "IGST_18",
                    "UnitPrice": 16800,
                    "Price": 16800,
                    "ItemDescription": "Double Width 1.8m Scaffold Height: 7.2m | From:1-Feb-2023 | To:28-Feb-2023 | Po:4400139261",
                    "LocationCode": "1",
                    "SACEntry": "2",
                    "AccountCode": "413001"
                }
            ],
            "Comments": "This order was delivered at - Mundra Solar Energy Limited, SEZ Unit-APSEZ, Survey No:180 P & Others Village: Tunda, Taluka: Mundra, Dist: Kachchh,,Gujarat,370435",
            "PayToCode": "Gujarat", # select state of customer address or billing address. Ask Himanshu/Ashok
            "AddressExtension": {
                "BillToBuilding": "3RD FLOOR,307 308 309,CAMPUS CORNER 2,100 FT ROAD,OPP PRAHLADNAGAR GARDEN,Ahmedabad@Ahmedabad@380015",
                "BillToCity": "Ahmedabad",
                "BillToZipCode": 380015,
                "BillToState": "GJ",
                "BillToCountry": "IN",
                "PlaceOfSupply": "GJ"
            }
        }
