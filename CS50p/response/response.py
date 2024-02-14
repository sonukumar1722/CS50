from validator_collection import validators, errors

def main():

    # Prompt the user to enter an email address.
    email_address = input("What's you email address? ")


    # Validate the email address using the validator_collection library.
    try:
        email_address = validators.email(email_address)
        print("Valid")
    except errors.InvalidEmailError:
        print("Invalid")


if __name__ == '__main__':
    main()
