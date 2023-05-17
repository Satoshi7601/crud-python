from flask import Flask

import pymongo

app =Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        
        host='localhost',
        port=27017,
        serverSelectionTimeoutMS = 1000 
        
    )
    print('Conectado')
    db = mongo.company
    mongo.server_info()
    
    
except :
    print("Erro canot connect db")


    app.route('/users', methods =['POST'])
      
def create_user():
    try:
        user ={'Name':'AA','LastName':'EE'}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
          
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    app.run(port='81', debug= True)
    
