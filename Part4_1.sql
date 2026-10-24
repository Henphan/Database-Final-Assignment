DROP PROCEDURE insNewArrivalByNationality;
DELIMITER //
CREATE PROCEDURE insNewArrivalByNationality(
    p_year INT,
    p_countryName VARCHAR(50),
    p_arrivalCount INT
)
    COMMENT 'Insert new record into ArrivalByNationality.'
    BEGIN
        DECLARE nextCountryId INT;

        -- TODO: Add rollback
        -- Check if the year exists
        IF p_year NOT IN (
            SELECT year
            FROM Year
        ) THEN
            INSERT INTO Year
            VALUES (p_year);
        END IF;

        -- Check if the country exists
        IF p_countryName NOT IN (
            SELECT name
            FROM Country
        ) THEN
            INSERT INTO Country (name, continent)
            VALUES (p_countryName, NULL);

            SET nextCountryId = LAST_INSERT_ID();
        ELSE
        -- NOTE: Assuming that country names are unique
            SELECT countryId INTO nextCountryId
            FROM Country
            WHERE name = p_countryName;
        END IF;

        -- Insert into ArrivalByNationality
        INSERT INTO ArrivalByNationality
        VALUES (p_year, nextCountryId, p_arrivalCount);
    END //
DELIMITER ;


DROP TRIGGER after_ArrivalByNationality_update;
DELIMITER //
CREATE TRIGGER before_ArrivalByNationality_update
    BEFORE UPDATE ON ArrivalByNationality
    FOR EACH ROW
    BEGIN
        DECLARE err_msg_invalid_count VARCHAR(100);
        SET err_msg_invalid_count = CONCAT('The new arrival count', NEW.arrivalCount, ' cannot be less than 0');
        IF NEW.arrivalCount < 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = err_msg_invalid_count;
        END IF;
    END //
DELIMITER ;


DROP VIEW YoY_ArrivalByNationality;
CREATE VIEW YoY_ArrivalByNationality (year, countryName, previous_year, current_year, pct_change) AS
    SELECT A1.year, C.name, A1.arrivalCount AS previous_year, A2.arrivalCount, 100 - (A2.arrivalCount / A1.arrivalCount * 100)
    FROM ArrivalByNationality A1
    INNER JOIN ArrivalByNationality A2
    ON A1.countryId = A2.countryId
    AND A1.year = A2.year + 1
    INNER JOIN Country C
    ON C.countryId = A1.countryId;
