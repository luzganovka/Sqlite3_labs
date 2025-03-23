import sqlite3
import random
import string


def random_int(min_value=1, max_value=10):
    return (random.randint(min_value, max_value))

# Функция для генерации случайного числа
def random_real(min_value=1, max_value=100):
    return (random.randint(min_value, max_value*100)/100)

# Функция для генерации случайной строки
def random_string(length=random_int(1, 50)):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def name_generator():
    word_lists = [
    ['left', 'brand-new', 'hilarious', 'epic', 'wierd', 'rusty', 'old', 'glowing', 'tiny', 'gigantic', 'golden', 'too heavy', 'long', 'flaming'],
    ['swoard', 'bow', 'hummer', 'pike', 'chair', 'railgun', 'BFG', 'magic staff', 'battle staff', 'machine gun', 'bomb'],
    ['of fame', 'of shame', 'of pain', 'of a rain', 'of doom', 'of an ancient giant', 'from the stars', 'from a tomb']]
    name = ''
    for words in word_lists:
        name += words[random.randint(0, len(words)-1)]
        name += ' '
    return name[:-1]

damage_types = ['acid', 'bludgeoning', 'cold', 'fire', 'force', 'lightning', 'necrotic', 'piercing', 'poison', 'psychic', 'radiant', 'slashing', 'thunder']

# Подключение к базе данных (или создание новой)
conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()

# Количество записей для добавления
num_records = 3

# Вставка случайных данных в таблицу
for _ in range(num_records):
    name =      name_generator()  # Генерация случайного имени
    basic_damage = random_real(1, 100)
    damage_type = damage_types[random.randint(0, len(damage_types) - 1)]
    rarity =    random_int(1, 10)
    price =     random_real(1, 1000)
    description = random_string(random_int(1, 50))
    cursor.execute('INSERT INTO Weapon (name, basic_damage, damage_type, rarity, price, description) VALUES (?, ?, ?, ?, ?, ?)',
                                         (name, basic_damage, damage_type, rarity, price, description))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print(f'Добавлено {num_records} записей в таблицу my_table.')
