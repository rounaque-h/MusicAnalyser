import mysql.connector

#Make sure to replace "your_username", "your_password", and "your_database" with your actual MySQL credentials and database name.

def create_table():
    # Establish a connection to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the SQL query to create the table
    create_table_query = """
    CREATE TABLE MusicData (
        Song_name VARCHAR(255),
        Artist VARCHAR(255),
        Language VARCHAR(255),
        Genre VARCHAR(255),
        Release_date VARCHAR(255),
        Pitch VARCHAR(255),
        Loudness VARCHAR(255)
    )
    """

    # Execute the create table query
    cursor.execute(create_table_query)

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

# Call the function to create the table
create_table()
