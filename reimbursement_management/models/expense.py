from odoo import models, fields, api

class ExpenseClaim(models.Model):

    _name='expense.claim'

    _description='Expense Claim'


    name=fields.Char(required=True)

    employee_id=fields.Many2one(
        'hr.employee',
        required=True
    )

    manager_id=fields.Many2one(
        'hr.employee',
        string="Manager"
    )

    amount=fields.Float()

    description=fields.Text()

    date=fields.Date()

    state=fields.Selection([

        ('draft','Draft'),

        ('submitted','Submitted'),

        ('manager','Manager Approval'),

        ('approved','Approved'),

        ('rejected','Rejected')

    ],default='draft')


    approval_ids=fields.One2many(

        'expense.approval',

        'expense_id'

    )


    def action_submit(self):

        self.state='submitted'


    def action_manager_approve(self):

        self.state='manager'


    def action_approve(self):

        self.state='approved'


    def action_reject(self):

        self.state='rejected'
        manager_id=fields.Many2one(
'hr.employee',
string="Manager"
)
