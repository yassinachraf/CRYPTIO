import requests

def get_user_inputs():
    note = input("Type the note here: ")
    return note

def get_confirmation(prompt, attempts):
    for attempt in range(attempts):
        confirm = input(prompt)
        if confirm.upper() == "Y":
            return True
        elif confirm.upper() == "N":
            return False
        else:
            remaining_attempts = attempts - (attempt + 1)
            print(f'Answer must be "Y" to confirm, "N" to cancel. You have {remaining_attempts} attempts left.')
    return None

def add_note_with_hash(transaction_hash):
    while True:
        note = get_user_inputs()

        if note:
            confirmation = get_confirmation("Do you confirm? Y/N: ", 3)

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
                print("You have used all your attempts. Request cancelled. Restart the process.")
        else:
            print("Note must be provided.")
