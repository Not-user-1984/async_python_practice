import asyncio


# Функция для обработки клиентских соединений
async def handle_client(reader, writer):
    while True:
        # Ждем данные от клиента
        request = await reader.read(8096)
        if not request:
            break

        print(f"Получен запрос от клиента: {request.decode()}")

        # Читаем ответ из файла
        with open("response.txt", "r") as response_file:
            response = response_file.read().encode()

        # Отправляем ответ клиенту
        writer.write(response)
        await writer.drain()
        print(f"Ответ отправлен клиенту")

    # Закрываем соединение
    writer.close()
    await writer.wait_closed()
    print("Соединение закрыто")


# Асинхронная функция для запуска сервера
async def start_server():
    server = await asyncio.start_server(handle_client, "localhost", 8000)
    print(f"Сервер запущен на localhost:8000")

    async with server:
        await server.serve_forever()


# Основной скрипт
if __name__ == "__main__":
    asyncio.run(start_server())
