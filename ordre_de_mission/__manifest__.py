# -*- coding: utf-8 -*-
{
    'name': "Ordre de mission",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_setup', 'hr', 'mail', 'project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views_ordre_de_mission.xml',
        'views/templates.xml',
        'views/ordre_mission_sequence.xml',
        'report/report_ordre_mission.xml',
        'report/template_ordre_mission.xml',
        'views/views_rapport_d_intervention.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
