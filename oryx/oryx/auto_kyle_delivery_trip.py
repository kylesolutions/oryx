import frappe

def create_kyle_delivery_trips(doc, method):
    """
    Automatically create Oryx Delivery Trips based on the number of vehicles in the Delivery Note.
    """
    if not doc.items:
        frappe.msgprint("No vehicle details found in custom_oryx_vehicle_details.")
        return

    created_trips = 0

    for vehicle_detail in doc.items:
        vehicle = vehicle_detail.custom_vehicle
        driver = vehicle_detail.custom_driver
        meter_reading = vehicle_detail.custom_meter_reading_before
        after_meter_reading = vehicle_detail.custom_meter_reading_after   
        before_loading = vehicle_detail.custom_before_loading_weight
        after_loading = vehicle_detail.custom_after_loading_weight
        loading_uom = vehicle_detail.custom_loading_uom
        item_code = vehicle_detail.item_code
        qty = vehicle_detail.custom_delivered_qty
        row_id = vehicle_detail.name 

        if not vehicle or not driver:
            frappe.log_error(f"Missing vehicle or driver in vehicle_detail: {vehicle_detail}", "Oryx Delivery Trip Creation Error")
            continue

        # Create new Kyle Delivery Trip
        kyle_trip = frappe.new_doc("Oryx Delivery Trip")
        kyle_trip.company = doc.company or frappe.defaults.get_user_default("Company")
        kyle_trip.vehicle = vehicle
        kyle_trip.driver = driver
        kyle_trip.meter_reading_after = meter_reading
        kyle_trip.meter_readingal = after_meter_reading
        kyle_trip.before_loading_weight = before_loading
        kyle_trip.after_loading_weight = after_loading
        kyle_trip.loading_uom = loading_uom
        kyle_trip.delivery_note = doc.name
        kyle_trip.item_code = item_code
        kyle_trip.qty = qty
        kyle_trip.posting_date = doc.posting_date
        kyle_trip.row_id = row_id
        
        try:
            kyle_trip.insert()
            kyle_trip.save()
            created_trips += 1
        except frappe.ValidationError as e:
            frappe.log_error(f"Error creating Oryx Delivery Trip: {str(e)}", "Oryx Delivery Trip Creation Error")
        except Exception as e:
            frappe.log_error(f"Unexpected error: {str(e)}", "Oryx Delivery Trip Creation Error")

    if created_trips > 0:
        frappe.msgprint(f"{created_trips} Oryx Delivery Trips Created and Submitted.")
    else:
        frappe.msgprint("No Oryx Delivery Trips were submitted.")




