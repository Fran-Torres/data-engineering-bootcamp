import pandas as pd
import openpyxl

# File Location
data = 'D:\\My_files\\Python\\profeco\\all_data.csv'
# Output file location - This may be changed in order to get this file to your own documents
output_location = 'D:\\My_files\\Python\\WizeLineChallenge'

# Chunk the data to make it a little bit faster to run
all_data = pd.read_csv(data, chunksize=10000000, low_memory=False)
frames = []
for chunk in all_data:
    frames.append(chunk)
all_data = pd.concat(frames)
# Filter to not add any value described as 'giro' inside the 'giro' column
not_giro = all_data['giro'] != 'giro'
file = all_data[not_giro]

# QUESTION 1 How many commercial chains are monitored, and therefore, included in this database?

nbr_commercial_chains = file.cadenaComercial.nunique()
name_commercial_chain = file.cadenaComercial.unique()
print(f"{nbr_commercial_chains} are being monitored by Profeco in this database.")

# QUESTION 2 What are the top 10 monitored products by State?

# Copy "producto" into a new column
file['productCount'] = file.producto

# Separate "estados" states
name_state = file.estado.unique()

# Blank list to iterate through the loop
state_list = []

# Loop to get top 10 products by state
for state in name_state:
    state_filter = file[(file.estado == state)]
    top_ten_pivot = state_filter.groupby(['estado','producto'])['productCount'].count().nlargest(10)
    # append each state pivot to the blank list "state_list"
    state_list.append(top_ten_pivot)

# Concatenate function to create final pivot
final_pivot = pd.concat(state_list)
final_pivot.to_excel(f"{output_location}\\output.xlsx", index=True, header=True)
print(final_pivot)


# QUESTION 3 Which is the commercial chain with the highest number of monitored products?

# value_counts() returns a series of unique values
top_chain = file.cadenaComercial.value_counts().nlargest(1)
print(f"{top_chain} has the highest number of products being monitored.")


# QUESTION 4 Use the data to find an interesting fact

# Commercial chain with the lowest number of monitored products.
last_chain = file.cadenaComercial.value_counts().nsmallest(1)
print(f"The commercial chain with the lowest number of products being monitored is {last_chain}.")

# Highest and lowest industries ("giros") monitored in this database.
top_industries = file.giro.value_counts().nlargest(3)
print(f"Here are the top 3 industries being monitored: \n{top_industries}.")
last_industries = file.giro.value_counts().nsmallest(3)
print(f"{last_industries} are the industries with the lower number of products being monitored.")
