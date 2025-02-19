# import frappe

# def create_kyle_delivery_trips(doc, method):
#     """
#     Automatically create Kyle Delivery Trips from the submitted Delivery Note
#     """
#     if not doc.custom_kyle_vehicle_details:
#         frappe.msgprint("No vehicle details found in custom_kyle_vehicle_details.")
#         return

#     for vehicle_detail in doc.custom_kyle_vehicle_details:
#         vehicle = vehicle_detail.vehicle
#         driver = vehicle_detail.driver

#         # Create Kyle Delivery Trip
#         kyle_trip = frappe.new_doc("Kyle Delivery Trip")
#         kyle_trip.company = doc.company or frappe.defaults.get_user_default("Company")
#         kyle_trip.vehicle = vehicle
#         kyle_trip.driver = driver
#         kyle_trip.posting_date = doc.posting_date
#         kyle_trip.posting_time = doc.posting_time

#         # Reference the delivery note
#         kyle_trip.delivery_note = doc.name

#         # Add stops for the Kyle Delivery Trip
#         for item in doc.items:
#             kyle_trip.append("kyle_delivery_stop", {
#                 "customer": doc.customer,  # Ensure customer is fetched
#                 "item_code": item.item_code,
#                 "quantity": item.qty
#             })

#         # Save and Submit the Kyle Delivery Trip
#         kyle_trip.insert()
#         kyle_trip.submit()

#     frappe.msgprint(f"{len(doc.custom_kyle_vehicle_details)} Kyle Delivery Trips Created.")







import frappe

def create_kyle_delivery_trips(doc, method):
    """
    Automatically create Kyle Delivery Trips from the submitted Delivery Note
    """
    if not doc.custom_kyle_vehicle_details:
        frappe.msgprint("No vehicle details found in custom_kyle_vehicle_details.")
        return

    created_trips = 0

    for vehicle_detail in doc.custom_kyle_vehicle_details:
        vehicle = vehicle_detail.vehicle
        driver = vehicle_detail.driver

        kyle_trip = frappe.new_doc("Kyle Delivery Trip")
        kyle_trip.company = doc.company or frappe.defaults.get_user_default("Company")
        kyle_trip.vehicle = vehicle
        kyle_trip.driver = driver
        kyle_trip.posting_date = doc.posting_date
        kyle_trip.posting_time = doc.posting_time
        kyle_trip.delivery_note = doc.name

        for item in doc.items:
            kyle_trip.append("kyle_delivery_stop", {
                "customer": doc.customer,
                "item_code": item.item_code,
                "quantity": item.qty
            })

        try:
            kyle_trip.insert()
            kyle_trip.save()
            
            created_trips += 1
        except frappe.ValidationError as e:
            frappe.log_error(f"Error creating Kyle Delivery Trip: {str(e)}", "Kyle Delivery Trip Creation Error")

    if created_trips > 0:
        frappe.msgprint(f"{created_trips} Kyle Delivery Trips Created and Submitted.")
    else:
        frappe.msgprint("No Kyle Delivery Trips were submitted.")
