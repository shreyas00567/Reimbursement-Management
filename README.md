# Reimbursement Management System

## Problem Statement

Manual reimbursement processes are time consuming and lack transparency.

## Solution

Developed an Odoo module implementing:

• Expense submission workflow  
• Multi level approval system  
• Sequential approval logic  
• Role based access  

## Architecture

Models:

expense.claim → Stores expenses  
expense.approval → Handles approvals  

## Workflow

Employee submits expense  
Manager approval triggered  
Next approver based on sequence  
Final approval updates status  

## Future Enhancements

OCR receipt scanning  
Currency conversion API  
Conditional approval rules  