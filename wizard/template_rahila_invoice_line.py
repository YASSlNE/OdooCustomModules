from odoo import models, fields, api
from datetime import datetime
import datetime
import time



# from odoo import pooler
from odoo import exceptions # will be used in the code
import logging
_logger = logging.getLogger(__name__)

class wizard_report_invoices_line(models.TransientModel):
    _name = 'wizard.report.invoices.line'

    date_from = fields.Date('Date From', required=True)
    date_to=fields.Date('Date To', required=True)
    partner_type = fields.Selection([('empty',''),('محطات / محطات خاصة','محطات خاصة'), ('محطات / محطات مملوكة','محطات مملوكة'),('كبار المستهلكين','كبار المستهلكين')], required=True , string='Partner type')

    @api.multi
    def print_report(self):
        data = {
            'ids': self.ids,
            'form': {
                'date_from': self.date_from,
                'date_to':self.date_to,
                'partner_type':self.partner_type,
            },
        }
        return self.env.ref('rahila_reporting.action_report_invoices_line').report_action(self, data)

    @api.one
    def annuler(self):
        print("annuler")

class report_invoices_line_template(models.AbstractModel):
    _name = 'report.rahila_reporting.reporting_invoice_line'

    def _get_report_values(self, docids, data=None):
        data2=[]
        docs = []
        data1=[]
        date_from = data['form']['date_from']
        date_to=data['form']['date_to']
        partner_form=data['form']['partner_type']
        print(partner_form,'partner_form++++')
        account_invoice = self.env['account.invoice'].search([])
        company_id = self.env['res.company'].search([])
        logo_web = company_id.logo
        dateAuj = time.strftime('%d-%m-%Y')
        for i in account_invoice:
            invoice_obj = self.env['account.invoice'].browse(i.id)
            sale_ref=invoice_obj.sale_ref
            sale_obj=self.env['sale.order'].search([('name','=',sale_ref)])
            payment_reference=sale_obj.account_mode_payement_ids.name


            for j in i.invoice_line_ids:
                partner_ids=self.env['res.partner'].search([('id','=',i.partner_id.id)])
                partner_name=  self.env['res.partner'].browse(partner_ids.id).name
                number = i.number
                partner_id = partner_name
                quantity = j.quantity
                prod_name=j.product_id.name
                print (prod_name,'prod_name+++++')
                amount_untaxed = i.amount_untaxed
                payment_term_id = i.payment_term_id
                partner_category = i.partner_category
                date_invoice = i.date_invoice
                private_transport = i.private_transport
                private_transport_fees = i.private_transport_fees
                driver_allowance = i.driver_allowance
                assistance_allowance = i.assistance_allowance
                amount_total = i.amount_total
                driver_ids=self.env['hr.employee'].search([('id','=',i.driver_id.id)])
                driver_name=  self.env['hr.employee'].browse(driver_ids.id).name
                driver_id = driver_name
                partner_type=self.env['res.partner'].browse(partner_ids.id).category_id.name
                partner_account_id=self.env['res.partner'].browse(partner_ids.id).partner_account_1
                account_obj=self.env['account.account'].search([('id','=',partner_account_id.id)])
                code_partner_account=account_obj.code
                warehouse_invoice = invoice_obj.departure_warehouse.name



                if partner_type == partner_form and (str(date_invoice) >= date_from) and (str(date_invoice) <= date_to):
                    data2.append({
                        'logo_web':logo_web,
                        'number':number,
                        'departure_warehouse': warehouse_invoice,
                        'partner_id':partner_id,
                        'payment_term_id':payment_term_id,
                        'partner_category':partner_category,
                        'private_transport':private_transport,
                        'private_transport_fees':private_transport_fees,
                        'driver_allowance':driver_allowance,
                        'assistance_allowance':assistance_allowance,
                        'driver_id':driver_id,
                        'quantity':quantity,
                        'product_id':prod_name,
                        'amount_untaxed':amount_untaxed,
                        'amount_total':amount_total,
                        'date_invoice': date_invoice,
                        'partner_account_1': code_partner_account,
                        'payment_ref':payment_reference,
                        'ref':self.env['res.partner'].browse(partner_ids.id).ref,
                    })
                elif (str(date_invoice) >= date_from) and (str(date_invoice) <= date_to) and partner_form=='empty':
                    print("test+++++++++++++++++++++++")
                    data2.append({
                        'logo_web':logo_web,
                        'number':number,
                        'departure_warehouse': warehouse_invoice,
                        'partner_id':partner_id,
                        'payment_term_id':payment_term_id,
                        'partner_category':partner_category,
                        'private_transport':private_transport,
                        'private_transport_fees':private_transport_fees,
                        'driver_allowance':driver_allowance,
                        'assistance_allowance':assistance_allowance,
                        'driver_id':driver_id,
                        'quantity':quantity,
                        'product_id':prod_name,
                        'amount_untaxed':amount_untaxed,
                        'amount_total':amount_total,
                        'date_invoice': date_invoice,
                        'partner_account_1': code_partner_account,
                        'payment_ref':payment_reference,
                        'ref':self.env['res.partner'].browse(partner_ids.id).ref,
                    })


        docs.append({
            'dateAuj': dateAuj,
            'date_from':date_from,
            'date_to':date_to,
            'partner_form': partner_form,

        })
        return {
            'doc_ids': docids,
            'doc_model': "self._name",
            'docs': docs,
            'data': data,
            'data1':data1,
            'data2':data2
        }

