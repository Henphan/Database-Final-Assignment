-- Average expenditures across the recorded categories for domestic and international tourists SELECT year, AVG(expenditureAmount) FROM ExpenditureByCategory
SELECT year, AVG(expenditureAmount), currency
FROM ExpenditureByCategory
GROUP BY year, currency;

-- Provinces with highest turnovers
SELECT PT.year, P.name, PT.turnoverAmount
FROM ProvincialTurnover PT
INNER JOIN Province P
ON PT.provinceId = P.provinceId
WHERE PT.year = 2024
ORDER BY turnoverAmount DESC;

-- Regions with highest turnovers
SELECT PT.year, R.name, SUM(PT.turnoverAmount) AS total_turnover
FROM ProvincialTurnover PT
INNER JOIN Province P
ON PT.provinceId = P.provinceId
INNER JOIN Region R
ON P.regionId = R.regionId
WHERE PT.year = 2024
GROUP BY R.name
ORDER BY total_turnover DESC;

-- How many Australian tourists visited Vietnam each year from 2015 onwards?
SELECT A.year, A.arrivalCount
FROM ArrivalByNationality A
INNER JOIN Country C
ON A.countryId = C.countryId
WHERE C.name = 'Australian';

 -- Expenditures that exceeded the average across all categories
SELECT E.year, EC.category, E.expenditureAmount
FROM ExpenditureByCategory E
INNER JOIN ExpenditureCategory EC
ON E.categoryId = EC.categoryId
INNER JOIN TouristType T
ON E.typeId = T.typeId
WHERE T.type = 'International'
AND E.expenditureAmount > (
  SELECT AVG(E1.expenditureAmount)
  FROM ExpenditureByCategory E1
  WHERE E.year = E1.year
  AND E.typeId = E1.typeId
)
ORDER BY E.year;

-- How did international arrivals by air, road, and water change between '19 and '24
-- Show the percentage growth
SELECT T.mode, A.arrivalCount, A2.arrivalCount,
(A2.arrivalCount / A.arrivalCount) * 100 - 100 AS growth_pct
FROM ArrivalByTransport A
INNER JOIN ArrivalByTransport A2
ON A.transportId = A2.transportId
INNER JOIN TransportMode T
ON A.transportId = T.transportId
WHERE A.year = '2019'
AND A2.year = '2024';

-- Which countries had more arrivals than avg. nationality's arrivals in 2024
SELECT A.year, C.name, A.arrivalCount
FROM ArrivalByNationality A
INNER JOIN Country C
ON A.countryId = C.countryId
WHERE A.year = 2024
AND A.arrivalCount > (
  SELECT AVG(arrivalCount)
  FROM ArrivalByNationality
  WHERE year = A.year
);

-- Which provinces have names containing 'Quang', display their tourism turnovers in 2023
SELECT PT.year, P.name, PT.turnoverAmount
FROM ProvincialTurnover PT
INNER JOIN Province P
ON PT.provinceId = P.provinceId
WHERE P.name LIKE "%Quang%"
AND PT.year = 2023;
