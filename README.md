Reimbursement Management System – Odoo Hackathon

Problem:

Manual reimbursement processes are slow, error prone and lack workflow automation.

Solution:

Developed a configurable reimbursement workflow engine in Odoo supporting sequential and conditional approvals.

Features Implemented:

Expense submission

Employee manager relationship

Multi level approval workflow

Sequential approval logic

Conditional approval rules

Percentage approval rule

Specific approver rule (CFO)

Hybrid rule support

Approval comments

Expense tracking

Architecture:

Models:

expense.claim → expense data

expense.approval → approval workflow

approval.rule → conditional logic

Workflow:

Employee submits expense

Manager approval

Finance approval

Sequential approval chain

Conditional rules evaluated

Final approval

Future Enhancements:

OCR receipt scanning

Currency conversion API

Fraud detection

Email notifications

Tech Stack:

Odoo

Python

PostgreSQL
