import requests
import hashlib
from passwordchecker.api.apicontract import ApiContract


class PwnedPasswordCom(ApiContract):
    _api = "https://api.pwnedpasswords.com/range/"
    CONNECTION_ERROR = -1
    HTTP_ERROR = -2
    ERRORS = {
        0: "OK",
        CONNECTION_ERROR: 'internet connection failed',
        HTTP_ERROR: 'api doesn\'t respond!'
    }

    def check(self, password):
        hashed_password = self.get_hash(password)
        link = self.get_link(hashed_password)
        result = self.get_result(link)
        return self.parse_result(password, hashed_password, result)

    def get_hash(self, password):
        return hashlib.sha1(password.encode("UTF-8")).hexdigest().upper()

    def get_link(self, hashed_password):
        return self._api + hashed_password[:5]

    def get_result(self, link):
        try:
            res = requests.get(link)
            if res.status_code != 200:
                raise self.HTTP_ERROR
        except requests.exceptions.ConnectionError:
            return self.CONNECTION_ERROR

        else:
            return res.text

    def parse_result(self, password, hashed_password, result):
        # error happened
        if isinstance(result, int):
            return self.make_result(password, 999, result)

        return self.make_result(password, self.find_password_used_count(hashed_password, result), 0)

    def find_password_used_count(self, hashed_password, hashed_passwords_text):

        hashed_passwords_text = hashed_passwords_text.strip()
        if len(hashed_passwords_text) == 0:
            return 0

        hash_tail = hashed_password[5:]
        hashed_passwords_list = (line.split(':') for line in hashed_passwords_text.splitlines())
        for hash, count in hashed_passwords_list:
            if hash == hash_tail:
                return int(count)
        return 0

    @classmethod
    def get_error(cls, code):
        return cls.ERRORS.get(code)
