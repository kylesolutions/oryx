import frappe
import requests
import json

@frappe.whitelist()
def generate_account(account_name):
    """
    Fetch Account from Site A and create the same Account in Site B.
    """
    # Fetch account from Site A
    account = frappe.get_doc("Account", account_name)

    # Prepare data to send to Site B
    account_data = {
        "account_name": account.account_name,
        "account_number": account.account_number,
        "account_type": account.account_type,
        "company": account.company,
        "parent_account": account.parent_account,
        "is_group": account.is_group,
        "root_type": account.root_type
    }

    # Site B credentials and endpoint
    site_b_url = "http://185.216.75.31:1011/api/resource/Account"
    api_key = "92312e181443484"
    api_secret = "890cbabf643b93a"

    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(site_b_url, json=account_data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            frappe.throw(f"Failed to create Account in Site B (Status Code: {response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Error while connecting to Site B: {str(e)}")
