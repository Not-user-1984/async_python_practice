def gen1(s):
    for i in s:
        print(f"gen1: возвращает {i}")
        yield i


def gen2(n):
    for i in range(n):
        print(f"gen2: возвращает {i}")
        yield i


g1 = gen1('C наступающим ')
g2 = gen2(4)

tasks = [g1, g2]
print("Начальные задачи:", tasks)

while tasks:
    task = tasks.pop(0)
    # print(f"Обрабатывается задача: {task}")

    try:
        i = next(task)
        # print(f"Возвращено значение: {i}")
        tasks.append(task)
        # print("Обновленные задачи:", tasks)
    except StopIteration:
        print(f"Задача {task} завершена.")
