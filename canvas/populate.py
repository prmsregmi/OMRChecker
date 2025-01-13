import csv
import difflib

# Filenames
CANVAS_FORMAT = "canvas_format.csv"
RESULT = "results.csv"
OUTPUT_FILE = "merged.csv"

# Step 1: Read second.csv into a dictionary: { name -> score }
scores = {}
with open(RESULT, mode="r", newline="", encoding="utf-8") as f2:
    reader = csv.reader(f2)
    next(reader)  # Skip the single header row in second.csv
    for row in reader:
        if not row:
            continue
        # name is column 5 (index 1), score is column 5 (index 4)
        name = row[4]
        name = name.replace(',', '').replace(' ', '').upper()
        score = row[3] if len(row) > 3 else ""
        scores[name] = score
print(scores)

# Step 2: Read first.csv, write everything to merged.csv, 
#         and for each data row (below the 2 header rows),
#         append the score in a new 13th column.
with open(CANVAS_FORMAT, mode="r", newline="", encoding="utf-8") as f1, \
     open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as out:

    reader = csv.reader(f1)
    writer = csv.writer(out)

    # 2 header rows from first.csv - write as-is
    header1 = next(reader)
    writer.writerow(header1)

    header2 = next(reader)
    writer.writerow(header2)

    # For each subsequent row, append the matching score
    count = 0
    for row in reader:
        # column 5 in first.csv is index 4 (the name)
        name = row[0] if len(row) > 4 else ""
        name = name.replace(',', '').replace(' ', '').upper()

        # Look up score from dictionary, default to empty string if not found
        possible_matches = difflib.get_close_matches(name, scores.keys(), n=1, cutoff=0.7)
        if possible_matches:
            best_match = possible_matches[0]
            score = scores[best_match]
            count += 1
        else:
            print(name)
            score = ""
        # Append score to the row (making it the 13th column)
        row[12] = score
        writer.writerow(row)
    print(count)

print(f"Done! Merged file saved as: {OUTPUT_FILE}")