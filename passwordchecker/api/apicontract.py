class ApiContract:

    @classmethod
    def make_result(cls, password, count, error_no):
        return f"{password},{count},{error_no}"

    @classmethod
    def get_error(cls, code):
        return "OK"
