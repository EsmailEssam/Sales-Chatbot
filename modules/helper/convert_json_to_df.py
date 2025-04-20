import pandas as pd
import json
import os

file_path = os.path.join(os.getcwd(), 'Dataset', 'products.json')


def convert_json_to_df(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data['data']['products'])
    return df


if __name__ == "__main__":
    df = convert_json_to_df(file_path)
    print(df.head())




