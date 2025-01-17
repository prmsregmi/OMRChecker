import pandas as pd
import itertools
import random

# Generate all combinations of length 4 using the letters A, B, C, D, E
codes = [''.join(code) for code in itertools.product('ABCDE', repeat=4)]

# Randomly sample 100 unique codes from the generated list
sampled_codes = random.sample(codes, 100)

# Load the first column from canvas_format.csv
canvas_data = pd.read_csv("canvas_format.csv")
names = canvas_data.iloc[1:, 0].head(100)  # Get the first column and limit to 100 names

# Ensure there are enough names for the sampled codes
if len(names) < 100:
    raise ValueError("Not enough names in canvas_format.csv to match the 100 sampled codes.")

# Create a DataFrame with names and sampled codes
sampled_codes_df = pd.DataFrame({
    "Name": names,
    "Code": sampled_codes
}).sort_values("Name")  # Sort by Name for a cleaner output

# Save the DataFrame to a CSV file
sampled_codes_df.to_csv("sampled_codes.csv", index=False)
