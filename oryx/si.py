import frappe
import requests
from frappe.utils import getdate

@frappe.whitelist()
def generate_sales_invoice(sales_invoice_name):
    """
    Generate a Sales Invoice in Site B based on the Sales Invoice in Site A.

    Args:
        sales_invoice_name (str): The name of the Sales Invoice in Site A.

    Returns:
        dict: The response from Site B on successful creation of the Sales Invoice.
    """
    # Get the Sales Invoice details from Site A
    sales_invoice = frappe.get_doc("Sales Invoice", sales_invoice_name)

    # Prepare data for Site B
    sales_invoice_data = {
        "doctype": "Sales Invoice",
        "customer": sales_invoice.customer,
        "posting_date": str(sales_invoice.posting_date),
        "currency": sales_invoice.currency,  # Ensure currency is passed
        "conversion_rate": sales_invoice.conversion_rate or 1,  # Default to 1 if not set
        "items": [
            {
                "item_code": item.item_code,
                "qty": item.qty,
                "rate": item.rate,
                "income_account": item.income_account or "Sales from Other Region - O"
            }
            for item in sales_invoice.items
        ],
        "company": sales_invoice.company,
        "debit_to": sales_invoice.debit_to or get_default_debit_to(sales_invoice.company),  # Use default if missing
        "custom_reference":sales_invoice.name
    }

    # Site B API credentials
    site_b_url = "http://109.199.100.136:1011/api/resource/Sales Invoice"
    api_key = "c921736221b267d"
    api_secret = "3a0b977b62167a4"

    # Set headers for the request
    headers = {
        "Authorization": f"token c921736221b267d:3a0b977b62167a4",
        "Content-Type": "application/json"
    }

    # Send the request to Site B
    try:
        response = requests.post(site_b_url, json=sales_invoice_data, headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            return response.json()
        else:
            frappe.throw(
                f"Failed to create Sales Invoice in Site B (Status Code: {response.status_code}): {response.text}"
            )
    except requests.exceptions.RequestException as e:
        # Handle connectivity errors
        frappe.throw(f"An error occurred while connecting to Site B: {str(e)}")

def get_default_debit_to(company):
    """
    Get the default Debit To account for a company.
    This function can be customized as needed.

    Args:
        company (str): The name of the company in Site B.

    Returns:
        str: The default Debit To account for the company.
    """
    # You can query the default account based on company or other parameters
    # Example: Retrieve the default receivable account for the company
    default_account = frappe.db.get_value('Company', company, 'default_receivable_account')
    if not default_account:
        # Fallback to a known default account if not set
        return "Debtors - O"
    return default_account





