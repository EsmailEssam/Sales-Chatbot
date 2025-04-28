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
    def __init__(self, dataset_path=None):
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

    def run(self, messages, session_id ):
        """
        Process the chat messages and return the current event from the model.
        Args:
            messages (list): List of (role, content) tuples representing the chat history.
            session_id (str or int): Unique session identifier.
        Returns:
            dict: The current event from the model's response stream.
        """
        config = {"configurable": {"thread_id": session_id}}
        events = get_graph().invoke(
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

        # currant_event = None
        # for event in events:
        #     currant_event = event

        return events
    
    def get_available_concerns(self):
        return self.available_concerns

    def get_available_categories(self):
        return self.available_categories
    
    def get_available_ingredients(self):
        return self.available_ingredients


if __name__ == "__main__":
    app = App()
    # Example usage with a single message
    messages = [("user", "hi")]
    res =  app.run(messages=messages, session_id=1)

    print(res['output_formatter_response'])
    print("--------------------------------")
    # print(res)

# print(events.get_graph().draw_mermaid())
