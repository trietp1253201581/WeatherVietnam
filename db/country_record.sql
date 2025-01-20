--GET BY CODE AND DATE
SELECT * 
FROM country_record
WHERE country_code = %s AND collect_date = %s;

--GET ALL BY CODE
SELECT * 
FROM country_record
WHERE country_code = %s;

--INSERT 
INSERT INTO country_record(country_code, collect_date, sunrise, sunset)
VALUES(%s, %s, %s, %s);

--UPDATE
UPDATE country_record SET sunrise = %s, sunset = %s
WHERE country_code = %s AND collect_date = %s;

--DELETE
DELETE FROM country_record
WHERE country_code = %s AND collect_date = %s;