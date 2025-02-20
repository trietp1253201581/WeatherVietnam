--GET ALL BY CITY AND TIME
SELECT *
FROM weather_condition
WHERE city_id = %s AND collect_time = %s;

--INSERT 
INSERT INTO weather_condition(city_id, collect_time, general_weather_status)
VALUES(%s, %s, %s);

--DELETE
DELETE FROM weather_condition
WHERE city_id = %s AND collect_time = %s;