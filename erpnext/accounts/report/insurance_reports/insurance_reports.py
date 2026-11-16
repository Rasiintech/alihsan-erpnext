# Copyright (c) 2026, Anfac Tech and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_data(filters):
    if not filters:
        filters = {}

    company = filters.get("company") or frappe.defaults.get_user_default("Company")
    from_date = filters.get("from")
    to_date = filters.get("to")

    query = """
        SELECT 
            si.patient AS pid,
            si.patient_name AS patient_name,
            si.name AS name,
            sii.item_group AS item_group,
            CASE 
                WHEN IFNULL(si.is_insurance, 0) = 1 THEN si.insurance
                ELSE si.customer
            END AS insurance,
            SUM(sii.net_amount) AS total_amount
        FROM 
            `tabSales Invoice` si
        JOIN 
            `tabSales Invoice Item` sii ON si.name = sii.parent
        LEFT JOIN
            `tabCustomer` c ON c.name = si.customer
        WHERE 
            si.docstatus = 1
            AND si.company = %(company)s
            AND si.status IN ('Unpaid', 'Paid', 'Overdue')
            AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND (
                IFNULL(si.is_insurance, 0) = 1
                OR (
                    IFNULL(si.is_insurance, 0) = 0
                    AND c.customer_group = 'Insurance'
                )
            )
        GROUP BY 
            si.patient, si.patient_name, si.name, sii.item_group,
            CASE 
                WHEN IFNULL(si.is_insurance, 0) = 1 THEN si.insurance
                ELSE si.customer
            END
        ORDER BY 
            total_amount DESC;
    """

    data = frappe.db.sql(query, {
        "company": company,
        "from_date": from_date,
        "to_date": to_date
    }, as_dict=1)

    return data

def get_columns():
    return [
        {
            "label": _("PID"),
            "fieldname": "pid",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Patient Name"),
            "fieldname": "patient_name",
            "fieldtype": "Data",
            "width": 170
        },
        {
            "label": _("Name"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 150
        },
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 140
        },
        {
            "label": _("Insurance"),
            "fieldname": "insurance",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Total Amount"),
            "fieldname": "total_amount",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 170
        }
    ]