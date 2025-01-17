import csv
import difflib

# Filenames
CANVAS_FORMAT = "canvas_format.csv"
CODE_FILE = "sampled_codes.csv"
RESULT = "results.csv"
OUTPUT_FILE = "merged.csv"


mapping = {}
with open(CODE_FILE, mode="r", newline="", encoding="utf-8") as f2:
    reader = csv.reader(f2)
    next(reader)  # Skip the single header row in second.csv
    for row in reader:
        if not row:
            continue
        name = row[0]
        code = row[1]
        name = name.replace(',', '').replace(' ', '').upper()
        mapping[code] = name

# Step 1: Read second.csv into a dictionary: { name -> score }
scores = {}
with open(RESULT, mode="r", newline="", encoding="utf-8") as f2:
    reader = csv.reader(f2)
    next(reader)  # Skip the single header row in second.csv
    for row in reader:
        if not row:
            continue
        # name is column 5 (index 1), score is column 5 (index 4)
        score = row[3]
        code = row[4]
        name = row[5].replace(',', '').replace(' ', '').upper()

        if code in mapping:
            ratio = difflib.SequenceMatcher(None, name, mapping[code]).ratio()
            if ratio > 0.85:
                scores[mapping[code]] = score
            elif ratio > 0.35:
                print(mapping[code] + "'s score was added but needs to be confirmed manually.")
                scores[mapping[code]] = score
            else:
                print(code + " exists but can't confirm the name")
        else:
            print(name + " has an invalid code")

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
    print("\n\nFollowing names not found:")
    for row in reader:
        # column 5 in first.csv is index 4 (the name)
        name = row[0] if len(row) > 4 else ""
        full_name = name
        name = name.replace(',', '').replace(' ', '').upper()
        if name in scores:
            score = scores[name]
            count += 1
        else:
            print(full_name)
            score = ""
        # Append score to the row (making it the 13th column)
        row[12] = score
        writer.writerow(row)
    print(f"\n\nTotal students graded {count}. Merged file saved as: {OUTPUT_FILE}")