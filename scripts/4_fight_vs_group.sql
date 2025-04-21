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
)

--рассчитать эффективность оружия против группы
SELECT Entity.id,
    Weapon.basic_damage * Entity.weapon_level * (Weaknesses.damage_modifier / 100) AS efficiency,
    Weaknesses.creature
FROM Entity
JOIN Weapon ON Entity.weapon_name = Weapon.name
JOIN Weaknesses ON Weapon.damage_type = Weaknesses.damage_type
WHERE Weaknesses.creature IN Enemies
AND Entity.id IN HeroesArsenal
;