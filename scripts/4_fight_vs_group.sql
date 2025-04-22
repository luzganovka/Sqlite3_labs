--создать группу существ
WITH Enemies AS (
    SELECT creature
    FROM Bestiary
    ORDER BY RANDOM()
    LIMIT 5
),
--выбрать партию игроков
Heroes AS (
    SELECT id
    FROM Player
    ORDER BY RANDOM()
    LIMIT 2
),
--выбрать всё оружте игроков
HeroesArsenal AS (
    SELECT id
    FROM Entity
    WHERE owner_id IN Heroes
),

-- Все существующие типы урона - вспомагательный для следующего
AllDamageTypes AS (
    SELECT DISTINCT damage_type FROM Weapon
),
-- Все возможные комбинации существ и типов урона, включая отсутствующие
AllWeaknesses AS (
    SELECT 
        Bestiary.creature,
        AllDamageTypes.damage_type,
        IFNULL(Weaknesses.damage_modifier, 100) AS damage_modifier
    FROM Bestiary
    CROSS JOIN AllDamageTypes
    LEFT JOIN Weaknesses 
        ON Bestiary.creature = Weaknesses.creature 
        AND AllDamageTypes.damage_type = Weaknesses.damage_type
),

--рассчитать эффективность оружия против группы
Efficiency AS (
    SELECT
        Entity.id AS eid,
        Weapon.name AS wname,
        Weapon.basic_damage * Entity.weapon_level * (AllWeaknesses.damage_modifier / 100) AS eff,
        AllWeaknesses.creature AS creature
    FROM Entity
    JOIN Weapon ON Entity.weapon_name = Weapon.name
    JOIN AllWeaknesses ON Weapon.damage_type = AllWeaknesses.damage_type
    WHERE AllWeaknesses.creature IN Enemies
    AND Entity.id IN HeroesArsenal
),

-- Average efficiency of certain entity against the whole group
AvgEff AS (
    SELECT eid, wname, AVG(eff) as avgeff
    FROM Efficiency
    GROUP BY eid
),

-- TODO: select top 2 ordered by avgeff
TopEff AS (
    SELECT eid, wname, avgeff
    FROM AvgEff
    ORDER BY avgeff DESC
    LIMIT 2
)

-- MAIN
SELECT * FROM TopEff;