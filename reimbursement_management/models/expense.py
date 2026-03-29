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

    currency=fields.Char()

    category=fields.Char()

    description=fields.Text()

    date=fields.Date()

    state=fields.Selection([

        ('draft','Draft'),

        ('submitted','Submitted'),

        ('manager','Manager Approval'),

        ('finance','Finance Approval'),

        ('approved','Approved'),

        ('rejected','Rejected')

    ],default='draft')


    approval_ids=fields.One2many(

        'expense.approval',

        'expense_id'

    )


    rule_id=fields.Many2one(

        'approval.rule'

    )


    def action_submit(self):

        self.state='submitted'


    def action_manager_approve(self):

        self.state='manager'


    def action_approve(self):

        self.state='approved'


    def action_reject(self):

        self.state='rejected'


    def check_rules(self):

        if self.rule_id:

            self.rule_id.check_rule(self)
