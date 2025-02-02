--GET BY STATUS
SELECT * 
FROM general_weather 
WHERE status_id = %s;

--GET ALL STATUS
SELECT *
FROM general_weather;