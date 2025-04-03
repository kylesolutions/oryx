# Copyright (c) 2025, vivek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OryxDeliveryTrip(Document):

    def update_vehicle_in_delivery_note(self):
        """
        Update vehicle, driver, and warehouse in Delivery Note Item using row_id.
        """
        if not self.row_id or not self.vehicle or not self.driver:
            frappe.throw("Row ID, vehicle, and driver details are required in Oryx Delivery Trip.")

        row_id = self.row_id
        vehicle = self.vehicle
        driver = self.driver

        if not frappe.db.exists("Delivery Note Item", row_id):
            frappe.throw(f"Delivery Note Item with Row ID {row_id} not found.")

        vehicle_doc = frappe.get_doc("Vehicle", vehicle)
        new_warehouse = vehicle_doc.get("custom_warehouse")

        if not new_warehouse:
            frappe.throw(f"No warehouse found for vehicle {vehicle}. Please check the vehicle details.")

        dn_item_doc = frappe.get_doc("Delivery Note Item", row_id)
        delivery_note = dn_item_doc.parent

        frappe.db.set_value("Delivery Note Item", row_id, {
            "custom_vehicle": vehicle,   # Correct field name
            "custom_driver": driver,     # Correct field name
            "warehouse": new_warehouse
        }, update_modified=False)

        frappe.db.commit()

        self.update_stock_ledger(delivery_note, row_id, new_warehouse)
        self.enqueue_stock_reposting(delivery_note)

        frappe.msgprint(f"Updated Delivery Note Item (Row: {row_id}) successfully.")

    def update_stock_ledger(self, delivery_note, row_id, new_warehouse):
        """
        Update the Stock Ledger Entry warehouse field.
        """
        stock_ledger_entries = frappe.get_all("Stock Ledger Entry", 
            filters={"voucher_detail_no": row_id, "voucher_no": delivery_note}, 
            fields=["name", "warehouse"])

        for sle in stock_ledger_entries:
            frappe.db.set_value("Stock Ledger Entry", sle.name, "warehouse", new_warehouse, update_modified=False)

        frappe.db.commit()
        frappe.msgprint(f"Stock Ledger Entry warehouse updated for {len(stock_ledger_entries)} entries.")

    def enqueue_stock_reposting(self, delivery_note):
        """
        Enqueue stock reposting.
        """
        frappe.enqueue("erpnext.stock.doctype.stock_reconciliation.stock_reconciliation.repost_stock", 
            posting_date=None, company=None, queue='long')


@frappe.whitelist()
def update_oryx_trip(trip_name):
    """
    Whitelisted function to update vehicle and driver in a submitted Delivery Note Item.
    """
    trip_doc = frappe.get_doc("Oryx Delivery Trip", trip_name)
    trip_doc.update_vehicle_in_delivery_note()  
    return {"status": "success", "message": f"Updated trip {trip_name}"}
