import pdfplumber
import pandas as pd
next_row = [""] * 4
# Function to split sublists into 7 elements
def sublist_split(list_of_lists):
    """
    This function divides the final element of each list into 4 separate elements in order to
    correctly fill the 7 columns.
    :param list_of_lists: List of lists containing 4 elements from the source table.
    :return: New list of lists containing 7 elements.
    """
    new_list_of_lists = []
    for sublist in list_of_lists:
        # Extract the first 3 elements as they are
        first_three_elements = sublist[:3]
        # Split the last element into 4 parts
        fourth_element_parts = sublist[3].split()
        # Combine first three elements with the split parts
        new_sublist = first_three_elements + fourth_element_parts
        # Append the modified sublist to the new list of lists
        new_list_of_lists.append(new_sublist)
    return new_list_of_lists

# Function to clean and combine tables into a single DataFrame
def extract_clean_tables(pdf_path, start_page, end_page):
    """
    This function extracts the desired data from the specified pages, ignoring headers and
    cleaning lines from newline issues by using the relevant functions.
    :param pdf_path: The filepath to the desired pdf.
    :param start_page: Int of first page.
    :param end_page: Int of last page.
    :return: The clean list of lists.
    """
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        for page_num in range(start_page - 1, end_page):    # Adjusting for 0-based index
            page = pdf.pages[page_num]
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Remove headers and clean newline issues
                    if not is_header(row):
                        clean_row = handle_newlines(row)
                        all_tables.append(clean_row)
        return all_tables

# Function to determine if a row is a header
def is_header(row):
    # Check for known keywords in headers
    header_keywords = ['Constituency Results: Winning Candidates and Majorities', 'Constituency Parties Majority Name of winning New\n1st 2nd Votes % candidate MP?']
    return any(keyword in row for keyword in header_keywords)

# Function to handle newline issues
def handle_newlines(row):
    global next_row
    if next_row is None:
        next_row = [""] * 4

    result = [""] * 4  # Initialize result list for the current row

    for i in range(4):
        if row[i] is not None and '\n' in row[i]:
            before_newline, after_newline = row[i].split('\n', 1)
            result[i] = before_newline

            # Find the next available null position in next_row
            for j in range(4):
                if next_row[j] == "":
                    next_row[j] = after_newline
                    break
        elif row[i] is not None:
            result[i] = row[i]

    # Update the row with next_row for the next call
    row[:] = next_row
    next_row = [""] * 4
    print(result)
    return result


# Main processing function
def process_pdf_data(pdf_path):
    # Extract and clean tables from pages 93 to 103
    raw_tables = extract_clean_tables(pdf_path, 93, 103)
    # Split the fourth element into subfields and replace rows
    processed_data = sublist_split(raw_tables)

    return processed_data

print(process_pdf_data('2019.pdf'))
