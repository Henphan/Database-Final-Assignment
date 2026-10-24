# Base code is from https://pynative.com/python-mysql-database-connection/ and 
#                      https://realpython.com/python-mysql/

# MySQL connctivity with pytho3 
# Sample code for Practical 09

import mysql.connector
from getpass import getpass

def top_turnover_province(year):
    query = """
        SELECT PT.year, P.name, PT.turnoverAmount
        FROM ProvincialTurnover PT
        INNER JOIN Province P
            ON PT.provinceId = P.provinceId
        WHERE PT.year = %s
        ORDER BY turnoverAmount DESC;
    """
    cur.execute(query, (year,))
    rows = cur.fetchall()
    for (year, province_name, turnover) in rows:
        print(year, province_name, turnover)

def top_arrival_nationality(nationality):
    query = """
        SELECT A.year, A.arrivalCount
        FROM ArrivalByNationality A
        INNER JOIN Country C
            ON A.countryId = C.countryId
        WHERE C.name = %s;
    """
    cur.execute(query, (nationality,))
    rows = cur.fetchall()
    for (year, arrival_count) in rows:
        print(year, arrival_count)

def compare_arrivals_between_years(year1, year2):
    # Comparing international arrivals by different means of transportation between two years.
    # NOTE: should we include A.year?
    # Note: Could be divided by 0
    query = """
        SELECT A.year, T.mode,
            A.arrivalCount,
            A2.arrivalCount,
            (A2.arrivalCount / A.arrivalCount) * 100 - 100 AS growth_pct
        FROM ArrivalByTransport A
        INNER JOIN ArrivalByTransport A2
            ON A.transportId = A2.transportId
        INNER JOIN TransportMode T
            ON A.transportId = T.transportId
        WHERE A.year = %s
          AND A2.year = %s
    """
    cur.execute(query, (year1, year2))
    rows = cur.fetchall()
    for (year, mode, year1_count, year2_count, pct_change) in rows:
        print(year, mode, year1_count, year2_count, pct_change)
def top_turnover_region():
    query = """
        SELECT PT.year, R.name, SUM(PT.turnoverAmount) AS total_turnover
        FROM ProvincialTurnover PT
        INNER JOIN Province P
            ON PT.provinceId = P.provinceId
        INNER JOIN Region R
            ON P.regionId = R.regionId
        WHERE PT.year = 2024
        GROUP BY R.name
        ORDER BY total_turnover DESC;
    """
    cur.execute(query)
    rows = cur.fetchall()
    for (year, region_name, total_turnover) in rows:
        print(year, region_name, total_turnover)

def insert_nationality_arrival(year, nationality, arrival_count):
    query = """
        CALL insNewArrivalByNationality(%s,%s,%s)
    """
    cur.execute(query, (year, nationality, arrival_count))
    conn.commit()


try:
    # define the connection 
    conn = mysql.connector.connect(
                host = "localhost",
                user = input("Enter username: "),
                password = getpass("Enter password: "), 
                database = "Phan_23028920"
                )
    if conn.is_connected():
        # Create a Cursor object to execute queries
        cur = conn.cursor()
        # show the database you are conencted to 
        cur.execute("SELECT DATABASE();")
        record = cur.fetchone()
        print("You're connected to database: ", record)
        print("Vietnam Tourism Database")
        print("Select an operation")
        print("1. View top provincces by tourism turnover")
        print("2. View tourist arrivals by nationality")
        print("3. Compare tourism arrivals between two years")
        print("4. View regional tourism turnover")
        print("5. Insert a new nationality arrival reocrd")
        print("0. Exit")
        
        uinput = 6;
        while uinput != '0':
            uinput = input("Choice: ")
            match uinput:
                case '1':
                    year = input("Enter year: ")
                    top_turnover_province(year)
                case '2':
                    year = input("Enter year: ")
                    nationality = input("Enter nationality: ")
                    top_arrival_nationality(nationality)
                case '3':
                    year1 = input("Enter year 1:")
                    year2 = input("Enter year 2:")
                    compare_arrivals_between_years(year1, year2)
                case '4':
                    top_turnover_region()
                case '5':
                    year = input("Enter year: ")
                    nationality = input("Enter nationality: ")
                    arrival_count = input("Enter arrival count: ")
                    insert_nationality_arrival(year, nationality, arrival_count)
                case '0':
                    print("Exiting...")
                case _:
                    print("Invalid input")

	
except mysql.connector.Error as err:
    print("Error while connecting to MySQL", err)   

finally:
    if conn.is_connected():
        cur.close()
        conn.close()
        print("MySQL connection is closed now")


