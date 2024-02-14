import re
import sys


def main():
    # Prompt the user for an IPv4 address and print the validation result
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    try:
        # Split the IP address into octets
        ip_bytes = ip.split('.')

        for byte in ip_bytes:
            # Check if each octet is a number and the IP has 4 octets
            if is_number(byte) and len(ip_bytes) == 4:
                # Check if the octet is within the valid range (0-255)
                if not 0 <= int(byte) <= 255:
                    return False
            else:
                return False

        return True  # If all octets are valid, return True
    except:
        return False  # Catch any exceptions (e.g., if the input is not a string)


def is_number(byte):
    try:
        # Attempt to convert the octet to an integer
        int(byte)
        return True
    except:
        return False


if __name__ == "__main__":
    main()
