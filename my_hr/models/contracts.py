from odoo import models, api, fields

def calculate_tax_value(AG3):
    if AG3 <= 30000:
        return 0
    elif AG3 <= 45000:
        return (AG3 - 30000) * 0.1
    elif AG3 <= 60000:
        return (AG3 - 45000) * 0.15 + (45000 - 30000) * 0.1
    elif AG3 <= 200000:
        return (AG3 - 60000) * 0.2 + (45000 - 30000) * 0.1 + (60000 - 45000) * 0.15
    elif AG3 <= 400000:
        return (AG3 - 200000) * 0.225 + (45000 - 30000) * 0.1 + (60000 - 45000) * 0.15 + (200000 - 60000) * 0.2
    elif AG3 <= 600000:
        return (45000 - 30000) * 0.1 + (60000 - 45000) * 0.15 + (200000 - 60000) * 0.2 + (400000 - 200000) * 0.225 + (AG3 - 400000) * 0.25
    elif AG3 <= 700000:
        return 45000 * 0.1 + (60000 - 45000) * 0.15 + (200000 - 60000) * 0.2 + (400000 - 200000) * 0.225 + (AG3 - 400000) * 0.25
    elif AG3 <= 800000:
        return 60000 * 0.15 + (200000 - 60000) * 0.2 + (400000 - 200000) * 0.225 + (AG3 - 400000) * 0.25
    elif AG3 <= 900000:
        return 200000 * 0.2 + (400000 - 200000) * 0.225 + (AG3 - 400000) * 0.25
    elif AG3 <= 1200000:
        return 400000 * 0.225 + (AG3 - 400000) * 0.25
    elif AG3 > 1200000:
        return 1200000 * 0.25 + (AG3 - 1200000) * 0.275
    else:
        return 0




class mycontracts(models.Model):
    
    _inherit = 'hr.contract'

    net_salary = fields.Float(string='NET Salary', compute='_calculate_net_salary')
    emp_share = fields.Float(string='Employee Share', help="Please enter the value in percentage")
    medical_ins = fields.Float(string="Medical Ins.")
    soc_ins = fields.Float(string='SOC INS.', compute='_compute_soc_ins')
    tax = fields.Float(string="TAX", compute="_calculate_tax")
    shohdaa = fields.Float(string="Elshohdaa", compute="_calculate_shohdaa")


    @api.depends('wage')
    def _compute_soc_ins(self):
        for cont in self:
            cont.soc_ins = cont.wage if cont.wage < 12600.0 else 12600.0

    @api.depends('wage')
    def _calculate_shohdaa(self):
        for cont in self:
            cont.shohdaa = cont.wage * 0.0005


    @api.depends('wage')
    def _calculate_tax(self):
        for cont in self:
            tax_pool = ((cont.wage - (cont.soc_ins*cont.emp_share)/100) * 12) - 15000
            cont.tax = calculate_tax_value(tax_pool) / 12

    @api.depends('wage')
    def _calculate_net_salary(self):
        for cont in self:
            cont.net_salary = cont.wage - (cont.soc_ins*(cont.emp_share/100) + cont.medical_ins + cont.tax + cont.shohdaa)



