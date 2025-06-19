# import frappe

# def create_kyle_delivery_trips(doc, method):
#     """
#     Automatically create Oryx Delivery Trips based on the number of vehicles in the Delivery Note.
#     """
#     if not doc.items:
#         frappe.msgprint("No vehicle details found in custom_oryx_vehicle_details.")
#         return

#     created_trips = 0

#     for vehicle_detail in doc.items:
#         vehicle = vehicle_detail.custom_vehicle
#         driver = vehicle_detail.custom_driver
#         meter_reading = vehicle_detail.custom_meter_reading_before
#         after_meter_reading = vehicle_detail.custom_meter_reading_after   
#         before_loading = vehicle_detail.custom_before_loading_weight
#         after_loading = vehicle_detail.custom_after_loading_weight
#         loading_uom = vehicle_detail.custom_loading_uom
#         item_code = vehicle_detail.item_code
#         qty = vehicle_detail.custom_delivered_qty
#         row_id = vehicle_detail.name 

#         if not vehicle or not driver:
#             frappe.log_error(f"Missing vehicle or driver in vehicle_detail: {vehicle_detail}", "Oryx Delivery Trip Creation Error")
#             continue

#         # Create new Kyle Delivery Trip
#         kyle_trip = frappe.new_doc("Oryx Delivery Trip")
#         kyle_trip.company = doc.company or frappe.defaults.get_user_default("Company")
#         kyle_trip.vehicle = vehicle
#         kyle_trip.driver = driver
#         kyle_trip.meter_reading_after = meter_reading
#         kyle_trip.meter_readingal = after_meter_reading
#         kyle_trip.before_loading_weight = before_loading
#         kyle_trip.after_loading_weight = after_loading
#         kyle_trip.loading_uom = loading_uom
#         kyle_trip.delivery_note = doc.name
#         kyle_trip.item_code = item_code
#         kyle_trip.qty = qty
#         kyle_trip.posting_date = doc.posting_date
#         kyle_trip.row_id = row_id
        
#         try:
#             kyle_trip.insert()
#             kyle_trip.save()
#             created_trips += 1
#         except frappe.ValidationError as e:
#             frappe.log_error(f"Error creating Oryx Delivery Trip: {str(e)}", "Oryx Delivery Trip Creation Error")
#         except Exception as e:
#             frappe.log_error(f"Unexpected error: {str(e)}", "Oryx Delivery Trip Creation Error")

#     if created_trips > 0:
#         frappe.msgprint(f"{created_trips} Oryx Delivery Trips Created and Submitted.")
#     else:
#         frappe.msgprint("No Oryx Delivery Trips were submitted.")





#working code

# import frappe
# from frappe import _

# def create_kyle_delivery_trips(doc, method):
#     """
#     Automatically create Oryx Delivery Trips when submitting a Delivery Note.
#     - Skips creation if Delivery Note is linked to a DO Form.
#     - Prevents duplicate trips if already created from linked Sales Orders.
#     - Creates one trip per vehicle entry in Delivery Note items.
#     """

#     # Skip if DO Form is linked
#     if doc.custom_do_form and frappe.db.exists("DO Form", doc.custom_do_form):
#         frappe.msgprint(f"Delivery Note is linked to DO Form {doc.custom_do_form}. Skipping Oryx Delivery Trip creation.")
#         return

#     # Get list of linked Sales Orders
#     so_list = list(set(item.against_sales_order for item in doc.items if item.against_sales_order))

#     # Check if any Oryx Delivery Trips already exist for the Sales Order(s)
#     if so_list:
#         existing_trips = frappe.get_all(
#             "Oryx Delivery Trip",
#             filters={"sales_order": ["in", so_list]},
#             pluck="sales_order"
#         )
#         if existing_trips:
#             frappe.msgprint(f"Oryx Delivery Trips already exist for Sales Order(s): {', '.join(set(existing_trips))}. Skipping creation.")
#             return

#     # Ensure items are present
#     if not doc.items:
#         frappe.msgprint("No vehicle details found in Delivery Note.")
#         return

#     created_trips = 0

#     for item in doc.items:
#         vehicle = item.custom_vehicle
#         driver = item.custom_driver
#         meter_reading = item.custom_meter_reading_before
#         after_meter_reading = item.custom_meter_reading_after   
#         before_loading = item.custom_before_loading_weight
#         after_loading = item.custom_after_loading_weight
#         loading_uom = item.custom_loading_uom
#         item_code = item.item_code
#         qty = item.custom_delivered_qty
#         row_id = item.name
#         loading_point = item.loading_point
#         address_display = item.address_display

#         # Validate vehicle and driver
#         if not vehicle or not driver:
#             frappe.msgprint(f"Skipping row {row_id}: Missing vehicle or driver.")
#             frappe.log_error(f"Missing vehicle or driver in item: {item}", "Oryx Delivery Trip Creation Error")
#             continue

#         try:
#             # Create new Oryx Delivery Trip
#             trip = frappe.new_doc("Oryx Delivery Trip")
#             trip.company = doc.company or frappe.defaults.get_user_default("Company")
#             trip.vehicle = vehicle
#             trip.driver = driver
#             trip.meter_reading_before = meter_reading
#             trip.meter_reading_after = after_meter_reading
#             trip.before_loading_weight = before_loading
#             trip.after_loading_weight = after_loading
#             trip.loading_uom = loading_uom
#             trip.delivery_note = doc.name
#             trip.sales_order = so_list[0] if so_list else None
#             trip.item_code = item_code
#             trip.qty = qty
#             trip.posting_date = doc.posting_date
#             trip.row_id = row_id
#             trip.customer = doc.customer
#             trip.address = doc.shipping_address_name
#             trip.delivery_point = loading_point
#             trip.address = address_display

#             trip.insert()
#             trip.save()
#             created_trips += 1

#             frappe.msgprint(f"Oryx Delivery Trip created and submitted for Vehicle: {vehicle}, Driver: {driver}.")

#         except frappe.ValidationError as e:
#             frappe.log_error(f"Validation Error creating Oryx Delivery Trip: {str(e)}", "Oryx Delivery Trip Creation Error")
#         except Exception as e:
#             frappe.log_error(f"Unexpected error: {str(e)}", "Oryx Delivery Trip Creation Error")

#     if created_trips > 0:
#         frappe.msgprint(f"{created_trips} Oryx Delivery Trip(s) successfully created.")
#     else:
#         frappe.msgprint("No Oryx Delivery Trips were created")





# import frappe
# from frappe import _

# def create_kyle_delivery_trips(doc, method):
#     """
#     Automatically create Oryx Delivery Trips when submitting a Delivery Note.
#     - Skips creation if Delivery Note is linked to a DO Form AND trips already exist.
#     - Prevents duplicate trips if already created from linked Sales Orders.
#     - Creates one trip per vehicle entry in Delivery Note items.
#     """

#     # Step 1: Check if DO Form is linked, and skip only if trips already exist for it
#     if doc.custom_do_form and frappe.db.exists("DO Form", doc.custom_do_form):
#         existing_do_trips = frappe.get_all(
#             "Oryx Delivery Trip",
#             filters={"do_form": doc.custom_do_form},
#             limit=1
#         )
#         if existing_do_trips:
#             frappe.msgprint(f"Oryx Delivery Trips already exist for DO Form {doc.custom_do_form}. Skipping creation.")
#             return
#         else:
#             frappe.msgprint(f"DO Form {doc.custom_do_form} is linked, but no Oryx Delivery Trips found. Proceeding with creation.")

#     # Step 2: Check for linked Sales Orders and skip if trips already created from them
#     so_list = list(set(item.against_sales_order for item in doc.items if item.against_sales_order))
#     if so_list:
#         existing_trips = frappe.get_all(
#             "Oryx Delivery Trip",
#             filters={"delivery_note": ["in", so_list]},
#             pluck="delivery_note"
#         )
#         if existing_trips:
#             frappe.msgprint(f"Oryx Delivery Trips already exist for Sales Order(s): {', '.join(set(existing_trips))}. Skipping creation.")
#             return

#     # Step 3: Validate items
#     if not doc.items:
#         frappe.msgprint("No vehicle details found in Delivery Note.")
#         return

#     created_trips = 0

#     # Step 4: Loop through Delivery Note Items
#     for item in doc.items:
#         vehicle = item.custom_vehicle
#         driver = item.custom_driver
#         meter_reading = item.custom_meter_reading_before
#         after_meter_reading = item.custom_meter_reading_after   
#         before_loading = item.custom_before_loading_weight
#         after_loading = item.custom_after_loading_weight
#         loading_uom = item.custom_loading_uom
#         item_code = item.item_code
#         qty = item.custom_delivered_qty
#         row_id = item.name
#         loading_point = item.loading_point
#         address_display = item.address_display

#         # Skip if vehicle or driver is missing
#         if not vehicle or not driver:
#             frappe.msgprint(f"Skipping row {row_id}: Missing vehicle or driver.")
#             frappe.log_error(f"Missing vehicle or driver in item: {item}", "Oryx Delivery Trip Creation Error")
#             continue

#         try:
#             # Step 5: Create and populate Oryx Delivery Trip
#             trip = frappe.new_doc("Oryx Delivery Trip")
#             trip.company = doc.company or frappe.defaults.get_user_default("Company")
#             trip.vehicle = vehicle
#             trip.driver = driver
#             trip.meter_reading_before = meter_reading
#             trip.meter_reading_after = after_meter_reading
#             trip.before_loading_weight = before_loading
#             trip.after_loading_weight = after_loading
#             trip.loading_uom = loading_uom
#             trip.delivery_note = doc.name
#             trip.sales_order = so_list[0] if so_list else None
#             trip.item_code = item_code
#             trip.qty = qty
#             trip.posting_date = doc.posting_date
#             trip.row_id = row_id
#             trip.customer = doc.customer
#             trip.address = doc.shipping_address_name
#             trip.delivery_point = loading_point
#             trip.address = address_display

#             # Link back to DO Form if applicable
#             if doc.custom_do_form:
#                 trip.do_form = doc.custom_do_form

#             trip.insert()
#             trip.save()
#             created_trips += 1

#             frappe.msgprint(f"Oryx Delivery Trip created for Vehicle: {vehicle}, Driver: {driver}.")

#         except frappe.ValidationError as e:
#             frappe.log_error(f"Validation Error creating Oryx Delivery Trip: {str(e)}", "Oryx Delivery Trip Creation Error")
#         except Exception as e:
#             frappe.log_error(f"Unexpected error: {str(e)}", "Oryx Delivery Trip Creation Error")

#     # Step 6: Summary message
#     if created_trips > 0:
#         frappe.msgprint(f"{created_trips} Oryx Delivery Trip(s) successfully created.")
#     else:
#         frappe.msgprint("No Oryx Delivery Trips were created.")



import frappe

def create_oryx_delivery_trips_from_plan(doc, method):
    """
    Automatically create Oryx Delivery Trips based on the vehicle details in the Oryx Delivery Plan.
    """

    if not doc.items:
        frappe.msgprint("No vehicle details found in the Oryx Delivery Plan.")
        return

    created_trips = 0

    for detail in doc.items:
        vehicle = detail.vehicle
        driver = detail.driver
        meter_reading = detail.meter_reading_after           # (Before Loading)
        after_meter_reading = detail.meter_readingal         # (After Loading)
        before_loading = detail.before_loading_weight
        after_loading = detail.after_loading_weight
        loading_uom = detail.loading_uom
        row_id = detail.name
        item_code = detail.item_code
        loaded_qty = detail.loaded_qty
        delivered_qty = detail.delivered_qty




        customer = doc.customer
        delivery_point = doc.delivery_point

        if not vehicle or not driver:
            frappe.log_error(
                f"Missing vehicle or driver in vehicle details row: {detail}",
                "Oryx Delivery Trip Creation Error"
            )
            continue

        try:
            trip = frappe.new_doc("Oryx Delivery Trip")
            trip.company = doc.company or frappe.defaults.get_user_default("Company")
            trip.vehicle = vehicle
            trip.driver = driver
            trip.meter_reading_before = meter_reading
            trip.meter_reading_after = after_meter_reading
            trip.before_loading_weight = before_loading
            trip.after_loading_weight = after_loading
            trip.loading_uom = loading_uom
            trip.delivery_plan = doc.name  # Link to Oryx Delivery Plan
            trip.row_id = row_id
            trip.item_code = item_code
            trip.customer = customer
            trip.delivery_point = delivery_point
            trip.loaded_quantity = loaded_qty
            trip.delivered_quantity = delivered_qty

            trip.insert()
            trip.save()
            created_trips += 1

        except frappe.ValidationError as e:
            frappe.log_error(f"Validation error: {str(e)}", "Oryx Delivery Trip Creation")
        except Exception as e:
            frappe.log_error(f"Unexpected error: {str(e)}", "Oryx Delivery Trip Creation")

    frappe.msgprint(f"{created_trips} Oryx Delivery Trips created." if created_trips else "No Oryx Delivery Trips were created.")
