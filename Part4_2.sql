-- Using the view
SELECT * FROM YoY_ArrivalByNationality
WHERE countryName = 'Australian'
AND year = 2021;

-- Inserting records into ArrivalByNationality
-- Year: exist, Country: exist
CALL insNewArrivalByNationality(2025, 'Australian', 67);
-- Year: exist, Country: new
CALL insNewArrivalByNationality(2025, 'Kenyan', 67);
-- Year: new, Country: exist
CALL insNewArrivalByNationality(2026, 'Kenyan', 67);
-- Year: new, Country: new
CALL insNewArrivalByNationality(2027, 'Mongolian', 67);

