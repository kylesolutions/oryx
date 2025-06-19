
# import frappe

# def goods_receive_trip(doc, method):
#     """
#     Automatically create Goods Receiving Trips based on the number of vehicles in the PO Form.
#     """
#     if not doc.custom_vehicle_details:
#         frappe.msgprint("No vehicle details found in PO Form.")
#         return

#     created_trips = 0

#     for vehicle_detail in doc.custom_vehicle_details:
#         vehicle = vehicle_detail.vehicle
#         driver = vehicle_detail.driver
#         loaded_qty = vehicle_detail.loaded_qty
#         meter_reading = vehicle_detail.meter_reading
#         before_loading = vehicle_detail.before_loading
#         meter_readingal = vehicle_detail.meter_readingal
#         after_loading = vehicle_detail.after_loading
#         address = vehicle_detail.address_display
#         loading_point = vehicle_detail.loading_point

#         if not vehicle or not driver:
#             frappe.log_error(f"Missing vehicle or driver in vehicle_detail: {vehicle_detail}", "Goods Receive Trips Creation Error")
#             continue

#         # Loop through item_details child table
#         for item in doc.items:
#             item_code = item.item_code  # Get item code from each row
#             loading_uom = item.uom

#             # Create new Goods Receive Trip
#             kyle_trip = frappe.new_doc("Goods Receive Trip")
#             kyle_trip.vehicle = vehicle
#             kyle_trip.driver = driver
#             kyle_trip.qty = loaded_qty
#             kyle_trip.meter_readingbl = meter_reading
#             kyle_trip.meter_readingal = meter_readingal
#             kyle_trip.weightbl = before_loading
#             kyle_trip.weightal = after_loading
#             kyle_trip.loading_point = loading_point
#             kyle_trip.item_code = item_code  # Assign correct item_code
#             kyle_trip.supplier = doc.supplier
#             kyle_trip.time = doc.posting_time
#             kyle_trip.date = doc.posting_date
#             kyle_trip.purchase_receipt = doc.name
#             kyle_trip.address = address
#             kyle_trip.loading_uom = loading_uom

#             try:
#                 kyle_trip.insert()
#                 kyle_trip.save()
#                 created_trips += 1
#             except frappe.ValidationError as e:
#                 frappe.log_error(f"Error creating Goods Receive Trips: {str(e)}", "Goods Receive Trips Creation Error")
#             except Exception as e:
#                 frappe.log_error(f"Unexpected error: {str(e)}", "Goods Receive Trips Creation Error")

#     if created_trips > 0:
#         frappe.msgprint(f"{created_trips} Goods Receive Trips Created and Saved.")
#     else:
#         frappe.msgprint("No Goods Receive Trips were saved.")





import frappe

def goods_receive_trip(doc, method):
    """
    Automatically create Goods Receiving Trips when submitting a Purchase Receipt,
    but only if the PO Form (custom_po_form) is not set.
    If a GRT is already created from the linked Purchase Order, do not create another.
    """

    # If Purchase Receipt is linked to a PO Form, skip GRT creation
    if doc.custom_po_form:
        frappe.msgprint(f"Purchase Receipt is linked to PO Form {doc.custom_po_form}. Skipping GRT creation.")
        return

    # Check if the Purchase Receipt is linked to a Purchase Order (PO)
    po_list = list(set(item.purchase_order for item in doc.items if item.purchase_order))

    # If there's a linked PO, check if GRTs are already created for it
    if po_list:
        existing_grt = frappe.get_all("Goods Receive Trip", 
                                      filters={"purchase_receipt": ["in", po_list]}, 
                                      fields=["name"])
        if existing_grt:
            frappe.msgprint(f"GRTs already exist for Purchase Order(s) {', '.join(po_list)}. Skipping GRT creation.")
            return

    # Ensure vehicle details exist
    if not doc.custom_vehicle_details:
        frappe.msgprint("No vehicle details found in Purchase Receipt.")
        return

    created_trips = 0

    for vehicle_detail in doc.custom_vehicle_details:
        vehicle = vehicle_detail.vehicle
        driver = vehicle_detail.driver
        loaded_qty = vehicle_detail.loaded_qty
        meter_reading = vehicle_detail.meter_reading
        before_loading = vehicle_detail.before_loading
        meter_readingal = vehicle_detail.meter_readingal
        after_loading = vehicle_detail.after_loading
        address = vehicle_detail.address_display
        loading_point = vehicle_detail.loading_point
        net_weight = vehicle_detail.net_weight

        if not vehicle or not driver:
            frappe.log_error(f"Missing vehicle or driver in vehicle_detail: {vehicle_detail}", "Goods Receive Trips Creation Error")
            continue

        for item in doc.items:
            item_code = item.item_code
            loading_uom = item.uom

            # Create new Goods Receive Trip
            kyle_trip = frappe.new_doc("Goods Receive Trip")
            kyle_trip.vehicle = vehicle
            kyle_trip.driver = driver
            kyle_trip.qty = loaded_qty
            kyle_trip.meter_readingbl = meter_reading
            kyle_trip.meter_readingal = meter_readingal
            kyle_trip.weightbl = before_loading
            kyle_trip.weightal = after_loading
            kyle_trip.loading_point = loading_point
            kyle_trip.item_code = item_code
            kyle_trip.supplier = doc.supplier
            kyle_trip.time = doc.posting_time
            kyle_trip.date = doc.posting_date
            kyle_trip.purchase_receipt = doc.name  # Changed from po_form to purchase_receipt
            kyle_trip.address = address
            kyle_trip.loading_uom = loading_uom
            kyle_trip.net_weight = net_weight

            try:
                kyle_trip.insert()
                kyle_trip.save()
                created_trips += 1
            except frappe.ValidationError as e:
                frappe.log_error(f"Error creating Goods Receive Trip: {str(e)}", "Goods Receive Trips Creation Error")
            except Exception as e:
                frappe.log_error(f"Unexpected error: {str(e)}", "Goods Receive Trips Creation Error")

    if created_trips > 0:
        frappe.msgprint(f"{created_trips} Goods Receive Trip(s) Created and Saved.")
    else:
        frappe.msgprint("No Goods Receive Trips were saved.")