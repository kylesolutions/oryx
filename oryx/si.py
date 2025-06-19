import frappe
import requests
import json
from frappe.utils import getdate

@frappe.whitelist()
def generate_sales_invoice(sales_invoice_name):
    """
    Generate a Sales Invoice in Site B based on the Sales Invoice in Site A.

    Args:
        sales_invoice_name (str): The name of the Sales Invoice in Site A.

    Returns:
        dict: Response message indicating success or failure.
    """
    try:
        # Fetch Sales Invoice from Site A
        sales_invoice = frappe.get_doc("Sales Invoice", sales_invoice_name)

        # ✅ Check if a reference already exists (to prevent duplicate creation)
        if sales_invoice.custom_reference_code:
            return {
                "message": f"Sales Invoice already created in Site B: {sales_invoice.custom_reference_code}"
            }

        # Prepare request data for Site B
        sales_invoice_data = {
            "doctype": "Sales Invoice",
            "customer": sales_invoice.customer,
            "posting_date": str(sales_invoice.posting_date),
            "currency": sales_invoice.currency,
            "conversion_rate": sales_invoice.conversion_rate or 1,  
            "items": [
                {
                    "item_code": item.item_code,
                    "qty": item.qty,
                    "rate": item.rate,
                    "income_account": item.income_account
                }
                for item in sales_invoice.items
            ] if sales_invoice.items else [],
            "company": sales_invoice.company,
            "debit_to": sales_invoice.debit_to or get_default_debit_to(sales_invoice.company),
            "custom_reference": sales_invoice.name  
        }

        # Site B API credentials
        site_b_url = "http://185.216.75.31:1011/api/resource/Sales Invoice"
        api_key = "92312e181443484"
        api_secret = "890cbabf643b93a"

        # Set headers for API request
        headers = {
            "Authorization": f"token {api_key}:{api_secret}",
            "Content-Type": "application/json"
        }

        # Send request to Site B
        response = requests.post(site_b_url, data=json.dumps(sales_invoice_data), headers=headers)

        # Handle response
        if response.status_code == 200:
            response_data = response.json()
            
            # Extract the created invoice ID
            site_b_invoice_name = response_data.get("data", {}).get("name")
            if site_b_invoice_name:
                # ✅ Update Site A with Site B's invoice number
                frappe.db.set_value("Sales Invoice", sales_invoice_name, "custom_reference_code", site_b_invoice_name)
                frappe.db.commit()
                return {"message": f"Sales Invoice {site_b_invoice_name} created in Site B and updated in Site A."}
            else:
                frappe.throw("Sales Invoice created, but response does not contain an invoice name.")

        else:
            error_message = f"Failed to create Sales Invoice in Site B (Status Code: {response.status_code}): {response.text}"
            frappe.throw(error_message)

    except requests.exceptions.RequestException as e:
        frappe.throw(f"Error connecting to Site B: {str(e)}")

    except frappe.DoesNotExistError:
        frappe.throw("Sales Invoice does not exist in Site A.")

    except Exception as e:
        frappe.throw(f"An unexpected error occurred: {str(e)}")

def get_default_debit_to(company):
    """
    Get the default 'Debit To' account for a company.

    Args:
        company (str): The name of the company.

    Returns:
        str: The default Debit To account.
    """
    default_account = frappe.db.get_value('Company', company, 'default_receivable_account')
    return default_account or "Debtors - O"
