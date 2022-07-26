# -*- coding: utf-8 -*-


{
    'name': "Clinique",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Clinique",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    'category': 'Clinique',

    # always loaded
    'data': [
        'views/views_ordre_de_mission.xml',
        'views/templates.xml',
        'wizard/Affiche_rdvs_views.xml',
        'report/report_patient.xml',
        'report/report_patient_templates.xml',
        'report/report_rdvs.xml',
        'data/sequence.xml',
        'wizard/Affiche_rdvs_views_template.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/security_rules.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
