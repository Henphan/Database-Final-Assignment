-- Using the view
SELECT * FROM YoY_ArrivalByNationality
WHERE countryName = 'Australian'
AND year = 2020;

-- Testing the trigger
-- Updating a record within ArrivalByNationality
UPDATE ArrivalByNationality
SET arrivalCount = arrivalCount + 100
WHERE year = 2024
AND countryId = 19;
-- Checking the audit table
SELECT *
FROM Audit_ArrivalByNationality
WHERE year = 2024
AND countryId = 19;

-- Testing the inserting procedure
-- Inserting records into ArrivalByNationality

-- Year: exist, Country: exist
-- Expected behaviour: duplicate error
CALL insNewArrivalByNationality(2025, 'Australian', 67);

-- Year: exist, Country: new
-- Expected behaviour: valid insert
CALL insNewArrivalByNationality(2025, 'Kenyan', 67);

-- Year: new, Country: exist
-- Expected behaviour: valid insert
CALL insNewArrivalByNationality(2026, 'Kenyan', 67);

-- Year: new, Country: new
-- Expected behaviour: valid insert
CALL insNewArrivalByNationality(2027, 'Mongolian', 67);

-- Year: new, Country: new
-- Expected behaviour: rollback
CALL insNewArrivalByNationality(2027, 'Mongolian', -67);
