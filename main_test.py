from modules import graph
from modules.helper.get_the_data_from_the_end_point import ProductDataFetcher
from modules.df_manager.df_manager_helpers.convert_json_to_df import ConvertJsonToDf   
from modules.df_manager.df_manager import DfManager
from modules.graph import get_graph

# fetcher = ProductDataFetcher()
# fetcher.run()

# converter = ConvertJsonToDf(r"D:\Electro Pi\Sales-Chatbot\Dataset\products.json")
# df = converter.run()

# print(df.head()) 

df_manager = DfManager(r"D:\Electro Pi\Sales-Chatbot\Dataset\products.json")
cleaned_df = df_manager.get_cleaned_df()
# print(cleaned_df.head())

# print(df_manager.get_category_set())
# print(df_manager.get_concerns_set())
# print(df_manager.get_ingredients_set())

available_concerns = df_manager.get_concerns_set()
available_categories = df_manager.get_category_set()
available_ingredients = df_manager.get_ingredients_set()

user_input = "ايه ارخص منتج عندك؟"

config = {"configurable": {"thread_id": "1"}}
events = get_graph().stream(
            {
                'messages': [('user', user_input)],
                'available_concerns': available_concerns, 
                'available_categories': available_categories,
                'available_ingredients': available_ingredients,
             },
            config,
            stream_mode='values',
        )

for event in events:
    print(event)
    print("--------------------------------")
    event['messages'][-1].pretty_print()
    print("--------------------------------")

