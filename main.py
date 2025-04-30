from src import graph
from src.helper.get_the_data_from_the_end_point import ProductDataFetcher
from src.df_manager.df_manager_helpers.convert_json_to_df import ConvertJsonToDf   
from src.df_manager.df_manager import DfManager
from src.graph import get_graph
import os

class App:
    """
    Sales Chatbot Application class for managing product data and generating responses.
    """
    def __init__(self, dataset_path: str = None):
        """
        Initialize the App with the path to the products dataset.
        """
        if dataset_path is None:
            dataset_path = os.path.join("Dataset", "products.json")
        self.dataset_path = dataset_path
        self.df_manager = DfManager(self.dataset_path)
        self.available_concerns = self.df_manager.get_concerns_set()
        self.available_categories = self.df_manager.get_category_set()
        self.available_ingredients = self.df_manager.get_ingredients_set()
        
        # Create and store the graph instance once (singleton pattern)
        self.graph = get_graph()

    def run(self, messages, session_id):
        """
        Process the chat messages and return the current event from the model.
        """
        config = {"configurable": {"thread_id": session_id}}
        events = self.graph.invoke(
            {
                'messages': messages,
                'available_concerns': self.available_concerns,
                'available_categories': self.available_categories,
                'available_ingredients': self.available_ingredients,
                'session_id': session_id
            },
            config,
            stream_mode='values',
        )

        return events
    

if __name__ == "__main__":
    app = App()
    # Example usage with a single message
    messages = [("user", "عاوز حاجه لتساقط الشعر")]
    res =  app.run(messages=messages, session_id=1)

    print(res['output_formatter_response'])
    print("--------------------------------")
    # print(res)

# print(events.get_graph().draw_mermaid())
