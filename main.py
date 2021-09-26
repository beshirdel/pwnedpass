from passwordchecker.passwordchecker import PasswordChecker
from passwordchecker.api.pwnedpasswordcom import PwnedPasswordCom
import sys


def print_result(item):
    password, used_count, error, status = item.values()
    if error == 0:
        if used_count > 0:
            print(f"'{password}' -> \"NOT SECURE!, it has been used at least {used_count} times\"")
        else:
            print(f"'{password}' -> \"SECURE!\"")
    else:
        print(f"{password} -> \"error: {status}\"")


def main():
    passwords = sys.argv[1:]
    if passwords:
        checker = PasswordChecker(api_obj=PwnedPasswordCom())
        result = checker.check_passwords(passwords)
        print("checking passwords")
        for item in result:
            print_result(item)
        print()


if __name__ == "__main__":
    main()
