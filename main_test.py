from modules.helper.get_the_data_from_the_end_point import ProductDataFetcher
from modules.df_manager.df_manager_helpers.convert_json_to_df import ConvertJsonToDf   
from modules.df_manager.df_manager import DfManager

# fetcher = ProductDataFetcher()
# fetcher.run()

# converter = ConvertJsonToDf(r"D:\Electro Pi\Sales-Chatbot\Dataset\products.json")
# df = converter.run()

# print(df.head()) 

df_manager = DfManager(r"D:\Electro Pi\Sales-Chatbot\Dataset\products.json")
cleaned_df = df_manager.get_cleaned_df()
print(cleaned_df.head())

print(df_manager.get_category_set())
print(df_manager.get_concerns_set())
print(df_manager.get_ingredients_set())

