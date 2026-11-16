// Copyright (c) 2026, Anfac Tech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Insurance Reports"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        },
        {
            "fieldname": "from",
            "label": __("From"),
            "fieldtype": "Date",
            "default": frappe.datetime.now_date(),
            "reqd": 1
        },
        {
            "fieldname": "to",
            "label": __("To"),
            "fieldtype": "Date",
            "default": frappe.datetime.now_date(),
            "reqd": 1
        }
    ]
};