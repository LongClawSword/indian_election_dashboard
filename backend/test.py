import pandas as pd

# Load the CSV
df = pd.read_csv("backend/election_data.csv")

# Define the general election years you want to keep
general_election_years = [1951, 1957, 1962, 1967, 1971, 1977, 1980, 1984, 1989,
                          1991, 1996, 1998, 1999, 2004, 2009, 2014, 2019]

# Filter the dataframe
df_filtered = df[df['year'].isin(general_election_years)]

# Save the updated CSV
df_filtered.to_csv("backend/election_data1.csv", index=False)
