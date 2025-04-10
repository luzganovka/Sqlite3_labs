-- total cost of all weapons with rarity >= 8
SELECT  CHAR(10) || CHAR(10) || 'total cost of all weapons with rarity >= 8' AS message;
select sum(price) from Weapon where rarity >= 8 group by (select (0));

-- sort by damage type and than by name
SELECT  CHAR(10) || CHAR(10) || 'sort by damage type and than by name' AS message;
select name, damage_type from Weapon order by damage_type, name;

-- number of weapons of every damage type
SELECT  CHAR(10) || CHAR(10) || 'number of weapons of every damage type' AS message;
select damage_type, count(name) from Weapon group by damage_type;

-- max rarity of listed weapons
SELECT  CHAR(10) || CHAR(10) || 'max rarity of listed weapons' AS message;
select max(rarity) from Weapon group by (select 0);

-- top list sorted by rarity
SELECT  CHAR(10) || CHAR(10) || 'top list sorted by rarity' AS message;
select rarity, name, damage_type
    from Weapon
    where rarity >= (select max(rarity) from Weapon group by (select 0))
    order by rarity desc
;

SELECT name, rarity
FROM (
    SELECT name, rarity,
           RANK() OVER (ORDER BY rarity DESC) AS rnk
    FROM Weapon
)
WHERE rnk = 1;

-- SELECT name, rarity
-- FROM Weapon
-- WHERE RANK() OVER (ORDER BY rarity DESC) = 1;

-- SELECT name, rarity
-- RANK() OVER (ORDER BY rarity DESC)
-- FROM Weapon
-- WHERE RANK() OVER (ORDER BY rarity DESC);

-- delete rarity, name, damage_type from Weapon where rarity >= (select max(rarity) from Weapon group by (select 0)) order by rarity desc;



-- mean price for weapon of every damage type
SELECT  CHAR(10) || CHAR(10) || 'mean price for weapon of every damage type' AS message;
select damage_type, avg(price) from Weapon group by damage_type;


-- price median
SELECT  CHAR(10) || CHAR(10) || 'price median' AS message;
select avg(price) from (
    select price
        from Weapon
        order by price
        limit (2 - (select count(name) from Weapon group by (select 0)) %2 )
        OFFSET ((select count(name) from Weapon group by (select 0)) -1) / 2
);


SELECT  CHAR(10) || CHAR(10) || 'figure out the most popular damage type' AS message;
-- select damage_type, count(name)
--     from Weapon
--     group by damage_type
-- ;

-- figure out the most popular damage type
select damage_type
    from (
        select damage_type, count(name) as count
        from Weapon
        group by damage_type
    )
    order by count desc
    limit 1
;