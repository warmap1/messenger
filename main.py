import os
import sys
import subprocess
import requests
import json
from get import Get
from menu import menu
from errors import errors

if os.path.isfile("token.tok"):
    pass
else:
    with open("token.tok", "w") as f:
        f.write("\n")
        print('Пожалуйста, зайдите в Ваш аккаунт или зарегистрируйте новый если у вас его нет перед использованием.')

# VARIABLES
get = Get()
host = "https://messanger-api-cjg0.onrender.com/"

platform = get.data()["OS"]
show_id = get.data()["show-id"]
show_id_file = show_id


def main():
    while True:
        token = get.token()
        menu(1, show_id)
        choice = input("Выбери действие: ")

        if choice == "1":  # ВХОД
            name = input("Юзернейм (A-z 0-9): ")
            password = input("Пароль (A-z 0-9): ")
            resp = requests.get(f"{host}/login?username={name}&password={password}")
            errors(1, resp)

        elif choice == "2":  # РЕГИСТРАЦИЯ
            name = input("Имя (от 4-х символов, A-z 0-9, >exit чтобы выйти): ")
            if name != ">exit":
                password = input("Пароль (от 6-и символов, A-z 0-9, >exit чтобы выйти): ")
                if password != ">exit":
                    resp = requests.get(f"{host}/register?username={name}&password={password}")
                    errors(2, resp)
                else: pass
            else: pass

        elif choice == "3":  # ПРОЧИТАТЬ СООБЩЕНИЯ
            resp = requests.get(f"{host}/read_messages?token={token}")
            errors(3, resp)

        elif choice == "4":  # НАПИСАТЬ СООБЩЕНИЕ
            message = input("Введите сообщение (>exit для выхода): ")
            if message != ">exit":
                resp = requests.get(f"{host}/add_message?message={message}&token={token}")
                errors(4, resp)
            else: pass

        elif choice == "5":
            req = reqests.get(f"{host}/admin?token={token}&allow=False")
            errors(5, req)

        elif choice == "6":
            while True:
                menu(2, show_id)
                setting = input("Введите новое значение по примеру выше: ")
                setting = setting.split()
                if setting[0] == "1":
                    if setting[1] == "True" or "False":
                        show_id == setting[1]
                        with open("data.json", "w") as f:
                            f.write("\n")
                            data = {"OS": platform, "show-id": show_id}
                            json.dump(data, f, indent=4)

                    else: print("Неверное значение!")

                if setting[0] == "0": break
        elif choice == "0": break
        else: print("Неверный выбор, попробуй снова.")

if __name__ == "__main__":
    main()
