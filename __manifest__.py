# -*- coding: utf-8 -*-
{
    'name': "sap_connector",

    'summary': "Connects to SAP HANA via Service Layer API",

    'description': """
        Connects to SAP HANA via Service Layer API. Creates and updates customers, journal entries, invoices and credit notes, etc.
    """,

    'author': "Vikas Mahato",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity/SAP',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/stock_location_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}

