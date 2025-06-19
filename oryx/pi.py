import frappe
import requests
import json
from datetime import datetime

@frappe.whitelist()
def generate_purchase_invoice(purchase_invoice_name):
    """
    Fetch Purchase Invoice details from Site A and create the same invoice in Site B.
    """
    # Get the Purchase Invoice
    pi = frappe.get_doc("Purchase Invoice", purchase_invoice_name)

    # Prepare Purchase Invoice data
    pi_data = {
        "supplier": pi.supplier,
        "posting_date": pi.posting_date.strftime("%Y-%m-%d"),
        "due_date": pi.due_date.strftime("%Y-%m-%d") if pi.due_date else None,
        "bill_no": pi.bill_no,
        "bill_date": pi.bill_date.strftime("%Y-%m-%d") if pi.bill_date else None,
        "company": pi.company,
        "currency": pi.currency,
        "conversion_rate": pi.conversion_rate,
        "taxes_and_charges": pi.taxes_and_charges,
        "items": [],
        "taxes": []
    }

    # Items
    for item in pi.items:
        pi_data["items"].append({
            "item_code": item.item_code,
            "item_name": item.item_name,
            "description": item.description,
            "qty": item.qty,
            "rate": item.rate,
            "uom": item.uom,
            "amount": item.amount,
            "cost_center": item.cost_center
        })

    # Taxes
    for tax in pi.taxes:
        pi_data["taxes"].append({
            "charge_type": tax.charge_type,
            "account_head": tax.account_head,
            "description": tax.description,
            "rate": tax.rate,
            "tax_amount": tax.tax_amount,
            "total": tax.total
        })

    # Site B API endpoint
    site_b_url = "http://185.216.75.31:1011/api/resource/Purchase Invoice"
    api_key = "92312e181443484"
    api_secret = "890cbabf643b93a"

    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(site_b_url, json=pi_data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            frappe.throw(
                f"Failed to create Purchase Invoice in Site B (Status Code: {response.status_code}): {response.text}"
            )
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Error connecting to Site B: {str(e)}")
