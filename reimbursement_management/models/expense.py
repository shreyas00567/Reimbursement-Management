from odoo import models, fields, api

class ExpenseClaim(models.Model):

    _name = 'expense.claim'
    _description = 'Expense Claim'


    name = fields.Char(
        string="Expense Title",
        required=True
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        required=True
    )

    manager_id = fields.Many2one(
        'hr.employee',
        string="Manager"
    )

    amount = fields.Float(
        string="Amount"
    )

    category = fields.Char(
        string="Category"
    )

    description = fields.Text(
        string="Description"
    )

    date = fields.Date(
        string="Expense Date"
    )

    employee_currency = fields.Char(
        string="Expense Currency"
    )

    company_currency = fields.Char(
        string="Company Currency"
    )

    converted_amount = fields.Float(
        string="Amount in Company Currency"
    )

    state = fields.Selection([

        ('draft','Draft'),

        ('submitted','Submitted'),

        ('manager','Manager Approval'),

        ('finance','Finance Approval'),

        ('approved','Approved'),

        ('rejected','Rejected')

    ], default='draft', string="Status")


    approval_ids = fields.One2many(

        'expense.approval',

        'expense_id',

        string="Approvals"

    )


    approval_count = fields.Integer(

        compute="_compute_approval_count"

    )


    rule_id = fields.Many2one(

        'approval.rule',

        string="Approval Rule"

    )


    def _compute_approval_count(self):

        for rec in self:

            rec.approval_count = len(rec.approval_ids)


    def action_submit(self):

        self.state = 'submitted'


    def action_manager_approve(self):

        self.state = 'manager'


    def action_approve(self):

        self.state = 'approved'


    def action_reject(self):

        self.state = 'rejected'


    def check_rules(self):

        if self.rule_id:

            self.rule_id.check_rule(self)
