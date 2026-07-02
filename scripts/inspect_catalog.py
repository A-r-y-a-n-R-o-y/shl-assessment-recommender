import json
from pprint import pprint

# Load the catalog
with open("data/catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 60)
print("TYPE:", type(data))
print("=" * 60)

if isinstance(data, list):
    print(f"Total assessments: {len(data)}")

    print("\nFirst assessment:\n")
    pprint(data[0])

    print("\n" + "=" * 60)

    print("\nLast assessment:\n")
    pprint(data[-1])

elif isinstance(data, dict):
    print("Top-level keys:")
    pprint(data.keys())

    # If assessments are inside another key
    for key, value in data.items():
        if isinstance(value, list):
            print(f"\nFound list under key: '{key}'")
            print(f"Length: {len(value)}")

            if len(value) > 0:
                print("\nFirst item:")
                pprint(value[0])
            break