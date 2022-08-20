
from odoo import tools
from odoo import fields, models, api


class ReportRapportIntervention(models.AbstractModel):
    _name = 'rapport.intervention.report'

    @api.model
    def _get_report_values(self, docids, data=None):
        module_obj = self.env['rapport.intervention']

        return {
            'doc_ids': docids,
            'doc_model': "rapport.intervention",
            'docs': module_obj,
            'get_total': self.get_total,
        }


