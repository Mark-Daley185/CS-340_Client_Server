from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse


class AnimalShelter(object):
    
    updatedRecords = 0
    deletedRecords = 0
    matchedRecords = 0

    def __init__(self, _password, _username = 'aacuser'):
        
        username = urllib.parse.quote_plus(_username)
        password = urllib.parse.quote_plus(_password)
        
        self.client = MongoClient('mongodb://%s:%s@localhost:41439/?authSource=AAC' % (username, password))
        self.dataBase = self.client['AAC']
       
    #Create a record
    def createRecord(self, data):
        if data:
            validData = self.dataBase.animals.insert_one(data)
            #check the status of the inserted value 
            return True if validData.acknowledged else False
	
        else:
            raise Exception("No data to save.")
    
    #Read a record
    def getId(self, postId):
        data = self.dataBase.find_one({'_id': ObjectId(postId)})
                                  
        return data
    
    #Read a record
    def getRecord(self, criteria = 'None'):
        if criteria:
            data = self.dataBase.animals.find(criteria, {'_id' : 0})
                                 
        else:
            data = self.dataBase.animals.find({},{'_id' : 0})
                                  
        return data
    
    #Update a record
    def updateRecord(self, query, newValue):
        if not query:
            raise Exception("Query doesn't exist.")
        elif not newValue:
            raise Exception("Value already exists.")
        else:
            updateData = self.dataBase.animals.update_many(query, {"$set": newValue})
            self.updatedRecords = updateData.modified_count
            self.matchedRecords = updateData.matched_count

            return True if updatedData.modified_count > 0 else False
    
    #Delete a record
    def deleteRecord(self, query):
        if not query:
            raise Exception("Doesn't exist.")
        
        else:
            deleteData = self.dataBase.animals.delete_many(query)
            self.records_deleted = deleteData.deleted_count

            return True if deleteData.deleted_count > 0 else False   