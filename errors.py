import requests

def errors(choise, resp):
    if choise == 1:
        if resp.status_code == 400 or (resp.headers.get('Conent-Type') == 'application/json' and resp.json().get('status') == 400):
            if resp.json().get('error') == 'username is required': print('Юзернейм отсутствует')
            elif resp.json().get('error') == 'password is required': print('Пароль отсутствует')
            elif resp.json().get('error') == 'name wrote incorrectly': print('Юзернейм написан не правильно')
            elif resp.json().get('error') == 'password wrote incorrectly': print('Пароль написан не правильно')
            elif resp.json().get('error') == 'name or password is incorrect': print('Юзернейм или парлоль не правильный')
        elif resp.status_code == 500 or (resp.headers.get('Content-Type') == 'application/json' and resp.json().get('status') == 409):
            if resp.json().get('error') == 'unexpected error': print('На сервере произошла непредвиденная ошибка')
        elif resp.status_code == 200 or resp.json()['status'] == 200:
            got_token = resp.json()['token']
            with open('token.tok', 'w') as f:
                f.write(got_token)
            print('Вход произошёл успешно!')

    elif choise == 2:
        if resp.status_code == 400 or (resp.headers.get("Content-Type") == "application/json" and resp.json().get("status") == 400):
            if resp.json().get("error") == "username is required":
                print("Юзернейм отсутствует")
            elif resp.json().get("error") == "password is required":
                print("Пароль отсутствует")
            elif resp.json().get("error") == "username is too short":
                print("Юзернейм слишком короткий")
            elif resp.json().get("error") == "password is too short":
                print("Пароль слишком короткий")
            elif resp.json().get("error") == "username is incorrect":
                print("Юзернейм написан не правильно. Исспользуйте только буквы от A до z и числа от 0 до 9")
            elif resp.json().get("error") == "password is incorrect":
                print("Пароль написан не правильно. Исспользуйте только буквы от A до z и числа от 0 до 9")
        elif resp.status_code == 409 or (resp.headers.get("Content-Type") == "application/json" and resp.json().get("status") == 409):
            if resp.json().get("error") == "account exists":
                print("Такой аккаунт уже существует")
        elif resp.status_code == 500 or (resp.headers.get("Content-Type") == "application/json" and resp.json().get("status") == 500):
            if resp.json().get("error") == "unexpected":
                print("На сервере произошла непредвиденная ошибка")
            elif resp.json().get("error") == "token generation":
                print("Произошла ошибка при генерации токена")
        elif resp.status_code == 200 or resp.json()["status"] == 200:
            print("Регистрация прошла успешна!")
            try:
                with open("token.tok", "w") as f:
                    f.write(resp.json()["token"])
                token = resp.json()["token"]
                print(token)
                print("Токен успешно сохранён")
            except:
                print(f'Ошибка при сохранении токена. Пожалуйста, впишите следующий текст в token.tok:\n{resp.json()["token"]}')

    elif choise == 3:
        if resp.status_code == 404 or resp.json()["status"] == 404:
            print("Сообщений нет!")
        elif resp.status_code == 400 or resp.json()["status"] == 400:
            print("Нет токена!")

        elif resp.status_code == 200 or resp.json()["status"] == 200:
            data = resp.json()
            for message in data["messages"]:
                author = message["author"]
                message_id = message["message_id"]
                text = message["text"]
                if show_id:
                    print(f"(id {message_id}) {author}: {text}")
                else:
                    print(f"{author}: {text}")

    elif choise == 4:
        if (resp.status_code == 400 or resp.json()["status"] == 400 and resp.json()["error"] == "token required"):
            print("Токен не найден")
        elif (resp.status_code == 400 or resp.json()["status"] == 400 and resp.json()["error"] == "message required"):
            print("Сообщения нет")
        elif resp.status_code == 500 or resp.json()["status"] == 500:
            print("Произошла ошибка")
        elif resp.status_code == 201 or resp.json()["status"] == 201:
            print("Сообщение успешно добавлено")
    
    elif choise == 5:
        if req.status_code == 400:
            print("Токен не найден")
        elif req.status_code == 503:
            print("Недостаточно прав!")
        elif req.status_code == 200:
            print("=== ДЕЙСТВИЯ АДМИНИСТРАТОРА ===")
            print(
                "1 - Удалить сообщение по ID\n2 - Удалить аккаунт по ID\n0 - Выход"
            )
            action = int(input("Введите номер действия: "))
            if action != 0:
                id = int(input("Введите ID сообщения/аккаунта: "))
                resp = reqests.get(
                    f"{host}/admin?token={token}&allow=True&action={action}&id={id}"
                )
                if resp.status_code == 400 or (resp.headers.get("Content-Type") == "application/json" and resp.json().get("status") == 400):
                    if resp.json().get("error") == "action is required":
                        print("Действие отсутствует")
                    elif resp.json().get("error") == "id is required":
                        print("ID отсутствует")

    else:
        pass
