from odoo import models, fields

class ExpenseApproval(models.Model):

    _name = 'expense.approval'
    _description = 'Expense Approval'


    expense_id = fields.Many2one(

        'expense.claim',

        string="Expense"

    )

    approver_id = fields.Many2one(

        'res.users',

        string="Approver"

    )

    sequence = fields.Integer(

        string="Approval Level",

        default=1

    )

    state = fields.Selection([

        ('pending','Pending'),

        ('approved','Approved'),

        ('rejected','Rejected')

    ], default='pending')


    comments = fields.Text(

        string="Comments"

    )

    is_special_approver = fields.Boolean(

        string="Special Approver (CFO)"

    )


    def action_approve(self):

        self.state = 'approved'

        self._move_to_next_approval()

        self._check_conditional_rules()


    def action_reject(self):

        self.state = 'rejected'

        self.expense_id.state = 'rejected'


    def _move_to_next_approval(self):

        next_approval = self.search([

            ('expense_id','=',self.expense_id.id),

            ('sequence','>',self.sequence)

        ], order="sequence asc", limit=1)


        if next_approval:

            next_approval.state = 'pending'

        else:

            self.expense_id.state = 'approved'


    def _check_conditional_rules(self):

        approvals = self.expense_id.approval_ids.filtered(

            lambda a: a.state == 'approved'

        )

        total = len(self.expense_id.approval_ids)


        # Percentage rule (60%)
        if total:

            percent = (len(approvals)/total) * 100

            if percent >= 60:

                self.expense_id.state = 'approved'


        # Special approver rule
        for appr in approvals:

            if appr.is_special_approver:

                self.expense_id.state = 'approved'
