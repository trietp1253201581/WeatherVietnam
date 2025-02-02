--GET BY ID
SELECT * 
FROM city
WHERE city_id = %s;

--GET BY NAME
SELECT * 
FROM city
WHERE name = %s;

--GET ALL BY COUNTRY
SELECT *
FROM city
WHERE country_code = %s;

--INSERT WITH UPDATE
INSERT INTO city(city_id, name, lon, lat, time_zone, country_code)
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
name = VALUES(name),
lon = VALUES(lon),
lat = VALUES(lat),
time_zone = VALUES(time_zone),
country_code = VALUES(country_code);

--UPDATE
UPDATE city SET name = %s, lon = %s, lat = %s,
time_zone = %s, country_code = %s
WHERE city_id = %s;

--DELETE
DELETE FROM city
WHERE city_id = %s;

--DELETE ALL BY COUNTRY
DELETE FROM city
WHERE country_code = %s;