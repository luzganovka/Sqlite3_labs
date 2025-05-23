-- Таблица оружия
CREATE TABLE Weapon (
    name TEXT PRIMARY KEY,
    basic_damage REAL NOT NULL,
    damage_type TEXT NOT NULL,
    rarity INTEGER,
    price REAL,
    description TEXT
);

-- Таблица игроков
CREATE TABLE Player (
    id SERIAL PRIMARY KEY,
    fraction TEXT,
    name TEXT
);

-- Таблица бестиария
CREATE TABLE Bestiary (
    creature TEXT PRIMARY KEY,
    biome TEXT NOT NULL,
    danger INTEGER NOT NULL
);

-- Таблица слабостей существ
CREATE TABLE Weaknesses (
    creature TEXT NOT NULL,
    damage_type TEXT NOT NULL,
    damage_modifier INTEGER NOT NULL,
    PRIMARY KEY (creature, damage_type),
    FOREIGN KEY (creature) REFERENCES Bestiary(creature) ON DELETE CASCADE
);

-- Таблица сущностей (владение оружием)
CREATE TABLE Entity (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER,
    weapon_name TEXT NOT NULL,
    weapon_level INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES Player(id) ON DELETE CASCADE,
    FOREIGN KEY (weapon_name) REFERENCES Weapon(name) ON DELETE CASCADE
);

-- Таблица фракций
CREATE TABLE Fraction (
    fraction_name TEXT PRIMARY KEY,
    weapon_name TEXT,
    enemy_name TEXT,
    FOREIGN KEY (weapon_name) REFERENCES Weapon(name) ON DELETE CASCADE,
    FOREIGN KEY (enemy_name)  REFERENCES Bestiary(creature) ON DELETE CASCADE
);