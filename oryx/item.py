import frappe
import requests
import json

@frappe.whitelist()
def generate_item(item_code):
    """
    Fetch Item details from Site A and create the same Item in Site B.
    """
    # Get the Item details from Site A
    item = frappe.get_doc("Item", item_code)

    # Prepare data for Site B
    item_data = {
        "item_code": item.item_code,
        "item_name": item.item_name,
        "item_group": item.item_group,
        "stock_uom": item.stock_uom,
        "description": item.description or "",
        "is_stock_item": item.is_stock_item,
        "disabled": item.disabled
    }

    # Site B API credentials and URL
    site_b_url = "http://185.216.75.31:1011/api/resource/Item"
    api_key = "92312e181443484"
    api_secret = "890cbabf643b93a"

    # Set headers for the request
    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }

    # Send the request to Site B
    try:
        response = requests.post(site_b_url, json=item_data, headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            return response.json()
        else:
            frappe.throw(
                f"Failed to create Item in Site B (Status Code: {response.status_code}): {response.text}"
            )
    except requests.exceptions.RequestException as e:
        # Handle connectivity errors
        frappe.throw(f"An error occurred while connecting to Site B: {str(e)}")
