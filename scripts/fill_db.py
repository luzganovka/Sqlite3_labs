import sqlite3
import random
import string

DB_PATH = '../mydb.db'
NEW_RECORDS = 10

def random_int(min_value=1, max_value=10):
    return (random.randint(min_value, max_value))

# Функция для генерации случайного числа
def random_real(min_value=1, max_value=100):
    return (random.randint(min_value, max_value*100)/100)

# Функция для генерации случайной строки
def random_string(length=random_int(1, 50)):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def weapon_name_generator():
    word_lists = [
    ['left', 'brand-new', 'hilarious', 'epic', 'wierd', 'rusty', 'old', 'glowing', 'tiny', 'gigantic', 'golden', 'too heavy', 'long', 'flaming'],
    ['sword', 'bow', 'hammer', 'pike', 'chair', 'railgun', 'BFG', 'magic staff', 'battle staff', 'machine gun', 'bomb'],
    ['of fame', 'of shame', 'of pain', 'of a rain', 'of doom', 'of an ancient giant', 'from the stars', 'from a tomb']]
    name = ''
    for words in word_lists:
        name += words[random.randint(0, len(words)-1)]
        name += ' '
    return name[:-1]


def creature_name_generator():
    word_lists = [
        ['саблезубый', 'вонючий', 'огромный', 'проклятый', 'желатиновый', 'невидимый', 'сонный', 'летающий'],
        ['заяц', 'ботинок', 'великан', 'дух', 'газебо', 'дракон', 'крестьянин', 'зерг', 'демон', 'куб', 'скелет', 'зомби'],
        ['с дробовиком', 'в доспехах', 'с палкой', 'без головы', 'с презрительным взглядом', 'сочащийся ядом', '-лучник']
    ]
    name = ''
    for words in word_lists:
        name += words[random.randint(0, len(words)-1)]
        name += ' '
    return name[:-1]


def weapon_generator(cursor, num_records):
    damage_types = ['acid', 'bludgeoning', 'cold', 'fire', 'force', 'lightning', 'necrotic', 'piercing',
                    'poison', 'psychic', 'radiant', 'slashing', 'thunder']
    
    inserted = 0
    for _ in range(num_records):
        name = weapon_name_generator()
        cursor.execute('SELECT 1 FROM Weapon WHERE name = ?', (name,))
        if cursor.fetchone():
            continue  # такое оружие уже есть

        basic_damage = random_real(1, 100)
        damage_type = random.choice(damage_types)
        rarity = random_int(1, 10)
        price = random_real(1, 1000)
        description = random_string(random_int(1, 50))

        cursor.execute('INSERT INTO Weapon (name, basic_damage, damage_type, rarity, price, description) VALUES (?, ?, ?, ?, ?, ?)',
                       (name, basic_damage, damage_type, rarity, price, description))
        inserted += 1

    print(f'Добавлено {inserted} новых записей в таблицу Weapon.')


def bestiary_generator(cursor, num_records):
    biomes = ['горы', 'заброшенные рудники', 'леса', 'озёра и реки', 'морское дно', 'городские улицы']
    
    inserted = 0
    for _ in range(num_records):
        creature = creature_name_generator()
        cursor.execute('SELECT 1 FROM Bestiary WHERE creature = ?', (creature,))
        if cursor.fetchone():
            continue  # уже есть такое существо

        biome = random.choice(biomes)
        danger = random_int(1, 10)

        cursor.execute('INSERT INTO Bestiary (creature, biome, danger) VALUES (?, ?, ?)',
                       (creature, biome, danger))
        inserted += 1

    print(f'Добавлено {inserted} новых записей в таблицу Bestiary.')

def weaknesses_generator(cursor):
    cursor.execute('SELECT creature FROM Bestiary')
    creatures = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT DISTINCT damage_type FROM Weapon')
    damage_types = [row[0] for row in cursor.fetchall()]

    if not creatures or not damage_types:
        print("Нет данных для генерации Weaknesses.")
        return

    count = 0
    for creature in creatures:
        num_weaknesses = random_int(1, min(3, len(damage_types)))
        chosen_types = random.sample(damage_types, num_weaknesses)

        for damage_type in chosen_types:
            cursor.execute('SELECT 1 FROM Weaknesses WHERE creature = ? AND damage_type = ?', (creature, damage_type))
            if cursor.fetchone():
                continue  # слабость уже есть

            damage_modifier = 10 * random_int(0, 20) # модификатор урона в процетах от 0 до 200
            cursor.execute('INSERT INTO Weaknesses (creature, damage_type, damage_modifier) VALUES (?, ?, ?)',
                           (creature, damage_type, damage_modifier))
            count += 1

    print(f'Добавлено {count} новых записей в таблицу Weaknesses.')


def fraction_generator(cursor):

    # Получаем список всех существ
    cursor.execute('SELECT creature FROM Bestiary')
    all_creatures = [row[0] for row in cursor.fetchall()]

    if not all_creatures:
        print("Нет существ в Bestiary для генерации фракций.")
        return

    # Получаем список уже существующих фракций
    cursor.execute('SELECT fraction_name FROM Fraction')
    existing_factions = set(row[0] for row in cursor.fetchall())

    # Получаем список оружий
    cursor.execute('SELECT name FROM Weapon')
    weapons = [row[0] for row in cursor.fetchall()]

    if not weapons:
        print("Нет оружия для генерации фракций.")
        return

    # Выбираем случайное подмножество существ (например, 80%)
    num_to_generate = int(len(all_creatures) * random.uniform(0.7, 0.9))
    chosen_creatures = random.sample(all_creatures, num_to_generate)

    word_lists = [
        ['сумасшедшие', 'элитные', 'богатые', 'воинственные', 'высокотехнологичные', 'праведные'],
        ['чернокнижники', 'рыцари', 'буржуи', 'амазонки', 'инфобезники', 'святые отцы'],
        ['из пещеры', 'на конях', 'со связями', 'из джунглей', 'из киберпанка', 'против насилия']
    ]

    inserted = 0
    for creature in chosen_creatures:
        enemy_name = creature

        # Генерируем имя фракции
        fraction_name = ''
        for words in word_lists:
            fraction_name += words[random.randint(0, len(words)-1)]
            fraction_name += ' '
        fraction_name = fraction_name[:-1]

        # Выбираем оружие и врага
        weapon_name = random.choice(weapons)

        cursor.execute('INSERT INTO Fraction (fraction_name, weapon_name, enemy_name) VALUES (?, ?, ?)',
                       (fraction_name, weapon_name, enemy_name))
        inserted += 1

    print(f'Добавлено {inserted} новых записей в таблицу Fraction.')

if __name__ == "__main__":
    
    # Подключение к базе данных (или создание новой)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    weapon_generator(cursor, 30)
    bestiary_generator(cursor, 30)
    weaknesses_generator(cursor)
    fraction_generator(cursor)

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()