--GET BY CITY AND TIME
SELECT *
FROM weather_status
WHERE city_id = %s AND collect_time = %s;

--GET ALL BY CITY
SELECT *
FROM weather_status
WHERE city_id = %s;

--INSERT
INSERT INTO weather_status (city_id, collect_time, temp, feels_temp, pressure, humidity, 
sea_level, grnd_level, visibility, wind_speed, wind_deg, wind_gust, clouds_all,
rain, sunrise, sunset, aqi, pm2_5)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    temp = VALUES(temp),
    feels_temp = VALUES(feels_temp),
    pressure = VALUES(pressure),
    humidity = VALUES(humidity),
    sea_level = VALUES(sea_level),
    grnd_level = VALUES(grnd_level),
    visibility = VALUES(visibility),
    wind_speed = VALUES(wind_speed),
    wind_deg = VALUES(wind_deg),
    wind_gust = VALUES(wind_gust),
    clouds_all = VALUES(clouds_all),
    rain = VALUES(rain),
    sunrise = VALUES(sunrise),
    sunset = VALUES(sunset),
    aqi = VALUES(aqi),
    pm2_5 = VALUES(pm2_5);

--DELETE
DELETE FROM weather_status
WHERE city_id = %s AND collect_time = %s;

--DELETE ALL BY CITY
DELETE FROM weather_status
WHERE city_id = %s;