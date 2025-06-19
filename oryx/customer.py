import frappe
import requests
import json

@frappe.whitelist()
def generate_customer(customer_name):
    """
    Fetch customer details from Site A and create the same customer in Site B.
    """
    # Get the Customer details from Site A
    customer = frappe.get_doc("Customer", customer_name)

    # Prepare data for Site B
    customer_data = {
        "customer_name": customer.customer_name,
        "customer_type": customer.customer_type,
        "customer_group": customer.customer_group,
        "territory": customer.territory or "Default Territory"
    }

     # Site B API credentials
    site_b_url = "http://185.216.75.31:1011/api/resource/Customer"
    api_key = "92312e181443484"
    api_secret = "890cbabf643b93a"

    # Set headers for the request
    headers = {
        "Authorization": f"token 92312e181443484:890cbabf643b93a",
        "Content-Type": "application/json"
    }


    # Send the request to Site B
    try:
        response = requests.post(site_b_url, json=customer_data, headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            return response.json()
        else:
            frappe.throw(
                f"Failed to create Customer in Site B (Status Code: {response.status_code}): {response.text}"
            )
    except requests.exceptions.RequestException as e:
        # Handle connectivity errors
        frappe.throw(f"An error occurred while connecting to Site B: {str(e)}")
