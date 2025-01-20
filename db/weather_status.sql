--GET BY CITY AND TIME
SELECT *
FROM weather_status
WHERE city_id = %s AND collect_time = %s;

--GET ALL BY CITY
SELECT *
FROM weather_status
WHERE city_id = %s;

--INSERT
INSERT INTO weather_status(city_id, collect_time, base, temp, feels_temp, temp_min, temp_max, 
pressure, humidity, sea_level, grnd_level, visibility, wind_speed, wind_deg, wind_gust, clouds_all)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

--DELETE
DELETE FROM weather_status
WHERE city_id = %s AND collect_time = %s;

--DELETE ALL BY CITY
DELETE FROM weather_status
WHERE city_id = %s;