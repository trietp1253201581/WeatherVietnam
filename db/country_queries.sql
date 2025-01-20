--GET BY CODE
SELECT * 
FROM country
WHERE country_code = %s;

--INSERT
INSERT INTO country(country_code, name)
VALUES(%s, %s);

--UPDATE
UPDATE country SET name = %s
WHERE country_code = %s;

--DELETE
DELETE FROM country
WHERE country_code = %s;