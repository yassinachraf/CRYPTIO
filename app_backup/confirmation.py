# confirmation.py

def get_confirmation(prompt, allow_return=False, previous_question=None):
    while True:
        user_input = input(prompt + ' (Y/N' + ('/B' if allow_return else '') + '): ')
        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False
        elif allow_return and user_input.lower() == 'b':
            if previous_question:
                return previous_question()
            else:
                print("No previous question to return to.")
        else:
            print("Invalid input. Please enter 'Y', 'N'" + (", or 'B'" if allow_return else '') + ".")

def retain_labels():
    return get_confirmation('Do you want to retain the labels? Enter "Y" to confirm or "N" to remove: ')

# Example usage of get_confirmation with return option
def example_question():
    print("This is the previous question.")
    # Proceed with whatever logic needed for the previous question
    return get_confirmation('Is this the correct answer?', allow_return=True, previous_question=retain_labels)
