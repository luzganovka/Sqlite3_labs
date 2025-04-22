--выбрать оружие
WITH MyWeapon AS (
    SELECT *
    FROM Weapon
    ORDER BY RANDOM()
    LIMIT 1
),

--выбрать врага и посчитать его хиты
MyEnemy AS (
    SELECT
        Bestiary.creature,
        danger * 100 * (IFNULL(Weaknesses.damage_modifier, 100) / 100.0) AS hp
    FROM Bestiary
    JOIN MyWeapon
    JOIN Weaknesses
        ON MyWeapon.damage_type == Weaknesses.damage_type
        AND Bestiary.creature == Weaknesses.creature
    ORDER BY RANDOM()
    LIMIT 1
),

-- найти всё оружие конкретного типа
-- и рассчитать для него время боя (в миллисекундах!)
FightTime AS (
    SELECT 
        Entity.id AS eid,
        MyWeapon.basic_damage * (1 + log(Entity.weapon_level + 1)) AS dmg,
        CAST (MyEnemy.hp / (MyWeapon.basic_damage * (1 + log(Entity.weapon_level + 1))) + 1 AS INTEGER) * MyWeapon.cooldown AS fight_time
    FROM MyWeapon
    JOIN Entity ON Entity.weapon_name = MyWeapon.name
    JOIN MyEnemy
),

Pretty AS (
    SELECT
        eid, dmg,
        CAST(MOD(fight_time, 1000) AS INTEGER)              AS nanosec,
        CAST(   fight_time / 1000 AS INTEGER)               AS sec,
        CAST(   fight_time / (1000 * 60) AS INTEGER)        AS min,
        CAST(   fight_time / (1000 * 60 * 60) AS INTEGER)   AS hrs

    FROM FightTime

)

-- MAIN
SELECT * FROM Pretty;