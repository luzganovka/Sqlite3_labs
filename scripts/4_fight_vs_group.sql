--создать группу существ
WITH enemies AS (
    SELECT creature
    FROM (
        SELECT creature,
            RANK() OVER (ORDER BY creature DESC) AS rnk
        FROM Bestiary
    )
    WHERE rnk = 1 OR rnk = 20 OR rnk = 40
),
--выбрать партию игроков
heroes AS (
    SELECT id
    FROM Player
    WHERE id = 1 OR id = 5 OR id = 10
),
--выбрать всё оружте игроков
heroes_arsenal AS (
    SELECT id
    FROM Entity
    WHERE owner_id IN heroes
)

--рассчитать эффективность оружия против группы
SELECT Entity.id, Weapon.basic_damage * Entity.weapon_level * (Weaknesses.damage_modifier / 100), Weaknesses.creature
FROM Entity
JOIN Weapon ON Entity.weapon_name = Weapon.name
JOIN Weaknesses ON Weapon.damage_type = Weaknesses.damage_type
WHERE Weaknesses.creature IN enemies
AND Entity.id IN heroes_arsenal
;