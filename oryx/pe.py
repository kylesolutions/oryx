import frappe
import requests
import json
from datetime import datetime

@frappe.whitelist()
def generate_payment_entry(payment_entry_name):
    """
    Fetch Payment Entry from Site A and create it in Site B.
    """
    # Fetch the Payment Entry from Site A
    pe = frappe.get_doc("Payment Entry", payment_entry_name)

    # Prepare data
    pe_data = {
        "payment_type": pe.payment_type,
        "party_type": pe.party_type,
        "party": pe.party,
        "posting_date": pe.posting_date.strftime("%Y-%m-%d"),
        "paid_from": pe.paid_from,
        "paid_to": pe.paid_to,
        "paid_amount": pe.paid_amount,
        "received_amount": pe.received_amount,
        "target_exchange_rate": pe.target_exchange_rate,
        "source_exchange_rate": pe.source_exchange_rate,
        "reference_no": pe.reference_no,
        "reference_date": pe.reference_date.strftime("%Y-%m-%d") if pe.reference_date else None,
        "remarks": pe.remarks,
        "company": pe.company,
        "mode_of_payment": pe.mode_of_payment,
        "party_bank_account": pe.party_bank_account,
        "references": []
    }

    for ref in pe.references:
        pe_data["references"].append({
            "reference_doctype": ref.reference_doctype,
            "reference_name": ref.reference_name,
            "total_amount": ref.total_amount,
            "outstanding_amount": ref.outstanding_amount,
            "allocated_amount": ref.allocated_amount
        })

    # Site B API endpoint
    site_b_url = "http://185.216.75.31:1011/api/resource/Payment Entry"
    api_key = "92312e181443484"
    api_secret = "890cbabf643b93a"

    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(site_b_url, json=pe_data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            frappe.throw(
                f"Failed to create Payment Entry in Site B (Status Code: {response.status_code}): {response.text}"
            )
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Error connecting to Site B: {str(e)}")
