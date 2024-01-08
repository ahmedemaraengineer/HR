from odoo import models, fields, api

class MyEmployee(models.AbstractModel):
    _inherit = 'hr.employee.base'

    machine_id = fields.Integer(required=True, copy=False, default=None)



    _sql_constraints = [
        ('UniqueEmpID', 'unique(machine_id)', 'Sorry, but the employee ID must be unique')
    ]


 

class MyCustomEmployee(models.Model):
    _inherit = 'hr.employee'

    documents = fields.One2many('emp.documents', 'employee_id', string="Documents")
    documents_no = fields.Integer(compute="_compute_documents_count")

    @api.depends('documents')
    def _compute_documents_count(self):
        for record in self:
            record.documents_no = len(record.documents)


    def action_view_emp_documents(self):
        action = self.env["ir.actions.actions"]._for_xml_id("my_hr.hr_employees_documents_action")  
        action['domain'] = [('employee_id', '=', self.id)] 
        return action               