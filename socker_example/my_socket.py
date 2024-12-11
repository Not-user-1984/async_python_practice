
import socket
from select import select

# Список задач для выполнения
tasks = []
# Словарь сокетов, готовых к чтению
to_read = {}
# Словарь сокетов, готовых к записи
to_write = {}


def server():
    # Создаем сокет для сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Устанавливаем опцию для повторного использования адреса
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Привязываем сокет к адресу localhost:8000
    server_socket.bind(('localhost', 8000))
    # Начинаем прослушивать входящие соединения
    server_socket.listen()
    while True:
        print('ждем соединение..')
        # Генерируем событие 'read' для серверного сокета
        yield ('read', server_socket)
        # Принимаем входящее соединение
        client_socket, addr = server_socket.accept()
        print("соединение с ", addr)
        # Добавляем задачу для обработки клиентского сокета
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        # Генерируем событие 'read' для клиентского сокета
        yield ('read', client_socket)
        # Получаем данные от клиента
        request = client_socket.recv(8096)

        if not request:
            break
        else:
            # Открываем файл с ответом
            with open("response.txt", "r") as response_file:
                # Генерируем событие 'write' для клиентского сокета
                yield ('write', client_socket)
                # Отправляем ответ клиенту
                client_socket.send(response_file.read().encode())
                print(f"ответил серверу {client_socket}")

    # Закрываем клиентский сокет
    client_socket.close()
    print("сервер закрыт")


def event_loop():
    print("запуск...")
    # Цикл работает, пока есть задачи или сокеты для чтения/записи
    while any([tasks, to_read, to_write]):
        print("задачи\n", tasks)
        print("на чтение\n", to_read)
        print("на запись\n", to_write)

        # Если нет задач, ожидаем готовности сокетов
        while not tasks:
            # Используем select для ожидания готовности сокетов
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            for sock in ready_to_read:
                print('сокет на чтение\n', sock)
                # Добавляем задачу для чтения в список задач
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                print('сокет на запись\n', sock)
                # Добавляем задачу для записи в список задач
                tasks.append(to_write.pop(sock))

        try:
            # Извлекаем первую задачу из списка
            task = tasks.pop(0)
            print(task)
            # Получаем событие и сокет из задачи
            reason, sock = next(task)

            if reason == 'read':
                # Если событие 'read', добавляем задачу в to_read
                to_read[sock] = task

            if reason == 'write':
                # Если событие 'write', добавляем задачу в to_write
                to_write[sock] = task
        except StopIteration:
            # Если задача завершена, выводим сообщение
            print('готово')


if __name__ == '__main__':
    # Добавляем задачу сервера в список задач
    tasks.append(server())
    # Запускаем цикл событий
    event_loop()