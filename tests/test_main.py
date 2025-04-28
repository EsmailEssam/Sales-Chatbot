import unittest
from unittest.mock import patch, MagicMock
from main import App

class TestAppMain(unittest.TestCase):
    """
    Unit tests for the App class in main.py.
    """

    @patch('main.get_graph')
    @patch('main.DfManager')
    def test_output_formatter_response_format(self, mock_df_manager, mock_get_graph):
        """
        Test that the output_formatter_response has the required format.
        """
        # Mock DfManager methods
        mock_df_manager.return_value.get_concerns_set.return_value = ['dry skin']
        mock_df_manager.return_value.get_category_set.return_value = ['serum']
        mock_df_manager.return_value.get_ingredients_set.return_value = ['hyaluronic acid']

        # Mock the event returned by the graph invoke
        expected_response = {
            "response": {
                "text": "For dry skin, I recommend our Hydrating Face Serum. It contains hyaluronic acid...",
                "suggestions": [
                    {
                        "product_id": "12345",
                        "caption": "Matches your dry skin concern and avoids fragrance."
                    }
                ],
                "session_id": "session-abc123"
            },
            "messages": [("user", "I have dry skin")],
            "output_formatter_response": {
                "response": {
                    "text": "For dry skin, I recommend our Hydrating Face Serum. It contains hyaluronic acid...",
                    "suggestions": [
                        {
                            "product_id": "12345",
                            "caption": "Matches your dry skin concern and avoids fragrance."
                        }
                    ],
                    "session_id": "session-abc123"
                }
            }
        }
        mock_get_graph.return_value.invoke.return_value = expected_response

        app = App(dataset_path='dummy_path.json')
        messages = [("user", "I have dry skin")]
        session_id = "session-abc123"
        res = app.run(messages, session_id)

        # Check output_formatter_response format
        self.assertIn('output_formatter_response', res)
        response = res['output_formatter_response']
        self.assertIn('response', response)
        self.assertIn('text', response['response'])
        self.assertIn('suggestions', response['response'])
        self.assertIn('session_id', response['response'])
        self.assertEqual(response['response']['session_id'], session_id)
        self.assertIsInstance(response['response']['suggestions'], list)
        self.assertGreater(len(response['response']['suggestions']), 0)
        self.assertIn('product_id', response['response']['suggestions'][0])
        self.assertIn('caption', response['response']['suggestions'][0])

if __name__ == '__main__':
    unittest.main() 