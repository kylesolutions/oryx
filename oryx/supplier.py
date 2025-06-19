import frappe
import requests
import json

@frappe.whitelist()
def generate_supplier(supplier_name):
    """
    Fetch Supplier with its Contact and Address from Site A
    and create the same in Site B.
    """
    supplier = frappe.get_doc("Supplier", supplier_name)

    # Prepare supplier core data
    supplier_data = {
        "supplier_name": supplier.supplier_name,
        "supplier_type": supplier.supplier_type,
        "supplier_group": supplier.supplier_group,
        "contacts": [],
        "addresses": []
    }

    # Fetch linked contacts
    contact_links = frappe.get_all("Dynamic Link", filters={
        "link_doctype": "Supplier",
        "link_name": supplier_name,
        "parenttype": "Contact"
    }, fields=["parent"])

    for cl in contact_links:
        contact = frappe.get_doc("Contact", cl.parent)
        supplier_data["contacts"].append({
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email_id": contact.email_id,
            "phone": contact.phone,
            "mobile_no": contact.mobile_no
        })

    # Fetch linked addresses
    address_links = frappe.get_all("Dynamic Link", filters={
        "link_doctype": "Supplier",
        "link_name": supplier_name,
        "parenttype": "Address"
    }, fields=["parent"])

    for al in address_links:
        address = frappe.get_doc("Address", al.parent)
        supplier_data["addresses"].append({
            "address_title": address.address_title,
            "address_line1": address.address_line1,
            "address_line2": address.address_line2,
            "city": address.city,
            "state": address.state,
            "pincode": address.pincode,
            "country": address.country,
            "address_type": address.address_type
        })

    # Site B API config
    site_b_url = "http://185.216.75.31:1011/api/method/oryx.supplier.create_supplier_with_contact_and_address"
    api_key = "92312e181443484"
    api_secret = "890cbabf643b93a"

    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(site_b_url, json=supplier_data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            frappe.throw(
                f"Failed to sync to Site B (Status Code: {response.status_code}): {response.text}"
            )
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Connection error to Site B: {str(e)}")

@frappe.whitelist(allow_guest=True)
def create_supplier_with_contact_and_address():
    import json
    from frappe.utils import nowdate

    data = json.loads(frappe.request.data)
    
    supplier = frappe.new_doc("Supplier")
    supplier.update({
        "supplier_name": data["supplier_name"],
        "supplier_type": data["supplier_type"],
        "supplier_group": data["supplier_group"],
    })
    supplier.insert(ignore_permissions=True)

    # Create Address
    for addr in data.get("addresses", []):
        address = frappe.new_doc("Address")
        address.update(addr)
        address.append("links", {
            "link_doctype": "Supplier",
            "link_name": supplier.name
        })
        address.insert(ignore_permissions=True)

    # Create Contact
    for con in data.get("contacts", []):
        contact = frappe.new_doc("Contact")
        contact.update(con)
        contact.append("links", {
            "link_doctype": "Supplier",
            "link_name": supplier.name
        })
        contact.insert(ignore_permissions=True)

    return {"status": "success", "supplier": supplier.name}
