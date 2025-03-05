# local imports
from modules.graph import get_graph

graph = get_graph()
# print(graph.get_graph().draw_mermaid())

def get_answer(user_input):

    config = {"configurable": {"thread_id": "1"}}
    events = graph.stream(
        {'messages' : [('user' , user_input)] },
        config ,
        stream_mode= 'values' ,    
    )
    
    for event in events:
        event['messages'][-1].pretty_print()
        
    return event



if __name__ == "__main__":
    print("Hello, World!")
    user_input = "ايه ارخص كتاب عندك؟"
    event = get_answer(user_input)

    print('*' *50)
    print(event['messages'][-1].content)
    print('*' *50)





