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

        -- Rollback when an error occurs
        DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            ROLLBACK;
            RESIGNAL;
        END;

        -- Starting the transaction
        START TRANSACTION;

        -- Check if the year exists, if not then insert
        IF p_year NOT IN (
            SELECT year
            FROM Year
        ) THEN
            INSERT INTO Year
            VALUES (p_year);
        END IF;

        -- Check if the country exists, if not then insert
        IF p_countryName NOT IN (
            SELECT name
            FROM Country
        ) THEN
            INSERT INTO Country (name, continent)
            VALUES (p_countryName, NULL);

            -- retrieves the countryId
            SET nextCountryId = LAST_INSERT_ID();
        -- if it is then find its countryId
        ELSE
        -- NOTE: Assuming that country names are unique
            SELECT countryId INTO nextCountryId
            FROM Country
            WHERE name = p_countryName;
        END IF;

        -- Insert into ArrivalByNationality
        INSERT INTO ArrivalByNationality
        VALUES (p_year, nextCountryId, p_arrivalCount);

        COMMIT;
    END //
DELIMITER ;


DROP TRIGGER after_ArrivalByNationality_update;
DELIMITER //
CREATE TRIGGER after_ArrivalByNationality_update
    AFTER UPDATE ON ArrivalByNationality
    FOR EACH ROW
    BEGIN
        IF NOT (OLD.arrivalCount <=> NEW.arrivalCount) THEN
            INSERT INTO Audit_ArrivalByNationality (
                year,
                countryId,
                old_arrivalCount,
                new_arrivalCount,
                audit_time
            )
                VALUES (
                    NEW.year,
                    NEW.countryId,
                    OLD.arrivalCount,
                    NEW.arrivalCount,
                    CURRENT_TIMESTAMP
                );
        END IF;
    END //
DELIMITER ;


DROP VIEW YoY_ArrivalByNationality;
CREATE VIEW YoY_ArrivalByNationality (year, countryName, previous_year, current_year, pct_change) AS
    SELECT A1.year, C.name, A2.arrivalCount, A1.arrivalCount,
    (A1.arrivalCount / A2.arrivalCount * 100) - 100
    FROM ArrivalByNationality A1
    INNER JOIN ArrivalByNationality A2
    ON A1.countryId = A2.countryId
    AND A1.year = A2.year + 1
    INNER JOIN Country C
    ON C.countryId = A1.countryId;
