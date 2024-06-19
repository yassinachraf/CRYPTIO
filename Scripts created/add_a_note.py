import requests

# Function to get user input for transaction hash and note
def get_user_inputs():
    transaction_hash = input("Please provide the transaction hash: ")
    note = input("Type the note here: ")
    return transaction_hash, note

# Function to get confirmation from the user
def get_confirmation(attempts):
    for attempt in range(attempts):
        confirm = input("Do you confirm? Y/N: ")
        if confirm.upper() == "Y":
            return True
        elif confirm.upper() == "N":
            return False
        else:
            remaining_attempts = attempts - (attempt + 1)
            print(f'Answer must be "Y" to confirm, "N" to cancel. You have {remaining_attempts} attempts left.')
    return None

# Main script logic
def main():
    while True:
        transaction_hash, note = get_user_inputs()

        if transaction_hash and note:
            confirmation = get_confirmation(3)

            if confirmation is True:
                url = "https://app-api.cryptio.co/api/transaction/notes"

                payload = {
                    "notes": [
                        {
                            "transaction_hashes": [transaction_hash],
                            "note": note
                        }
                    ]
                }
                headers = {
                    "content-type": "application/json",
                    "cryptio-api-key": "2e737658-575d-4b42-8625-616c5f115cb5"
                }

                response = requests.put(url, json=payload, headers=headers)

                print("Note added")
                break
            elif confirmation is False:
                print("Request cancelled")
                break
            else:
                print("You have used all your attempts. Request cancelled. Restarted the process.")
        else:
            print("Both transaction hash and note must be provided.")

if __name__ == "__main__":
    main()
