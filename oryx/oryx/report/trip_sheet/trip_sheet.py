# Copyright (c) 2025, vivek and contributors
# For license information, please see license.txt

# import frappe





import frappe


import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Vehicle No", "fieldname": "vehicle", "fieldtype": "Data", "width": 150},
        {"label": "Driver", "fieldname": "driver", "fieldtype": "Data", "width": 150},
        {"label": "From", "fieldname": "locationport", "fieldtype": "Data", "width": 150},
        {"label": "To", "fieldname": "next_port", "fieldtype": "Data", "width": 150},
        {"label": "Vessel Name", "fieldname": "receiving_vessel", "fieldtype": "Data", "width": 150},
        {"label": "Starting Time", "fieldname": "", "fieldtype": "Time", "width": 150},
        {"label": "Closing Time", "fieldname": "", "fieldtype": "Time", "width": 150},
        {"label": "Closing Date", "fieldname": "", "fieldtype": "Date", "width": 150},
        {"label": "BDR/DN No.", "fieldname": "delivery_note", "fieldtype": "Data", "width": 150},
        {"label": "Remarks", "fieldname": "", "fieldtype": "Data", "width": 150},
        {"label": "Inspect Sign", "fieldname": "", "fieldtype": "Data", "width": 150}
        
       
    ]

def get_data(filters):
    conditions = []  
    
    if filters.get("start_date") and filters.get("end_date"):
        conditions.append(f"posting_date BETWEEN '{filters['start_date']}' AND '{filters['end_date']}'")

    
    if filters.get("driver"):
        conditions.append(f"driver = '{filters['driver']}'")

   
    conditions_sql = " AND ".join(conditions) if conditions else "1=1"  

    query = f"""
        SELECT 
            posting_date,
            vehicle,
            driver,
            locationport,
            receiving_vessel,
            next_port,
            delivery_note
        FROM `tabKyle Delivery Trip`
        WHERE docstatus = 1 AND {conditions_sql}
        ORDER BY posting_date DESC
    """

    frappe.logger().info(f"Executing SQL Query: {query}")  

    return frappe.db.sql(query, as_dict=True)
