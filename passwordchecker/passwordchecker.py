import concurrent.futures



class PasswordChecker:

    def __init__(self, api_obj):
        self.api_obj = api_obj

    def check_passwords(self, password_list):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.map(self.api_obj.check, password_list)

        def result_generator():
            for item in result:
                yield self.make_dict_result(item)
            return StopIteration

        return result_generator()

    @classmethod
    def make_result(cls, password, count, error_no):
        return f"{password},{count},{error_no}"

    def make_dict_result(self, item):
        li = item.split(",")
        return {
            "password": li[0],
            "used_count": int(li[1]),
            "error": int(li[2]),
            "status": self.api_obj.get_error(int(li[2]))
        }



