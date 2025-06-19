import frappe

def auto_delivery_trips(doc, method):
    """
    Automatically create Oryx Delivery Trips for each item and vehicle in the Delivery Note.
    """
    if not doc.item_details or not doc.vehicle_details:
        frappe.msgprint("Missing item or vehicle details.")
        return

    created_trips = 0

    for item in doc.item_details:
        loading_uom = item.uom
        item_code = item.item_code
        qty = item.qty

        for vehicle_detail in doc.vehicle_details:
            vehicle = vehicle_detail.vehicle
            driver = vehicle_detail.driver
            meter_reading = vehicle_detail.meter_reading
            before_loading = vehicle_detail.before_loading
            after_meter_reading = vehicle_detail.meter_readingal
            after_loading = vehicle_detail.after_loading
            row_id = vehicle_detail.name
            
            if not vehicle or not driver:
                frappe.log_error(f"Missing vehicle or driver in vehicle_detail: {vehicle_detail}", "Oryx Delivery Trip Creation Error")
                continue

            kyle_trip = frappe.new_doc("Oryx Delivery Trip")
            
            kyle_trip.vehicle = vehicle
            kyle_trip.driver = driver
            kyle_trip.meter_reading_after = meter_reading
            kyle_trip.meter_readingal = after_meter_reading
            kyle_trip.before_loading_weight = before_loading
            kyle_trip.after_loading_weight = after_loading
            kyle_trip.loading_uom = loading_uom
            kyle_trip.do_form = doc.name
            kyle_trip.item_code = item_code
            kyle_trip.qty = qty
            kyle_trip.posting_date = doc.delivery_date
            kyle_trip.customer = doc.customer
            kyle_trip.delivery_point = doc.loading_point
            kyle_trip.address = doc.address_display
            kyle_trip.row_id = row_id

            try:
                kyle_trip.insert()
                kyle_trip.save()
                created_trips += 1
            except frappe.ValidationError as e:
                frappe.log_error(f"Validation error creating Oryx Delivery Trip: {str(e)}", "Oryx Delivery Trip Creation Error")
            except Exception as e:
                frappe.log_error(f"Unexpected error: {str(e)}", "Oryx Delivery Trip Creation Error")

    if created_trips > 0:
        frappe.msgprint(f"{created_trips} Oryx Delivery Trip(s) Created")
    else:
        frappe.msgprint("No Oryx Delivery Trips were created")
