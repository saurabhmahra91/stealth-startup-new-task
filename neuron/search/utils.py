import csv
from pathlib import Path


def load_fashion_data(csv_path: Path = Path("fashion_catalog.csv")) -> list[dict]:
    data = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Clean and split sizes
            sizes_raw = row.get("available_sizes", "")
            sizes_list = [s.strip().lower() for s in sizes_raw.split(",") if s.strip()]
            row["available_sizes"] = sizes_list

            price_str = row.get("usd_price", "").strip()
            row["usd_price"] = float(price_str) if price_str else None

            data.append(row)
    return data


# Example usage:
if __name__ == "__main__":
    fashion_data = load_fashion_data(Path("fashion_catalog.csv"))
    for item in fashion_data[:3]:
        print(item)
