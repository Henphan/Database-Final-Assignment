-- Testing transaction handling
-- Inserting records into ArrivalByNationality
-- Year: exist, Country: exist
CALL insNewArrivalByNationality(2025, 'Australian', 67);
    -- Should raise duplicated error
    -- Nothing should be inserted
-- Year: exist, Country: new
CALL insNewArrivalByNationality(2025, 'Kenyan', 67);
    -- Year is not insert
    -- Country is inserted
    -- Transaction should be valid
-- Year: new, Country: exist
CALL insNewArrivalByNationality(2026, 'Kenyan', 67);
-- Year: new, Country: new
CALL insNewArrivalByNationality(2027, 'Mongolian', -10);
    -- 2027 and Mongolian should not be inserted and are rolled-back

