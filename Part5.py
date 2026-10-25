# Base code is from https://pynative.com/python-mysql-database-connection/ and 
#                      https://realpython.com/python-mysql/

# MySQL connctivity with pytho3 
# Sample code for Practical 09

import mysql.connector
import subprocess, os
from getpass import getpass

def clear_screen():
    if os.name == 'nt':
        subprocess.run(['cmd', '/c', 'cls'])
    else:
        subprocess.run(['clear'])

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
    if not rows:
        print("No record for the year:", year)
    else:
        header_format = "| {:<10} | {:<20} | {:>19} |"
        print("-" * 59)
        print(header_format.format("Year", "Province", "Turnover (B. VND)"))
        print("-" * 59)
        for (year, province_name, turnover) in rows:
            print(f"| {year:<10} | {province_name:<20} | {turnover:>19,} |")
        print("-" * 59)

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
    if not rows:
        print("No record for the nationality:", nationality)
    else:
        header_format = "| {:<10} | {:>20} |"
        print("-" * 37)
        print(header_format.format("Year", "Arrival Count"))
        print("-" * 37)
        for (year, arrival_count) in rows:
            print(header_format.format(year, arrival_count))
        print("-" * 37)

def compare_arrivals_between_years(year1, year2):
    query = """
        SELECT T.mode, A.arrivalCount, A2.arrivalCount,
        (A2.arrivalCount / A.arrivalCount) * 100 - 100 AS growth_pct
        FROM ArrivalByTransport A
        INNER JOIN ArrivalByTransport A2
        ON A.transportId = A2.transportId
        INNER JOIN TransportMode T
        ON A.transportId = T.transportId
        WHERE A.year = %s
        AND A2.year = %s;
    """
    cur.execute(query, (year1, year2))
    rows = cur.fetchall()
    if not rows:
        print("No record for the combination: {}, {}".format(year1, year2))
    else:
        print("-" * 53)
        header_format = "| {:<10} | {:<10} | {:<10} | {:>10} |"
        print(header_format.format("Mode", year1, year2, "% Change"))
        print("-" * 53)
        for (mode, year1_count, year2_count, pct_change) in rows:
            print(f"| {mode:<10} | {year1_count:<10} | {year2_count:<10} | {pct_change:>10} |")
        print("-" * 53)
def top_turnover_region(year):
    query = """
        SELECT PT.year, R.name, SUM(PT.turnoverAmount) AS total_turnover
        FROM ProvincialTurnover PT
        INNER JOIN Province P
            ON PT.provinceId = P.provinceId
        INNER JOIN Region R
            ON P.regionId = R.regionId
        WHERE PT.year = %s
        GROUP BY R.name
        ORDER BY total_turnover DESC;
    """
    cur.execute(query, (year,))
    rows = cur.fetchall()

    if not rows:
        print("No record for the year:", year)
    else:
        header_format = "| {:<7} | {:<40} | {:>19} |"
        print("-" * 75)
        print(header_format.format("Year", "Region", "Turnover (B. VND)"))
        print("-" * 75)

        for (year, region_name, total_turnover) in rows:
            print(f"| {year:<7} | {region_name:<40} | {total_turnover:>19,.2f} |")

        print("-" * 75)


def insert_nationality_arrival(year, nationality, arrival_count):
    query = """
        CALL insNewArrivalByNationality(%s, %s, %s)
    """
    cur.execute(query, (year, nationality, arrival_count))
    conn.commit()

    header_format = "| {:<20} | {:<20} |"
    print("-" * 47)
    print(header_format.format("Field", "Inserted Value"))
    print("-" * 47)
    print(header_format.format("Year", year))
    print(header_format.format("Nationality", nationality))
    print(f"| {'Arrival Count':<20} | {int(arrival_count):<20,} |")
    print("-" * 47)
    print("Record inserted successfully.")

def display_menu():
    print("Vietnam Tourism Database")
    print("Select an operation")
    print("1. View top provinces by tourism turnover for a year")
    print("2. View tourist arrivals over the years by nationality")
    print("3. Compare tourism arrivals between two years")
    print("4. View top regions by tourism turnover for a year")
    print("5. Insert a new nationality arrival record")
    print("0. Exit")

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
        
        uinput = 6;
        while uinput != '0':
            clear_screen()
            display_menu()
            uinput = input("Choice: ")
            match uinput:
                case '1':
                    year = input("Enter year: ")
                    top_turnover_province(year)
                case '2':
                    nationality = input("Enter nationality: ")
                    top_arrival_nationality(nationality)
                case '3':
                    year1 = input("Enter the before year: ")
                    year2 = input("Enter the after year: ")
                    compare_arrivals_between_years(year1, year2)
                case '4':
                    year = input("Enter year: ")
                    top_turnover_region(year)
                case '5':
                    year = input("Enter year: ")
                    nationality = input("Enter nationality: ")
                    arrival_count = input("Enter arrival count: ")
                    insert_nationality_arrival(year, nationality, arrival_count)
                case '0':
                    print("Exiting...")
                case _:
                    print("Invalid input")
            input("Press <Enter> to continue")

	
except mysql.connector.Error as err:
    if err.errno == '1062':
        print("An entry for ({}, {}) already exists.".format(year, nationality))
    elif err.errno == '1264':
        print("The arrival count <{}> is invalid.".format(arrival_count))
    else:
        print("Error while connecting to MySQL", err)   
finally:
    if conn.is_connected():
        cur.close()
        conn.close()
        print("MySQL connection is closed now")


