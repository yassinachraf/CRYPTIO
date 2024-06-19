# confirmation.py

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
