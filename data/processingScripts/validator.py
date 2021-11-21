import dataImport

users = dataImport.importUsers()
sessions = dataImport.importSessions()
products = dataImport.importProducts()

if(len(users.get('error')) != 0):
    print('Users has some faulty records')

if(len(sessions.get('error')) != 0):
    print('Sessions has some faulty records')

if(len(products.get('error')) != 0):
    print('Products has some faulty records')


