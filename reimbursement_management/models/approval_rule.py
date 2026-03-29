from odoo import models, fields

class ApprovalRule(models.Model):

    _name='approval.rule'

    _description='Approval Rules'


    name=fields.Char()

    percentage_required=fields.Float()

    require_cfo=fields.Boolean()


    def check_rule(self,expense):

        approvals=expense.approval_ids.filtered(

            lambda a:a.state=='approved'

        )


        total=len(expense.approval_ids)


        if total:

            percent=(len(approvals)/total)*100


            if percent>=self.percentage_required:

                expense.state='approved'


        if self.require_cfo:

            for appr in approvals:

                if appr.is_cfo:

                    expense.state='approved'
