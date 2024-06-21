# remove_labels.py
import requests

def remove_label(base_url, transaction_hashes, api_key, label_id, label_name):
    url = f"{base_url}/label/{label_id}/remove"
    payload = {"transaction_hashes": transaction_hashes}
    headers = {
        "content-type": "application/json",
        "cryptio-api-key": api_key
    }

    try:
        response = requests.delete(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"The following label has been removed: {label_name}.")
        print(response.text)
    except requests.RequestException as e:
        print(f"Failed to remove label {label_name}: {e}")
