
from odoo import tools
from odoo import fields, models, api


class ReportOrdreMission(models.AbstractModel):
    _name = 'ordre.mission.report'

    @api.model
    def _get_report_values(self, docids, data=None):
        module_obj = self.env['ordre.mission']

        return {
            'doc_ids': docids,
            'doc_model': "ordre.mission",
            'docs': module_obj,
            'get_total': self.get_total,
        }


