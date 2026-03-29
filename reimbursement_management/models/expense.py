from odoo import models, fields, api
import base64
import tempfile
import re

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

    manager_comment = fields.Text(
        string="Manager Comment"
    )

    approval_status = fields.Char(
        string="Approval Status"
    )

    history = fields.Text(
        string="Approval History"
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
        string="Converted Amount"
    )

    conversion_rate = fields.Float(
        string="Conversion Rate"
    )

    receipt = fields.Binary(
        string="Receipt"
    )

    ocr_text = fields.Text(
        string="OCR Extracted Text"
    )

    detected_amount = fields.Float(
        string="Detected Amount"
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


    @api.onchange('employee_id')
    def assign_manager(self):

        if self.employee_id:

            self.manager_id = self.employee_id.parent_id


    def convert_currency(self):

        if self.conversion_rate:

            self.converted_amount = self.amount * self.conversion_rate


    def run_ocr(self):

        if not self.receipt:

            return

        try:

            import easyocr

            reader = easyocr.Reader(['en'])

            image_data = base64.b64decode(self.receipt)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:

                f.write(image_data)

                image_path = f.name


            result = reader.readtext(image_path, detail=0)

            extracted_text = " ".join(result)

            self.ocr_text = extracted_text


            amounts = re.findall(r'\d+\.\d+|\d+', extracted_text)


            if amounts:

                detected = max([float(a) for a in amounts])

                self.detected_amount = detected

                self.amount = detected


            if not self.description:

                self.description = extracted_text[:200]


            self.log_history("OCR processed successfully")

        except Exception as e:

            self.log_history("OCR failed : " + str(e))


    def action_submit(self):

        self.state = 'submitted'

        self.approval_status = "Waiting for approval"

        self.run_ocr()

        self.log_history("Expense submitted")


    def action_manager_approve(self):

        self.state = 'manager'

        self.log_history("Manager approved expense")


    def action_approve(self):

        self.state = 'approved'

        self.approval_status = "Approved"

        self.log_history("Expense approved")


    def action_reject(self):

        self.state = 'rejected'

        self.approval_status = "Rejected"

        self.log_history("Expense rejected")


    def check_rules(self):

        if self.rule_id:

            self.rule_id.check_rule(self)


    def log_history(self, message):

        if self.history:

            self.history = self.history + "\n" + message

        else:

            self.history = message