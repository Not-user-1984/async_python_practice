import asyncio
import time


# Асинхронные задачи
async def task1():
    await asyncio.sleep(2)
    return "Задача 1 завершена"


async def task2():
    await asyncio.sleep(1)
    return "Задача 2 завершена"


async def task3():
    await asyncio.sleep(3)
    return "Задача 3 завершена"


# Синхронные задачи
def sync_task1():
    time.sleep(2)
    return "Синхронная задача 1 завершена"


def sync_task2():
    time.sleep(1)
    return "Синхронная задача 2 завершена"


def sync_task3():
    time.sleep(3)
    return "Синхронная задача 3 завершена"


# Функция для замера времени выполнения
def measure_time(func):
    start_time = time.time()
    result = func()
    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")
    return result


# Асинхронная функция
async def async_main():
    # Запускаем задачи одновременно
    results = await asyncio.gather(task1(), task2(), task3())
    return results


# Синхронная функция
def sync_main():
    results = [sync_task1(), sync_task2(), sync_task3()]
    return results


# Основной скрипт
if __name__ == "__main__":
    print("Асинхронное выполнение:")
    async_results = measure_time(lambda: asyncio.run(async_main()))
    print(async_results)

    print("\nСинхронное выполнение:")
    sync_results = measure_time(sync_main)
    print(sync_results)
