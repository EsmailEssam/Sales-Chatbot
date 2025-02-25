from .sales_crew import ai_crew
import os

def books_to_html(books):
  with open(os.path.join(os.getcwd(), 'template', 'offer_card_template.txt'), 'r', encoding='utf-8') as f:
    offer_cand_template = f.read()
  
  with open(os.path.join(os.getcwd(), 'template', 'norm_card_template.txt'), 'r', encoding='utf-8') as f:
    norm_cand_template = f.read()

  with open(os.path.join(os.getcwd(), 'template', 'cards_template.txt'), 'r', encoding='utf-8') as f:
      all_cand_template = f.read()
  
  all_cards = ''
  for book in books['books']:
    if book['discount_percentage'] > 0:
      new_card_template = offer_cand_template.replace("img_url" , book['Image_URL'])
      new_card_template = new_card_template.replace("book_title" , book['Book_title'])
      new_card_template = new_card_template.replace("book_author" , book['Book_author'])
      new_card_template = new_card_template.replace("discount_percentage" , str(book['discount_percentage']))
      new_card_template = new_card_template.replace("price_befor_diccount" , str(book['price']))
      new_card_template = new_card_template.replace("price_after_discount" , str(book['price_after_discount']))
    else:
      new_card_template = norm_cand_template.replace("img_url" , book['Image_URL'])
      new_card_template = new_card_template.replace("book_title" , book['Book_title'])
      new_card_template = new_card_template.replace("book_author" , book['Book_author'])
      new_card_template = new_card_template.replace("price_after_discount" , str(book['price_after_discount']))
  
    all_cards += new_card_template + '\n'
  
  new_template = all_cand_template.replace('put_your_cards_here', all_cards)
  
  return new_template

def process_query(query):
    result = ai_crew.kickoff(inputs={
      'query': query
    })
    
    return result.to_dict()
  
  
if __name__ == "__main__" :  
  res =  process_query('what is best deal in your web site?')

  print(res)