--GET ALL BY COUNTRY WITH DATE ORDER
SELECT * 
FROM country_record
WHERE country_code = %s
ORDER BY collect_date;

--INSERT WITH UPDATE
INSERT INTO country_record(country_code, collect_date, sunrise, sunset)
VALUES(%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
sunrise = VALUES(sunrise),
sunset = VALUES(sunset);

--UPDATE
UPDATE country_record SET sunrise = %s, sunset = %s
WHERE country_code = %s AND collect_date = %s;

--DELETE
DELETE FROM country_record
WHERE country_code = %s AND collect_date = %s;