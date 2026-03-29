from odoo import models, fields

class ExpenseApproval(models.Model):

    _name='expense.approval'

    _description='Expense Approval'


    expense_id=fields.Many2one(

        'expense.claim'

    )

    approver_id=fields.Many2one(

        'res.users'

    )

    sequence=fields.Integer(

        default=1

    )

    is_cfo=fields.Boolean()

    state=fields.Selection([

        ('pending','Pending'),

        ('approved','Approved'),

        ('rejected','Rejected')

    ],default='pending')


    comments=fields.Text()


    def action_approve(self):

        self.state='approved'

        self.check_next()


    def action_reject(self):

        self.state='rejected'

        self.expense_id.state='rejected'


    def check_next(self):

        next_approval=self.search([

            ('expense_id','=',self.expense_id.id),

            ('sequence','>',self.sequence)

        ],order="sequence asc",limit=1)


        if next_approval:

            next_approval.state='pending'

        else:

            self.expense_id.state='approved'


        self.check_special_rules()


    def check_special_rules(self):

        approvals=self.expense_id.approval_ids.filtered(

            lambda a:a.state=='approved'

        )

        total=len(self.expense_id.approval_ids)


        if total:

            percent=(len(approvals)/total)*100


            if percent>=60:

                self.expense_id.state='approved'


        for appr in approvals:

            if appr.is_cfo:

                self.expense_id.state='approved'
