PRAGMA foreign_keys = ON;

-- Таблица оружия
CREATE TABLE Weapon (
    name TEXT PRIMARY KEY,
    basic_damage REAL NOT NULL,
    damage_type TEXT NOT NULL,
    cooldown INT NOT NULL, --(мс/удар) - минимальное время (в мс) между двумя ударами (НЕ СКОРОСТЬ)
    rarity INTEGER,
    price REAL,
    description TEXT
);

-- Таблица игроков
CREATE TABLE Player (
    id INTEGER PRIMARY KEY,
    fraction TEXT,
    name TEXT
);

-- Таблица сущностей (владение оружием)
CREATE TABLE Entity (
    id INTEGER PRIMARY KEY,
    owner_id INTEGER NOT NULL,
    weapon_name TEXT NOT NULL,
    weapon_level INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES Player(id) ON DELETE CASCADE,
    FOREIGN KEY (weapon_name) REFERENCES Weapon(name) ON DELETE CASCADE
);

-- Таблица слабостей существ
CREATE TABLE Weaknesses (
    creature TEXT NOT NULL,
    damage_type TEXT NOT NULL,
    damage_modifier INTEGER NOT NULL,
    PRIMARY KEY (creature, damage_type)
    FOREIGN KEY (creature) REFERENCES Bestiary(creature) ON DELETE CASCADE
);

-- Таблица бестиария
CREATE TABLE Bestiary (
    creature TEXT PRIMARY KEY,
    biome TEXT NOT NULL,
    danger INTEGER NOT NULL
);

-- Таблица фракций
CREATE TABLE Fraction (
    fraction_name TEXT PRIMARY KEY,
    weapon_name TEXT,
    enemy_name TEXT,
    FOREIGN KEY (weapon_name)   REFERENCES Weapon  (name)       ON DELETE CASCADE
    FOREIGN KEY (enemy_name)    REFERENCES Bestiary(creature)   ON DELETE CASCADE
);