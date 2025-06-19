import frappe

def update_po_collection_status(po_name):
    # Get all GRTs linked to this PO Form
    all_grts = frappe.get_all(
        "Goods Receive Trip",
        filters={"po_form": po_name},
        fields=["name", "receive_status"]
    )

    # Check if all receive_status values are 'Received'
    all_received = all(grt["receive_status"].strip().lower() == "received" for grt in all_grts)

    # Set collection_status accordingly
    collection_status = "Received" if all_received else "In Progress"

    # Update the PO Form
    frappe.db.set_value("PO Form", po_name, "collection_status", collection_status)

def on_update(doc, method):
    frappe.logger().info(f"on_update triggered for GRT: {doc.name}")
    if doc.po_form:
        update_po_collection_status(doc.po_form)