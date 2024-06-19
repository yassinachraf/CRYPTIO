import sys
from get_label_ids import get_label_ids
from process_movements import process_movements
from remove_labels import remove_label
import add_a_note

base_url = "https://app-api.cryptio.co/api"
headers = {
    "content-type": "application/json",
    "cryptio-api-key": "2e737658-575d-4b42-8625-616c5f115cb5"
}

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

def main():
    transaction_hash = input("Do you want to apply the 'Ignore' label if the balance of all asset movements is zero, and 'Revenue' otherwise? If so, please provide the transaction hash here: ")
    
    confirmation = get_confirmation('Do you want to proceed? Enter "Y" to confirm or "N" to cancel: ', 3)
    if confirmation is True:
        revenue_label_id, ignore_label_id, revenue_label_name, ignore_label_name = get_label_ids(base_url, headers)
        process_movements(base_url, headers, transaction_hash, revenue_label_id, ignore_label_id, revenue_label_name, ignore_label_name)

        retain_labels = get_confirmation('Do you want to retain the labels? Enter "Y" to confirm or "N" to remove: ', 3)
        if retain_labels is True:
            print("Labels retained.")
        elif retain_labels is False:
            remove_label(base_url, [transaction_hash], headers["cryptio-api-key"], revenue_label_id, revenue_label_name)
            remove_label(base_url, [transaction_hash], headers["cryptio-api-key"], ignore_label_id, ignore_label_name)
            print("Labels removed.")
        else:
            print("You have used all your attempts. Request cancelled. Restart the process.")
            sys.exit()
        
        add_note_confirmation = get_confirmation('Do you want to add a note? Enter "Y" to confirm or "N" to cancel: ', 3)
        if add_note_confirmation is True:
            add_a_note.add_note_with_hash(transaction_hash)
        elif add_note_confirmation is False:
            print("Labels applied and no note added.")
        else:
            print("You have used all your attempts. Labels applied and no note added.")
    elif confirmation is False:
        print("Request cancelled")
        sys.exit()
    else:
        print("You have used all your attempts. Request cancelled. Restart the process.")
        sys.exit()

if __name__ == "__main__":
    main()
