#!/usr/bin/env python3  # если с виндовса - убрать этоу строчку
import json
import os
from collections import defaultdict


def parse_chat(file_path, target_ids, results_dict):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)

        chat_name = data.get("name", "Unknown Chat")
        messages = data.get("messages", [])

        for msg in messages:
            sender_id = str(msg.get("from_id"))

            if sender_id in target_ids:
                # Извлекаем данные
                sender_name = msg.get("from", "Unknown")
                timestamp = msg.get("date", "00:00:00")
                raw_text = msg.get("text", "")

                # Собираем текст сообщения
                full_message = ""
                if isinstance(raw_text, str):
                    full_message = raw_text
                elif isinstance(raw_text, list):
                    for part in raw_text:
                        full_message += part.get("text", "") if isinstance(part, dict) else str(part)

                if full_message.strip():
                    formatted_entry = (
                        f"От_{sender_name} в_чате[{chat_name}] в_[{timestamp}]:\n"
                        f"{full_message.strip()}\n"
                        f"{'-' * 30}"  # Разделитель для читаемости
                    )
                    results_dict[sender_id].append(formatted_entry)

    except Exception as e:
        print(f"[!] Ошибка при чтении {file_path}: {e}")


def main():
    files = []
    targets = set()

    # 1. Первый запрос файла
    first_path = input("Введи путь к файлу JSON: ").strip().strip('"')
    if os.path.exists(first_path):
        files.append(first_path)
        print("успешно")
    else:
        print("Файл не найден.")

    while True:
        print("\n--- Меню управления ---")
        print("1 // Добавить еще чат")
        print("2 // Добавить пользователя/телей (ID)")
        print("3 // Начать парсинг")

        choice = input("\nВыбери пункт: ").strip()

        if choice == "1":
            path = input("Введи путь к JSON: ").strip().strip('"')
            if os.path.exists(path):
                files.append(path)
                print("успешно добавлено")
            else:
                print("Ошибка: файл не найден.")

        elif choice == "2":
            ids = input("Введи ID через пробел: ").split()
            for i in ids:
                targets.add(i)
            print(f"Текущий список ID: {list(targets)}")

        elif choice == "3":
            if not files or not targets:
                print("[!] Ошибка: добавь хотя бы один файл и один ID.")
                continue


            results_per_user = defaultdict(list)

            print("[*] Парсинг запущен...")
            for f_path in files:
                parse_chat(f_path, targets, results_per_user)

            if not results_per_user:
                print("\nНичего не найдено.")
            else:
                # Создаем отдельный файл для каждого ID
                for user_id, msgs in results_per_user.items():
                    filename = f"{user_id}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("\n".join(msgs))
                    print(f"Создан файл: {filename} (сообщений: {len(msgs)})")
                print("\nГотово!")
            break


if __name__ == "__main__":
    main()

