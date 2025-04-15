import psycopg2
import random
import string

DB_CONFIG = {
    'dbname': 'mydb',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'db',
    'port': 5432
}

def random_int(min_value=1, max_value=10):
    return random.randint(min_value, max_value)

def random_real(min_value=1, max_value=100):
    return round(random.uniform(min_value, max_value), 2)

def random_string(length=None):
    length = length or random_int(1, 50)
    return ''.join(random.choices(string.ascii_letters, k=length))

def weapon_name_generator():
    word_lists = [
        ['left', 'brand-new', 'hilarious', 'epic', 'weird', 'rusty', 'old', 'glowing', 'tiny', 'gigantic', 'golden', 'too heavy', 'long', 'flaming'],
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
    damage_types = ['acid', 'bludgeoning', 'cold', 'fire', 'force', 'lightning', 'necrotic', 'piercing',
                    'poison', 'psychic', 'radiant', 'slashing', 'thunder']
    inserted = 0
    for _ in range(num_records):
        name = weapon_name_generator()
        cursor.execute('SELECT 1 FROM Weapon WHERE name = %s', (name,))
        if cursor.fetchone():
            continue

        cursor.execute('''
            INSERT INTO Weapon (name, basic_damage, damage_type, rarity, price, description)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            name,
            random_real(10, 100),
            random.choice(damage_types),
            random_int(1, 10),
            random_real(10, 1000),
            random_string()
        ))
        inserted += 1
    print(f'Добавлено {inserted} записей в Weapon')

def bestiary_generator(cursor, num_records):
    biomes = ['горы', 'заброшенные рудники', 'леса', 'озёра и реки', 'морское дно', 'городские улицы']
    inserted = 0
    for _ in range(num_records):
        creature = creature_name_generator()
        cursor.execute('SELECT 1 FROM Bestiary WHERE creature = %s', (creature,))
        if cursor.fetchone():
            continue

        cursor.execute('''
            INSERT INTO Bestiary (creature, biome, danger)
            VALUES (%s, %s, %s)
        ''', (
            creature,
            random.choice(biomes),
            random_int(1, 10)
        ))
        inserted += 1
    print(f'Добавлено {inserted} записей в Bestiary')

def weaknesses_generator(cursor):
    cursor.execute('SELECT creature FROM Bestiary')
    creatures = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT DISTINCT damage_type FROM Weapon')
    damage_types = [row[0] for row in cursor.fetchall()]

    if not creatures or not damage_types:
        return

    inserted = 0
    for creature in creatures:
        num_weaknesses = random_int(1, min(3, len(damage_types)))
        for damage_type in random.sample(damage_types, num_weaknesses):
            cursor.execute('SELECT 1 FROM Weaknesses WHERE creature = %s AND damage_type = %s', (creature, damage_type))
            if cursor.fetchone():
                continue

            cursor.execute('''
                INSERT INTO Weaknesses (creature, damage_type, damage_modifier)
                VALUES (%s, %s, %s)
            ''', (creature, damage_type, random_int(0, 20) * 10))
            inserted += 1
    print(f'Добавлено {inserted} записей в Weaknesses')

def fraction_generator(cursor):
    cursor.execute('SELECT creature FROM Bestiary')
    all_creatures = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT fraction_name FROM Fraction')
    existing = set(row[0] for row in cursor.fetchall())

    cursor.execute('SELECT name FROM Weapon')
    weapons = [row[0] for row in cursor.fetchall()]

    if not all_creatures or not weapons:
        return

    word_lists = [
        ['сумасшедшие', 'элитные', 'богатые', 'воинственные', 'высокотехнологичные', 'праведные'],
        ['чернокнижники', 'рыцари', 'буржуи', 'амазонки', 'инфобезники', 'святые отцы'],
        ['из пещеры', 'на конях', 'со связями', 'из джунглей', 'из киберпанка', 'против насилия']
    ]

    num_to_generate = int(len(all_creatures) * random.uniform(0.7, 0.9))
    inserted = 0
    for creature in random.sample(all_creatures, num_to_generate):
        fraction_name = ' '.join(random.choice(words) for words in word_lists)
        if fraction_name in existing:
            continue

        weapon_name = random.choice(weapons)
        cursor.execute('''
            INSERT INTO Fraction (fraction_name, weapon_name, enemy_name)
            VALUES (%s, %s, %s)
        ''', (fraction_name, weapon_name, creature))
        inserted += 1
    print(f'Добавлено {inserted} записей в Fraction')

def main():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            weapon_generator(cursor, 30)
            bestiary_generator(cursor, 30)
            weaknesses_generator(cursor)
            fraction_generator(cursor)
            conn.commit()

if __name__ == '__main__':
    main()