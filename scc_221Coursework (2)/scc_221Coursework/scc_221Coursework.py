import mysql.connector
import csv
import plotly.graph_objects as go
import plotly.io as pio  # Import plotly.io to control the renderer

# Set the default renderer to 'browser' to avoid using kaleido
pio.renderers.default = "browser"  # This ensures the plot is shown in the browser

# Database configuration with empty values for host, user, and password
DB_CONFIG = {
    "host": "localhost",  # Empty string for host
    "user": "root",  # Empty string for user
    "password": "Ali_Ahmed7504",  # Empty string for password
    "database": "scc_221Coursework"
}


def create_database():
    """Creates the scc_221Coursework database if it doesn't exist."""
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS scc_221Coursework;")
    conn.commit()
    conn.close()


def connect_to_database():
    """Connects to the scc_221Coursework database."""
    return mysql.connector.connect(**DB_CONFIG)


def create_tables(conn):
    """Creates all tables required for the scc_221Coursework database."""
    cursor = conn.cursor()
    
    # Create all tables

    cursor.execute("""
     CREATE TABLE IF NOT EXISTS TennisTour (
        TourName VARCHAR(60),
        prizeMoney INT,
        Organizer VARCHAR(50),
        PRIMARY KEY (TourName)
    );
    """)
    
    # PRIMARY KEY (TourName, SponsorBrand) is a composite key because sponsor is a weak entity
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS sponsorsPartneredWith (
        TourName VARCHAR(60),
        sponsorBrand varchar(20),
        sponsorPhoneNum varchar(11),
        sponsorDuration TEXT,
        PRIMARY KEY (TourName, sponsorBrand),
        FOREIGN KEY (TourName) REFERENCES TennisTour(TourName) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
     CREATE TABLE IF NOT EXISTS playersRegistered (
        TourName VARCHAR(60),
        playerID INT,
        playerDominantHand varchar(10),
        playerName varchar(30),
        PRIMARY KEY (playerID),
        FOREIGN KEY (TourName) REFERENCES TennisTour(TourName) ON DELETE SET NULL
    );
    """)

    cursor.execute("""
     CREATE TABLE IF NOT EXISTS tournamentsHosted (
        TourName VARCHAR(60),
        tournamentName varchar(30),
        tournamentLocation TEXT,
        tournamentCapacity INT,
        PRIMARY KEY (tournamentName),
        FOREIGN KEY (TourName) REFERENCES TennisTour(TourName) ON DELETE CASCADE
    );
    """)
    
    conn.commit()


def populate_table_from_csv(conn, table_name, csv_file):
    """Populates a specified table from a CSV file."""
    cursor = conn.cursor()

    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        if table_name == "TennisTour":
            query = """
            INSERT INTO TennisTour (
                TourName, prizeMoney, Organizer
            ) VALUES (%s, %s, %s)
            """
            for row in reader:
                try:
                    cursor.execute(query, row)
                except Exception as e:
                    print(f"Error inserting into TennisTour, row {row}: {e}")
        
        elif table_name == "sponsorsPartneredWith":
            query = """
            INSERT INTO sponsorsPartneredWith (
                TourName, sponsorBrand, sponsorPhoneNum, sponsorDuration
            ) VALUES (%s, %s, %s, %s)
            """
            for row in reader:
                try:
                    cursor.execute(query, row)
                except Exception as e:
                    print(f"Error inserting into sponsorsPartneredWith, row {row}: {e}")

        elif table_name == "playersRegistered":
            query = """
            INSERT INTO playersRegistered (
                TourName, playerID, playerDominantHand, playerName
            ) VALUES (%s, %s, %s, %s)
            """
            for row in reader:
                try:
                    cursor.execute(query, row)
                except Exception as e:
                    print(f"Error inserting into palbasics, row {row}: {e}")

        elif table_name == "tournamentsHosted":
            query = """
            INSERT INTO tournamentsHosted (
                TourName, tournamentName, tournamentLocation, tournamentCapacity
            ) VALUES (%s, %s, %s, %s)
            """
            for row in reader:
                try:
                    cursor.execute(query, row)
                except Exception as e:
                    print(f"Error inserting into palbasics, row {row}: {e}")
    
    conn.commit()
    print(f"Data successfully inserted into {table_name} from {csv_file}")


def query_and_plot(conn):
    """Queries playerDominantHand from playersRegistered for ATP players only and displays a bar chart."""
    cursor = conn.cursor()
    cursor.execute("SELECT playerDominantHand FROM playersRegistered WHERE TourName = 'ATP';")
    
    # Fetch all rows of the query result
    data = cursor.fetchall()

    # Check if data is None or empty
    if data is None or len(data) == 0:
        print("No data found in the playerdRegistered table. Exiting.")
        return

    # Extract statsattackmelee values
    playerDominantHand_values = [row[0] for row in data]

    # Create a frequency dictionary for statsattackmelee values
    value_counts = {}
    for value in playerDominantHand_values:
        value_counts[value] = value_counts.get(value, 0) + 1

    # Convert the dictionary to two lists: one for the values and one for the counts
    values = list(value_counts.keys())
    counts = list(value_counts.values())
    
    # Create a bar chart using Plotly
    bar_chart = go.Figure(data=[
        go.Bar(
            x=values,
            y=counts,
            text=counts,  # Display the count on top of each bar
            textposition='auto',
            marker=dict(color='royalblue')
        )
    ])
    
    # Update layout for better appearance
    bar_chart.update_layout(
        title="Bar Chart of ATP players' dominant hand",
        xaxis_title="playerDominantHand",
        yaxis_title="Count",
        template="plotly_dark"
    )
    
    # Display the bar chart in a web browser (default renderer)
    bar_chart.show()

#############################################################################################################

    cursor1 = conn.cursor()
    cursor1.execute("SELECT TourName, prizeMoney FROM TennisTour;")
    
    # Fetch all rows of the query result
    data = cursor1.fetchall()

    # Check if data is None or empty
    if data is None or len(data) == 0:
        print("No data found in the TennisTour table. Exiting.")
        return

    tour_names = [row[0] for row in data]
    prize_money_values = [row[1] for row in data]

    # Create a bar chart using Plotly
    bar_chart = go.Figure(data=[
        go.Bar(
            x=tour_names,
            y=prize_money_values,
            text=prize_money_values,  # Display the prize money on top of each bar
            textposition='auto',
            marker=dict(color='royalblue')
        )
    ])
    
    # Update layout for better appearance
    bar_chart.update_layout(
        title="Prize Money Distribution Across Tennis Tours",
        xaxis_title="Tour Name",
        yaxis_title="Prize Money",
        template="plotly_dark"
    )
    
    # Display the bar chart
    bar_chart.show()

#############################################################################################################

    cursor2 = conn.cursor()
    
    # Query to fetch sponsorBrand counts for specific TourNames
    cursor2.execute("""
        SELECT TourName, COUNT(sponsorBrand) AS sponsorCount
        FROM sponsorsPartneredWith
        WHERE TourName IN ('ATP', 'WTA', 'GTFT')
        GROUP BY TourName;
    """)
    
    # Fetch all rows of the query result
    data = cursor2.fetchall()

    # Check if data is None or empty
    if data is None or len(data) == 0:
        print("No data found in the sponsorsPartneredWith table. Exiting.")
        return

    # Separate the data into TourNames and their corresponding sponsor counts
    tour_names = [row[0] for row in data]
    sponsor_counts = [row[1] for row in data]

    # Create a bar chart using Plotly
    bar_chart = go.Figure(data=[
        go.Bar(
            x=tour_names,
            y=sponsor_counts,
            text=sponsor_counts,  # Display the count on top of each bar
            textposition='auto',
            marker=dict(color='royalblue')
        )
    ])
    
    # Update layout for better appearance
    bar_chart.update_layout(
        title="Sponsor Counts for ATP, WTA, and GTFT",
        xaxis_title="Tour Name",
        yaxis_title="Sponsor Count",
        template="plotly_dark"
    )
    
    # Display the bar chart
    bar_chart.show()

#############################################################################################################

    cursor3 = conn.cursor()
    cursor3.execute("SELECT tournamentCapacity FROM tournamentsHosted;")
    
    # Fetch all rows of the query result
    data = cursor3.fetchall()

    # Check if data is None or empty
    if data is None or len(data) == 0:
        print("No data found in the tournamentsHosted table. Exiting.")
        return

    # Extract statsattackmelee values
    tournamentCapacity_values = [row[0] for row in data]

    # Create a frequency dictionary for statsattackmelee values
    value_counts = {}
    for value in tournamentCapacity_values:
        value_counts[value] = value_counts.get(value, 0) + 1

    # Convert the dictionary to two lists: one for the values and one for the counts
    values = list(value_counts.keys())
    counts = list(value_counts.values())
    
    # Create a bar chart using Plotly
    bar_chart = go.Figure(data=[
        go.Bar(
            x=values,
            y=counts,
            text=counts,  # Display the count on top of each bar
            textposition='auto',
            marker=dict(color='royalblue')
        )
    ])
    
    # Update layout for better appearance
    bar_chart.update_layout(
        title="Bar Chart of tournament capacities for tournaments globally",
        xaxis_title="tournamentCapacity",
        yaxis_title="Count",
        template="plotly_dark"
    )
    
    # Display the bar chart in a web browser (default renderer)
    bar_chart.show()

def main():
    """Main function to orchestrate the tasks."""
    # Step 1: Create the database
    create_database()
    
    # Step 2: Connect to the database
    conn = connect_to_database()
    
    # Step 3: Create tables
    create_tables(conn)
    
    # Step 4: Populate tables from CSV files
    try:
        populate_table_from_csv(conn, "TennisTour", "TennisTour.csv")
        populate_table_from_csv(conn, "sponsorsPartneredWith", "sponsorsPartneredWith.csv")
        populate_table_from_csv(conn, "playersRegistered", "playersRegistered.csv")
        populate_table_from_csv(conn, "tournamentsHosted", "tournamentsHosted.csv")

    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure the CSV files are in the correct location.")
        conn.close()
        return
    
    # Step 5: Query and plot bar chart
    query_and_plot(conn)
    
    # Step 7: Close the connection
    conn.close()


if __name__ == "__main__":
    main()