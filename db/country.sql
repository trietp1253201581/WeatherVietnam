--GET BY CODE
SELECT * 
FROM country
WHERE country_code = %s;

--INSERT WITH UPDATE
INSERT INTO country(country_code, name)
VALUES(%s, %s)
ON DUPLICATE KEY UPDATE
name = VALUES(name);

--DELETE
DELETE FROM country
WHERE country_code = %s;