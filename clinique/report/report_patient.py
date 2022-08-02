class PatientReport(models.AbstractModel):
    _name = 'report.patient.report'
    _description = 'Report patient'

    def _get_report_values(self, docids, data=None):
        docs = self.env['clinique.patient'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'clinique.patient',
            'docs': docs,
        }