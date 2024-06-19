import requests

def get_confirmation(prompt, attempts=3):
    for attempt in range(attempts):
        confirm = input(prompt).strip().upper()
        if confirm == "Y":
            return True
        elif confirm == "N":
            return False
        else:
            remaining_attempts = attempts - (attempt + 1)
            print(f'Input must be "Y" to confirm or "N" to cancel. You have {remaining_attempts} attempts left.')
    return None

def remove_label(url, transaction_hashes, api_key, label_name):
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

# Get transaction hash from the user
transaction_hash = input("Please enter the transaction hash: ").strip()

# Confirm the transaction hash
confirmation_prompt = f"Please confirm removal of labels for the transaction hash: '{transaction_hash}' by typing 'Y' to proceed or 'N' to cancel: "
if get_confirmation(confirmation_prompt):
    # Define the URLs and API key
    url1 = "https://app-api.cryptio.co/api/label/18f3bc7a-2165-4cb3-8f4d-6c21fd9ea322/remove"
    url2 = "https://app-api.cryptio.co/api/label/845eb3d0-2f73-4848-93fe-2f90efbc4d43/remove"
    api_key = "2e737658-575d-4b42-8625-616c5f115cb5"
    
    # Remove labels using the defined URLs
    remove_label(url1, [transaction_hash], api_key, "REVENUE")
    remove_label(url2, [transaction_hash], api_key, "IGNORE")
else:
    print("Operation cancelled.")
