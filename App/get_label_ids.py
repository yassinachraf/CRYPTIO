# get_label_ids.py
import requests

def get_label_ids(base_url, headers):
    label_url = f"{base_url}/label"
    response = requests.get(label_url, headers=headers)
    labels = response.json()["data"]

    revenue_label = list(filter(lambda x: x["name"].lower() == "revenue", labels))
    ignore_label = list(filter(lambda x: x["name"].lower() == "ignore", labels))

    revenue_label_id = revenue_label[0]["id"] if revenue_label else None
    ignore_label_id = ignore_label[0]["id"] if ignore_label else None

    return revenue_label_id, ignore_label_id, "revenue" if revenue_label else None, "ignore" if ignore_label else None