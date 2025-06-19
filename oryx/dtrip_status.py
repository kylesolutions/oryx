import frappe

def update_dt_collection_status(do_name):
    # Get all GRTs linked to this PO Form
    all_oryx_delivery_trip = frappe.get_all(
        "Oryx Delivery Trip",
        filters={"delivery_note": do_name},
        fields=["name", "delivery_status"]
    )

    # Check if all receive_status values are 'Received'
    all_received = all(oryx_delivery_trip["delivery_status"].strip().lower() == "delivered" for oryx_delivery_trip in all_oryx_delivery_trip)

    # Set collection_status accordingly
    delivery_status = "delivered" if all_received else "In Progress"

    # Update the PO Form
    frappe.db.set_value("DO Form", do_name, "delivery_status", delivery_status)

def on_update(doc, method):
    frappe.logger().info(f"on_update triggered for Oryx Delivery Trip: {doc.name}")
    if doc.delivery_note:
        update_dt_collection_status(doc.delivery_note)