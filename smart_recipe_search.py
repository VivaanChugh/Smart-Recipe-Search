import pandas as pd
import difflib
from tabulate import tabulate  # Import tabulate for pretty table output

# Load CSV data
def load_csv(file_path):
    df = pd.read_csv(file_path, usecols=[1, 6, 8, 13, 16, 27, 28])

    # Convert Calories and Price columns to numeric, forcing invalid values to NaN
    df['Calories'] = pd.to_numeric(df['Calories'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Fill NaNs with a large value outside the normal filtering range
    df.fillna({'Calories': -1, 'Price': float('inf')}, inplace=True)
    return df

# Filter by fuzzy matching
def filter_by_fuzzy(df, column1, value, n, min_calories, max_calories, max_price, column2):
    matches = difflib.get_close_matches(value.lower(), df[column1].str.lower(), n=n)
    print(f"Matches found: {matches}")  # Debugging: See which matches are found

    # Perform the fuzzy filtering
    filtered_df = df[df[column1].str.lower().isin(matches)]
    print(f"Rows after fuzzy matching: {len(filtered_df)}")  # Check how many rows are left after fuzzy matching

    # Apply the numeric filters
    filtered_df1 = filtered_df[(filtered_df['Calories'] >= min_calories) & (filtered_df['Calories'] <= max_calories)]
    print(f"Rows after calories filtering: {len(filtered_df1)}")  # Debugging

    filtered_df2 = filtered_df1[(filtered_df1['Price'] <= max_price)]
    print(f"Rows after price filtering: {len(filtered_df2)}")  # Debugging

    return filtered_df2

def main():
    file_path = 'modified_recipes.csv'  # Replace with your CSV file path
    df = load_csv(file_path)

    print("Original DataFrame:")
    print(df.head())  # Display first few rows for debugging

    value = input('What would you like to search for: ')
    n = 100
    min_calories = int(input('Minimum Calories Filter: '))
    max_calories = int(input('Maximum Calories Filter: '))
    max_price = float(input('Maximum Price Filter: '))  # Changed to float for price with decimals

    final_filtered_df = filter_by_fuzzy(df, 'Name', value, n, min_calories, max_calories, max_price, 'RecipeIngredientParts')

    print("\nFiltered DataFrame (Top 10 closest matches):")
    if final_filtered_df.empty:
        print('No matches')
    else:
        # Prepare DataFrame for table display
        df_list = final_filtered_df.head(10).values.tolist()  # Limit to top 10 rows for display
        headers = final_filtered_df.columns.tolist()  # Get the column names for headers

        # Keep string slicing logic
        for i in df_list:
            i[3] = str(i[3])
            i[5] = str(i[5])
        for i in df_list:
            i[3] = i[3][2:-1]  # Slice string for some reason
            i[5] = i[5][2:-1]  # Same here

        # Print the table using tabulate
        print(tabulate(df_list, headers=headers, tablefmt="grid"))  # grid format for better visuals

main()
