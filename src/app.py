import pandas as pd
from validator import validate_vehicle  # if you separated logic
# if all logic is in app.py only, just call the functions directly

def main():
    # Load dataset
    validation_data = pd.read_csv("../data/validation_dataset.csv")

    print("🔍 Running validation checks...\n")

    # Loop through test data
    for _, row in validation_data.iterrows():
        result = validate_vehicle(
            plate=row["user_input_plate"],
            brand=row["user_input_brand"],
            model=row["user_input_model"],
            year=row["user_input_year"],
        )
        print(result)

if __name__ == "__main__":
    main()
