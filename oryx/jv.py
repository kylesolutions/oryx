import frappe
import requests
import json

@frappe.whitelist()
def generate_journal_entry(journal_entry_name):
    """
    Fetch Journal Entry details from Site A and create the same Journal Entry in Site B.
    """
    # Get the Journal Entry document from Site A
    je = frappe.get_doc("Journal Entry", journal_entry_name)

    # Prepare Journal Entry data for Site B
    je_data = {
        "posting_date": je.posting_date.strftime("%Y-%m-%d"),
        "voucher_type": je.voucher_type,
        "company": je.company,
        "remark": je.remark or "",
        "accounts": []
    }


    # Copy accounts child table
    for row in je.accounts:
        je_data["accounts"].append({
            "account": row.account,
            "debit_in_account_currency": row.debit_in_account_currency,
            "credit_in_account_currency": row.credit_in_account_currency,
            "party_type": row.party_type,
            "party": row.party,
            "reference_type": row.reference_type,
            "reference_name": row.reference_name,
            "cost_center": row.cost_center,
            "user_remark": row.user_remark,
            # if any date field like reference_date exists:
            # "reference_date": row.reference_date.strftime("%Y-%m-%d") if row.reference_date else None
        })


    # Site B API credentials and URL
    site_b_url = "http://185.216.75.31:1011/api/resource/Journal Entry"
    api_key = "92312e181443484"
    api_secret = "890cbabf643b93a"

    # Set headers for the request
    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }

    # Send the request to Site B
    try:
        response = requests.post(site_b_url, json=je_data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            frappe.throw(
                f"Failed to create Journal Entry in Site B (Status Code: {response.status_code}): {response.text}"
            )
    except requests.exceptions.RequestException as e:
        frappe.throw(f"An error occurred while connecting to Site B: {str(e)}")
