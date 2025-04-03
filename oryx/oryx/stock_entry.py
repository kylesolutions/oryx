
import frappe

def create_stock_entry(doc, method):
    """
    Automatically create a Stock Entry when a Purchase Receipt is submitted.
    """
    try:
        # Initialize Stock Entry
        stock_entry = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Transfer",
            "posting_date": doc.posting_date,
            "posting_time": doc.posting_time,
            "purchase_receipt_no": doc.name,
            "items": []
        })

        # Extract unique target warehouses from custom_vehicle_details
        target_warehouses = set()
        if doc.custom_vehicle_details:
            for row in doc.custom_vehicle_details:
                if row.warehouse:
                    if not frappe.db.exists("Warehouse", row.warehouse):
                        frappe.throw(f"Target warehouse '{row.warehouse}' does not exist.")
                    target_warehouses.add(row.warehouse)

        if not target_warehouses:
            frappe.throw("No target warehouses found in custom_vehicle_details.")

        # Validate source warehouse
        s_warehouse = doc.set_warehouse
        if not s_warehouse:
            frappe.throw(f"Source warehouse (set_warehouse) is not set for Purchase Receipt {doc.name}.")

        # Process each item for each target warehouse
        for t_warehouse in target_warehouses:
            for item in doc.items:
                loaded_qty = 0
                for vehicle_row in doc.custom_vehicle_details:
                    if vehicle_row.warehouse == t_warehouse:
                        loaded_qty = float(vehicle_row.loaded_qty or 0)
                        break

                if loaded_qty > 0:
                    stock_entry.append("items", {
                        "item_code": item.item_code,
                        "qty": loaded_qty,
                        "basic_rate": item.rate,
                        "s_warehouse": s_warehouse,
                        "t_warehouse": t_warehouse
                    })

        # Insert and submit the Stock Entry
        if stock_entry.items:
            stock_entry.insert()
            stock_entry.save()
            frappe.msgprint(f"Stock Entry '{stock_entry.name}' created for Purchase Receipt '{doc.name}'.")
        else:
            frappe.throw("No valid items found for creating the Stock Entry.")

    except Exception as e:
        error_message = f"Error creating Stock Entry for Purchase Receipt {doc.name}: {str(e)}"
        frappe.log_error(error_message, "Auto Stock Entry Error")
        frappe.throw(f"Error while creating Stock Entry: {str(e)}")





