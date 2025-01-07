import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# Function to process each line of the text file and extract the required data
def process_line(line):
    """
    Process a single line of text and extract the required data into 7 elements.
    :param line: String containing the data of a single constituency.
    :return: List of 7 elements: ['constituency', 'first_party', 'second_party', 'majority', 'majority_percentage', 'winning_candidate', 'new_mp']
    """
    # Split the line by spaces
    parts = line.split()

    # Find the index of the % symbol using generator expression
    percent_index = next(i for i, part in enumerate(parts) if '%' in part)

    # Extract the second, third and fourth elements
    majority_percentage = parts[percent_index]
    majority = parts[percent_index - 1]
    second_party = parts[percent_index - 2]
    first_party = parts[percent_index - 3]

    # Extract the constituency name
    constituency = ' '.join(parts[:percent_index - 3])

    # Extract winning candidate name and new MP status
    winning_candidate_parts = parts[percent_index + 1:-1]
    winning_candidate = ' '.join(winning_candidate_parts)
    new_mp = parts[-1]

    # Return the extracted data as a list
    return [constituency, first_party, second_party, majority, majority_percentage, winning_candidate, new_mp]


# Function to process the text file and create a DataFrame
def process_text_file(file_path):
    """
    Process the text file and create a DataFrame with the required data.
    :param file_path: The path to the text file containing the constituency data.
    :return: Pandas DataFrame with the extracted data.
    """
    data = []

    # Open the text file and process each line
    with open(file_path, 'r') as file:
        for line in file:
            # Process each line and add the extracted data to the list
            processed_line = process_line(line.strip())
            data.append(processed_line)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=['constituency', 'first_party', 'second_party', 'majority', 'majority_percentage', 'winning_candidate', 'new_mp'])

    return df


# Function to retrieve IDs from table where needed
# noinspection SqlResolve
def get_id_from_table(session, table_name, column_name, value):
    """
    This function retrieves the ID from a given table where the column matches the specified value.
    :param session: The SQLAlchemy session object.
    :param table_name: The name of the table.
    :param column_name: The name of the column.
    :param value: The value to match in the column.
    :return: The ID of the matching row.
    """
    query = text(f"SELECT ID FROM {table_name} WHERE {column_name} = :value")
    result = session.execute(query, {'value': value}).fetchone()
    return result[0] if result else None


# Function to map party names
def map_abbreviated_to_full(party_name):
    """
    This function maps party names to their corresponding IDs.
    :param party_name: The abbreviated name of the party.
    :return: The full name of the party.
    """
    party_mapping = {
        'Con': 'Conservatives',
        'Lab': 'Labour',
        'LD': 'Liberal Democrats',
        'Brexit': 'Reform',
        'Green': 'Greens'
    }
    return party_mapping.get(party_name, 'Other')


# Procedures to insert data into database
def insert_constituencies(df, db_connection):
    """
    Inserts constituencies from the DataFrame into the Constituency table of the DB.
    :param df: DataFrame containing the constituency data.
    :param db_connection: Connection string for the MySQL DB.
    """
    # Extract the 'constituency' column from the DataFrame
    constituencies = df['constituency'].unique()

    # Create a list of tuples, each containing a single constituency name
    constituency_data = [(constituency,) for constituency in constituencies]

    # Create a SQLAlchemy engine for MySQL
    engine = create_engine(db_connection)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Prepare the insert query using SQLAlchemy's text function
    insert_query = text("INSERT INTO constituency (Constituency) VALUES (:constituency)")

    try:
        # Execute the insert query for each tuple in the list
        for data in constituency_data:
            session.execute(insert_query, {'constituency': data})

        # Commit the transaction
        session.commit()

    except Exception as e:
        # Rollback the transaction in case of error
        session.rollback()
        print(f"An error occurred: {e}")

    finally:
        # Close the session
        session.close()


def insert_constituency_results(df, db_connection):
    """
    Inserts constituency results from the DataFrame into the ConstituencyResult table of the DB.
    :param df: DataFrame containing the constituency result data.
    :param db_connection: Connection string for the MySQL DB.
    """
    # Create a SQLAlchemy engine for MySQL
    engine = create_engine(db_connection)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Get the ElectionID for the 2019 election
    election_id = get_id_from_table(session, 'election', 'Year', 2019)

    try:
        for index, row in df.iterrows():
            constituency_id = get_id_from_table(session, 'constituency', 'Constituency', row['constituency'])
            first_party_id = get_id_from_table(session, 'party', 'Party', map_abbreviated_to_full(row['first_party']))
            second_party_id = get_id_from_table(session, 'party', 'Party', map_abbreviated_to_full(row['second_party']))

            # Convert majority percentage to remove percentage sign and remove commas from majority
            majority = row['majority'].replace(',', '')
            majority_percentage = row['majority_percentage'].replace('%','')

            # Convert NewMP to boolean
            new_mp = True if row['new_mp'].lower() == 'yes' else False

            # Insert the row into the constituencyresult table
            insert_query = text("""
                INSERT INTO constituencyresult (ElectionID, ConstituencyID, FirstPartyID, SecondPartyID, Majority, MajorityPercentage, WinningCandidate, NewMP)
                VALUES (:election_id, :constituency_id, :first_party_id, :second_party_id, :majority, :majority_percentage, :winning_candidate, :new_mp)
            """)
            session.execute(insert_query, {
                'election_id': election_id,
                'constituency_id': constituency_id,
                'first_party_id': first_party_id,
                'second_party_id': second_party_id,
                'majority': majority,
                'majority_percentage': majority_percentage,
                'winning_candidate': row['winning_candidate'],
                'new_mp': new_mp
            })

        # Commit the transaction
        session.commit()

    except Exception as e:
        # Rollback the transaction in case of error
        session.rollback()
        print(f"An error occured: {e}")

    finally:
        # Close the session
        session.close()


# Main code
df_2019 = process_text_file('2019.txt')
db_connection_string = 'mysql+pymysql://root:SamSpence@127.0.0.1:3306/election_simulator'
insert_constituencies(df_2019, db_connection_string)
insert_constituency_results(df_2019, db_connection_string)

