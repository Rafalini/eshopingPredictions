from dataModels.User import User
from dataModels.Session import Session
from dataModels.Product import Product
import jsonlines

def importUsers():
    correctUsersList = []
    faultyUsersList = []
    with jsonlines.open('../raw/users.jsonl') as usersInput:
        for entry in usersInput.iter():
            user = User(entry['user_id'],
                        entry['name'],
                        entry['city'],
                        entry['street'])
            if (entry['user_id'] == None or
                entry['name'] == None or
                entry['street'] == None):

                faultyUsersList.append(user)
            else:
                correctUsersList.append(user)
    return {'correct': correctUsersList, 'error':faultyUsersList}

def importSessions():
    correctSessionList = []
    faultySessionList = []
    with jsonlines.open('../raw/sessions.jsonl') as usersInput:
        for entry in usersInput.iter():
            session = Session(entry['session_id'],
                              entry['timestamp'],
                              entry['user_id'],
                              entry['product_id'],
                              entry['event_type'],
                              entry['offered_discount'],
                              entry['purchase_id'])
        if (entry['session_id'] == None or
            entry['timestamp']  == None or
            entry['user_id']  == None or
            entry['product_id']  == None or
            entry['event_type']  == None or
            entry['offered_discount']  == None or
            entry['purchase_id'] == None):

            faultySessionList.append(session)
        else:
            correctSessionList.append(session)
            
    return {'correct': correctSessionList, 'error':faultySessionList}

def importProducts():
    correctProductList = []
    faultyProductList = []
    with jsonlines.open('../raw/products.jsonl') as usersInput:
        for entry in usersInput.iter():
            product = Product(entry['product_id'],
                                       entry['product_name'],
                                       entry['category_path'],
                                       entry['price'])
            if(entry['product_id']  == None or
               entry['product_name'] == None or
               entry['category_path'] == None or
               entry['price'] == None):

               faultyProductList.append(product)
            else:
               correctProductList.append(product)
    return {'correct': correctProductList, 'error':faultyProductList}


# response = importUsers()
# response.get('correct')[0].print()
# response = importSessions()
# response.get('correct')[0].print()
# response = importProducts()
# response.get('correct')[0].print()
