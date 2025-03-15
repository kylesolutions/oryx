// Copyright (c) 2025, vivek and contributors
// For license information, please see license.txt

frappe.query_reports["Trip sheet"] = {
	"filters": [

        {
            "fieldname": "driver",
            "label": __("Driver"),
            "fieldtype": "Link",
            "options": "Driver",
            "reqd": 0
        },
        {
            "fieldname": "start_date",
            "label": __("Start Date"),
            "fieldtype": "Date",
            "reqd": 1
        },
        {
            "fieldname": "end_date",
            "label": __("End Date"),
            "fieldtype": "Date",
            "reqd": 1
        }
    ]
};
