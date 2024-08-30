import json
import sys


class Get:
    def __init__(self):
        pass

    def token(self):
        try:
            with open("token.tok", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            with open("token.tok", "w") as f:
                f.write("\n")
                print("Токен не найден. Пожалуйста, зайдите в свой аккаунт")

    def data(self):
        try:
            with open("data.json", "r") as f:
                if f.read().strip():
                    f.seek(0)
                    data = json.load(f)
                    return data
                else:
                    self._write_default_data()
                    with open("data.json", "r") as fi:
                        data = json.load(fi)
                    print(data)
                    return data
        except FileNotFoundError:
            self._write_default_data()
            with open("data.json", "r") as fi:
                data = json.load(fi)
            print(data)
            return data

    def _write_default_data(self):
        default_data = {"OS": sys.platform, "show-id": False}
        with open("data.json", "w") as f:
            json.dump(default_data, f, indent=4)
