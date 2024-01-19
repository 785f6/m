import re

def parse_address(input_str):
    # Инициализация словаря для хранения результатов
    result = {
        "город": "",
        "улица": "",
        "тип_улицы": "",
        "дом": "",
        "корпус": ""
    }

    # Удаляем точки из строки
    input_str = input_str.replace('.', ' ')

    # Разбиваем строку по запятой
    parts = input_str.split(',')

    # Первая часть строки (город)
    first_part = parts[0].strip()
    # Используем регулярное выражение для поиска слов "г" или "город" и удаляем их
    pattern = re.compile(r'\bг\s|\sг\b|\bгород\b', re.IGNORECASE)
    matches = pattern.findall(first_part)
    for match in matches:
        first_part = first_part.replace(match, '')
    result['город'] = first_part.strip()

    # Вторая часть строки (улица)
    second_part = parts[1].strip()
    # Используем регулярное выражение для поиска аббревиатур типов улиц и удаляем их
    pattern = re.compile(r'\bул\s|\sул\b|\bпр\s|\sпр\b|\bнаб\s|\sнаб\b', re.IGNORECASE)
    matches = pattern.findall(second_part)

    for match in matches:
        second_part = second_part.replace(match, '').strip()

    for match in matches:
        if 'ул' in match.lower():
            result['тип_улицы'] = 'улица'
            break
        elif 'пр' in match.lower():
            result['тип_улицы'] = 'проспект'
            break
        elif 'наб' in match.lower():
            result['тип_улицы'] = 'набережная'
            break

    street_types = ['улица', 'бульвар', 'проспект', 'набережная', 'аллея', 'переулок']
    for street_type in street_types:
        if street_type.lower() in second_part.lower():
           type_start = second_part.lower().index(street_type.lower())
           street_type_value = second_part[type_start:type_start + len(street_type)].strip()
           second_part = second_part.replace(street_type_value, '').strip()
           result['тип_улицы'] = street_type_value.lower()
           break

    result['улица'] = second_part

    # Третья часть строки (дом и корпус)
    third_part = ' '.join(parts[2:]).strip()
    
    # Используем регулярное выражение для поиска чисел в строке
    matches = re.findall(r'[^\d]*(\d+)[^\d]*', third_part)
    for match in matches:
        num = match
        # Определяем, является ли число номером дома или корпуса и записываем в словарь
        if result['дом'] == "":
            result['дом'] = num
        else:
            result['корпус'] = num
        third_part = third_part.replace(num, '')

    return result


# Примеры использования
addresses = [
    "Санкт-Петербург, Большая Морская улица, дом 67",
    "СПБ, Невский проспект, 55",
    "г. Санкт-Петербург, Озерковский проспект, 48к2",
    "Город Санкт-Петербург, Биржевая набережная, д. 14 корпус 3",
    "СПБ Г., аллея Евгения Шварца, 10 дом 5 к",
    "СПБ, бульвар Новаторов, 100",
    "Санкт-Петербург гОроД, Ленина, 99 к. 3",   
]

for address in addresses:
    print(f"Адрес: {address}")
    result = parse_address(address)
    for key, value in result.items():
        print(f"{key} - {value}")
    print()


    # Добавляем в программу возможность ввода с клавиатуры
while True:
    address_input = input("Введите адрес (для выхода введите '1'): ")
    
    # Проверяем условие выхода
    if address_input == '1':
        break

    result = parse_address(address_input)
    
    # Выводим результаты
    for key, value in result.items():
        print(f"{key} - {value}")
    print()