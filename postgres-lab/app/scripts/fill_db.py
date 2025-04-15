import psycopg2
import random
import string
import time

# Настройки подключения к PostgreSQL (укажи свои значения)
DB_CONFIG = {
    'dbname': 'mydb',
    'user': 'pgroot',
    'password': '123',
    'host': 'db',
    'port': 5432
}

def random_int(min_value=1, max_value=10):
    return random.randint(min_value, max_value)

def random_real(min_value=1, max_value=100):
    return random.randint(min_value, max_value * 100) / 100

def random_string(length=random_int(1, 50)):
    return ''.join(random.choices(string.ascii_letters, k=length))

def weapon_name_generator():
    word_lists = [
        ['left', 'brand-new', 'hilarious', 'epic', 'wierd', 'rusty', 'old', 'glowing', 'tiny', 'gigantic', 'golden', 'too heavy', 'long', 'flaming'],
        ['sword', 'bow', 'hammer', 'pike', 'chair', 'railgun', 'BFG', 'magic staff', 'battle staff', 'machine gun', 'bomb'],
        ['of fame', 'of shame', 'of pain', 'of a rain', 'of doom', 'of an ancient giant', 'from the stars', 'from a tomb']
    ]
    return ' '.join(random.choice(words) for words in word_lists)

def creature_name_generator():
    word_lists = [
        ['саблезубый', 'вонючий', 'огромный', 'проклятый', 'желатиновый', 'невидимый', 'сонный', 'летающий'],
        ['заяц', 'ботинок', 'великан', 'дух', 'газебо', 'дракон', 'крестьянин', 'зерг', 'демон', 'куб', 'скелет', 'зомби'],
        ['с дробовиком', 'в доспехах', 'с палкой', 'без головы', 'с презрительным взглядом', 'сочащийся ядом', '-лучник']
    ]
    return ' '.join(random.choice(words) for words in word_lists)

def weapon_generator(cursor, num_records):
    damage_types = ['acid', 'bludgeoning', 'cold', 'fire', 'force', 'lightning', 'necrotic', 'piercing', 'poison', 'psychic', 'radiant', 'slashing', 'thunder']
    inserted = 0
    for _ in range(num_records):
        name = weapon_name_generator()
        cursor.execute('SELECT 1 FROM Weapon WHERE name = %s', (name,))
        if cursor.fetchone():
            continue

        cursor.execute(
            'INSERT INTO Weapon (name, basic_damage, damage_type, rarity, price, description) VALUES (%s, %s, %s, %s, %s, %s)',
            (name, random_real(), random.choice(damage_types), random_int(), random_real(1, 1000), random_string())
        )
        inserted += 1
    print(f'Добавлено {inserted} новых записей в таблицу Weapon.')

def bestiary_generator(cursor, num_records):
    biomes = ['горы', 'заброшенные рудники', 'леса', 'озёра и реки', 'морское дно', 'городские улицы']
    inserted = 0
    for _ in range(num_records):
        creature = creature_name_generator()
        cursor.execute('SELECT 1 FROM Bestiary WHERE creature = %s', (creature,))
        if cursor.fetchone():
            continue
        cursor.execute('INSERT INTO Bestiary (creature, biome, danger) VALUES (%s, %s, %s)', (creature, random.choice(biomes), random_int()))
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
        for damage_type in random.sample(damage_types, random_int(1, min(3, len(damage_types)))):
            cursor.execute('SELECT 1 FROM Weaknesses WHERE creature = %s AND damage_type = %s', (creature, damage_type))
            if cursor.fetchone():
                continue
            cursor.execute('INSERT INTO Weaknesses (creature, damage_type, damage_modifier) VALUES (%s, %s, %s)',
                           (creature, damage_type, 10 * random_int(0, 20)))
            count += 1
    print(f'Добавлено {count} новых записей в таблицу Weaknesses.')

def fraction_generator(cursor):
    cursor.execute('SELECT creature FROM Bestiary')
    all_creatures = [row[0] for row in cursor.fetchall()]
    if not all_creatures:
        print("Нет существ в Bestiary для генерации фракций.")
        return

    cursor.execute('SELECT fraction_name FROM Fraction')
    existing_factions = set(row[0] for row in cursor.fetchall())

    cursor.execute('SELECT name FROM Weapon')
    weapons = [row[0] for row in cursor.fetchall()]
    if not weapons:
        print("Нет оружия для генерации фракций.")
        return

    chosen_creatures = random.sample(all_creatures, int(len(all_creatures) * random.uniform(0.7, 0.9)))
    word_lists = [
        ['сумасшедшие', 'элитные', 'богатые', 'воинственные', 'высокотехнологичные', 'праведные'],
        ['чернокнижники', 'рыцари', 'буржуи', 'амазонки', 'инфобезники', 'святые отцы'],
        ['из пещеры', 'на конях', 'со связями', 'из джунглей', 'из киберпанка', 'против насилия']
    ]
    inserted = 0
    for creature in chosen_creatures:
        fraction_name = ' '.join(random.choice(words) for words in word_lists)
        cursor.execute('SELECT 1 FROM Fraction WHERE fraction_name = %s', (fraction_name,))
        if cursor.fetchone():
            continue
        cursor.execute('INSERT INTO Fraction (fraction_name, weapon_name, enemy_name) VALUES (%s, %s, %s)',
                       (fraction_name, random.choice(weapons), creature))
        inserted += 1
    print(f'Добавлено {inserted} новых записей в таблицу Fraction.')

def player_generator(cursor, num_records):
    cursor.execute('SELECT fraction_name FROM Fraction')
    factions = [row[0] for row in cursor.fetchall()]
    inserted = 0
    for _ in range(num_records):
        name = f"Игрок_{random_string(6)}"
        fraction = random.choice(factions) if factions and random.random() < 0.5 else None
        try:
            cursor.execute('INSERT INTO Player (fraction, name) VALUES (%s, %s)', (fraction, name))
            inserted += 1
        except psycopg2.errors.UniqueViolation:
            continue
    print(f'Добавлено {inserted} новых игроков в таблицу Player.')

def entity_generator(cursor, num_records):
    cursor.execute('SELECT id FROM Player')
    player_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT name FROM Weapon')
    weapon_names = [row[0] for row in cursor.fetchall()]
    if not weapon_names:
        print("Нет оружия для генерации Entity.")
        return
    inserted = 0
    for _ in range(num_records):
        owner_id = random.choice(player_ids) if player_ids and random.random() < 0.8 else None
        try:
            cursor.execute('INSERT INTO Entity (owner_id, weapon_name, weapon_level) VALUES (%s, %s, %s)',
                           (owner_id, random.choice(weapon_names), random_int(1, 10)))
            inserted += 1
        except psycopg2.errors.UniqueViolation:
            continue
    print(f'Добавлено {inserted} новых сущностей в таблицу Entity.')

if __name__ == "__main__":
    
    time.sleep(5)
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()

        weapon_generator(cursor, 30)
        bestiary_generator(cursor, 30)
        weaknesses_generator(cursor)
        fraction_generator(cursor)
        player_generator(cursor, 30)
        entity_generator(cursor, 60)

    except Exception as e:
        print("Ошибка при работе с базой данных:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
