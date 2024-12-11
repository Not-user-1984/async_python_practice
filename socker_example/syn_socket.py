import socket


# Функция для обработки клиентских соединений
def handle_client(client_socket):
    while True:
        # Получаем данные от клиента
        request = client_socket.recv(8096)
        if not request:
            break

        print(f"Получен запрос от клиента: {request.decode()}")

        # Читаем ответ из файла
        with open("response.txt", "r") as response_file:
            response = response_file.read().encode()

        # Отправляем ответ клиенту
        client_socket.send(response)
        print(f"Ответ отправлен клиенту")

    # Закрываем соединение
    client_socket.close()
    print("Соединение закрыто")


# Функция для запуска сервера
def start_server():
    # Создаем сокет для сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Устанавливаем опцию для повторного использования адреса
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Привязываем сокет к адресу localhost:8000
    server_socket.bind(("localhost", 8000))
    # Начинаем прослушивать входящие соединения
    server_socket.listen()
    print(
        f" Сервер запущен на localhost:8000"
        )

    while True:
        # Принимаем входящее соединение
        client_socket, addr = server_socket.accept()
        print(f"Соединение с клиентом {addr}")

        # Обрабатываем клиента
        handle_client(client_socket)


# Основной скрипт
if __name__ == "__main__":
    start_server()
