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

def main(messages, session_id):
    df_manager = DfManager(r"D:\Electro Pi\Sales-Chatbot\Dataset\products.json")
    cleaned_df = df_manager.get_cleaned_df()
    available_concerns = df_manager.get_concerns_set()
    available_categories = df_manager.get_category_set()
    available_ingredients = df_manager.get_ingredients_set()

    config = {"configurable": {"thread_id": session_id}}
    events = get_graph().stream(
        {
            'messages': messages,  # Now expects a list of (role, content) tuples
            'available_concerns': available_concerns,
            'available_categories': available_categories,
            'available_ingredients': available_ingredients,
            'session_id': session_id
        },
        config,
        stream_mode='values',
    )

    for event in events:
        currant_event = event

    return currant_event


if __name__ == "__main__":

    res = main(user_input= "hi" , session_id= 1)


    print(res['messages'][-2 :])
    print("--------------------------------")
    print(res['output_formatter_response'])

# print(events.get_graph().draw_mermaid())
