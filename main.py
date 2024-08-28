import os
import sys
import subprocess
import requests
import json

# IDK
def menu(number):
    if number == 1:
        print("=== МЕНЮ ===")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Прочитать сообщения")
        print("4. Написать сообщение")
        print("5. Действия администратора")
        print("6. Настройки")
        print("0. Выйти\n")
    elif number == 2:
        print('\n=== НАСТРОЙКИ ===')
        print(f'1. Показ ID у сообщений - True/False - сейчас {show_id}')
        print('0. Выход в меню')
        print('Чтобы поменять параметр введите его номер и новое значение (1 True)')

if os.path.isfile('token.tok'): pass
else: 
    with open('token.tok', 'w') as f:
        f.write('\n')

class Get:
    def __init__(self):
        pass

    def token(self):
        try:
            with open('token.tok', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            with open('token.tok', 'w') as f:
                f.write('\n')
                print('Токен не найден. Пожалуйста, зайдите в свой аккаунт')

    def data(self):
        try:
            with open('data.json', 'r') as f:
                if f.read().strip():
                    f.seek(0)
                    data = json.load(f)
                    return data
                else:
                    self._write_default_data()
                    with open('data.json', 'r') as fi:
                        data = json.load(fi)
                    print(data)
                    return data
        except FileNotFoundError:
            self._write_default_data()
            with open('data.json', 'r') as fi:
                data = json.load(fi)
            print(data)
            return data

    def _write_default_data(self):
        default_data = {
            'OS': sys.platform,
            'show-id': False
        }
        with open('data.json', 'w') as f:
            json.dump(default_data, f, indent=4)

# VARIABLES
get = Get()
host = "https://messanger-api-cjg0.onrender.com/"

# if token: pass
# else: print('Токен отсутствует!')
platform = get.data()["OS"]
show_id = get.data()["show-id"]
show_id_file = show_id

def main():
    while True:
        # if platform == 'linux':
        #     subprocess.run('clear', shell=True)
        # elif platform == 'win32' or 'win' in platform:
        #     subprocess.run('cls', shell=True)

        token = get.token()
        menu(1)
        choice = input("Выбери действие: ")

        if choice == '1': # ВХОД
            name = input("Юзернейм (A-z 0-9): ")
            password = input("Пароль (A-z 0-9): ")
            resp = requests.get(f'{host}/login?username={name}&password={password}')
            if resp.status_code == 400 or (resp.headers.get('Conent-Type') == 'application/json' and resp.json().get('status') == 400):
                if   resp.json().get('error') == 'username is required'                 : print('Юзернейм отсутствует')
                elif resp.json().get('error') == 'password is required'                 : print('Пароль отсутствует')
                elif resp.json().get('error') == 'name wrote incorrectly'               : print('Юзернейм написан не правильно')
                elif resp.json().get('error') == 'password wrote incorrectly'           : print('Пароль написан не правильно')
                elif resp.json().get('error') == 'name or password is incorrect'        : print('Юзернейм или парлоль не правильный')
            elif     resp.status_code         == 500 or (resp.headers.get('Content-Type') == 'application/json' and resp.json().get('status') == 409):
                if   resp.json().get('error') == 'unexpected error'                     : print('На сервере произошла непредвиденная ошибка')
            elif     resp.status_code         == 200 or resp.json()['status'] == 200    :
                got_token = resp.json()['token']
                with open('token.tok', 'w') as f:
                    f.write(got_token)
                print('Вход произошёл успешно!')

        elif choice == '2': # РЕГИСТРАЦИЯ
            name = input("Имя (от 4-х символов, A-z 0-9, >exit чтобы выйти): ")
            if name != '>exit':
                password = input("Пароль (от 6-и символов, A-z 0-9, >exit чтобы выйти): ")
                if password != '>exit':
                    resp = requests.get(f'{host}/register?username={name}&password={password}')
                    if resp.status_code == 400 or (resp.headers.get('Content-Type') == 'application/json' and resp.json().get('status') == 400):
                        if   resp.json().get('error') == 'username is required'                                                    : print('Юзернейм отсутствует')
                        elif resp.json().get('error') == 'password is required'                                                    : print('Пароль отсутствует')
                        elif resp.json().get('error') == 'username is too short'                                                   : print('Юзернейм слишком короткий')
                        elif resp.json().get('error') == 'password is too short'                                                   : print('Пароль слишком короткий')
                        elif resp.json().get('error') == 'username is incorrect'                                                   : print('Юзернейм написан не правильно. Исспользуйте только буквы от A до z и числа от 0 до 9')
                        elif resp.json().get('error') == 'password is incorrect'                                                   : print('Пароль написан не правильно. Исспользуйте только буквы от A до z и числа от 0 до 9')
                    elif     resp.status_code == 409 or (resp.headers.get('Content-Type') == 'application/json' and resp.json().get('status') == 409):
                        if   resp.json().get('error') == 'account exists'                                                          : print('Такой аккаунт уже существует')
                    elif     resp.status_code == 500 or (resp.headers.get('Content-Type') == 'application/json' and resp.json().get('status') == 500):
                        if   resp.json().get('error') == 'unexpected'                                                              : print('На сервере произошла непредвиденная ошибка')
                        elif resp.status_code == 500 or resp.json()['status'] == 500 and resp.json()['error'] == 'token generation': print('Произошла ошибка при генерации токена')
                    elif     resp.status_code == 200 or resp.json()['status'] == 200                                               :
                        print('Регистрация прошла успешна!')
                        try:
                            with open('token.tok', 'w') as f:
                                f.write(resp.json()['token'])
                            token = resp.json()['token']
                            print(token)
                            print('Токен успешно сохранён')
                        except:
                            print(f'Ошибка при сохранении токена. Пожалуйста, впишите следующий текст в token.tok:\n{resp.json()['token']}')
                else: pass
            else: pass

        elif choice == '3': # ПРОЧИТАТЬ СООБЩЕНИЯ
            resp = requests.get(f'{host}/read_messages?token={token}')
            if   resp.status_code == 404 or resp.json()['status'] == 404: print('Сообщений нет!')
            elif resp.status_code == 400 or resp.json()['status'] == 400: print('Нет токена!')

            elif resp.status_code == 200 or resp.json()['status'] == 200:
                data = resp.json()
                for message in data["messages"]:
                    author = message["author"]
                    message_id = message["message_id"]
                    text = message["text"]
                    if show_id:
                        print(f"(id {message_id}) {author}: {text}")
                    else:
                        print(f"{author}: {text}")

        elif choice == '4': # НАПИСАТЬ СООБЩЕНИЕ
            message = input('Введите сообщение (>exit для выхода): ')
            if message != '>exit':
                resp = requests.get(f'{host}/add_message?message={message}&token={token}')
                if   resp.status_code == 400 or resp.json()['status'] == 400 and resp.json()['error'] == "token required"  : print('Токен не найден')
                elif resp.status_code == 400 or resp.json()['status'] == 400 and resp.json()['error'] == "message required": print('Сообщения нет')
                elif resp.status_code == 500 or resp.json()['status'] == 500                                               : print('Произошла ошибка')
                elif resp.status_code == 201 or resp.json()['status'] == 201                                               : print('Сообщение успешно добавлено')
            else:
                pass

        elif choice == '5':
            req = reqests.get(f'{host}/admin?token={token}&allow=False')
            if   req.status_code == 400: print('Токен не найден')
            elif req.status_code == 503: print('Недостаточно прав!')
            elif req.status_code == 200:
                print('=== ДЕЙСТВИЯ АДМИНИСТРАТОРА ===')
                print('1 - Удалить сообщение по ID\n2 - Удалить аккаунт по ID\n0 - Выход')
                action = int(input('Введите номер действия: '))
                if action != 0:
                    id = int(input('Введите ID сообщения/аккаунта: '))
                    resp = reqests.get(f'{host}/admin?token={token}&allow=True&action={action}&id={id}')
                    if resp.status_code == 400 or (resp.headers.get('Content-Type') == 'application/json' and resp.json().get('status') == 400):
                        if resp.json().get('error') == 'action is required': print('Действие отсутствует')
                        elif resp.json().get('error') == 'id is required': print('ID отсутствует')

        elif choice == '6':
            while True:
                # if platform == 'linux': subprocess.run('clear')
                # elif platform == 'win32' or 'win' in platform: subprocess.run('cls')
                menu(2)
                setting = input('Введите новое значение по примеру выше: ')
                setting = setting.split()
                print(setting)
                if setting[0] == '1':
                    if setting[1] == "True" or "False":
                        show_id == setting[1]
                        with open('data.json', 'w') as f:
                            #json.dump('', f, indent=4)
                            f.write('\n')
                            data = {
                                'OS': platform,
                                'show-id': show_id
                            }
                            json.dump(data, f, indent=4)
                    else:
                        print('Неверное значение!')
                if setting[0] == '0':
                    break
        elif choice == '0':
            break
        else:
            print("Неверный выбор, попробуй снова.")

if __name__ == "__main__":
    main()
