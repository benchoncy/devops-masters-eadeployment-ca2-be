/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package bp;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.bson.Document;
import java.lang.System;

/**
 *
 * @author kanolan
 */
public class BPPersistence {
    
    public static final String FILTERS = "com.mongodb.client.model.Filters.*";
    public static final String UPDATES = "com.mongodb.client.model.Updates.*";
    
    String databaseUrl = System.getenv("DATABASE_URI");
    String databaseName = System.getenv("DATABASE_NAME");
    String databaseCollection = System.getenv("DATABASE_COLLECTION");
    
    MongoDatabase database;
    
    public void initiliaze() throws Exception {
        try {   
            System.out.println(">> " + databaseUrl); 
            //Create client for connection
            MongoClient mongoClient = MongoClients.create(databaseUrl);
                        
            System.out.println(">> " + databaseName);
            //Connect to DB
            database = (MongoDatabase) mongoClient.getDatabase(databaseName);
            System.out.println("Name: " + database.getName() ); 
            
            MongoCollection<Document> collection = database.getCollection(databaseCollection);
            for (String name : database.listCollectionNames()) {
                System.out.println(name);
            }
        } 
        catch(Exception e) {
            Logger.getLogger(BPPersistence.class.getName()).log(Level.WARNING, null, e.getMessage());
            throw new Exception("Cannot connect to database.");
        }
    }
       
    /**
    public MongoCollection<Document> accessCollecton() throws Exception {
        try {
            //MongoCollection instances are immutable.
            MongoCollection<Document> collection = database.getCollection("customers");
            return collection;
        }
        catch(Exception e) {
            throw new Exception("Cannot retrieve a collection from the db.");
        }        
    }
    
    public FindIterable<Document> accessCollectonByUser(String email) throws Exception {
        FindIterable<Document> findIt = null;
        try {
            MongoCollection<Document> collection = database.getCollection("customers");
            Bson bsonFilter = Filters.eq("email", email);                        
            findIt = collection.find(bsonFilter);
            //collection.find(Filters.eq("email", email)).forEach(printBlock);
        }
        catch(Exception e) {
            e.printStackTrace(); 
            System.out.println(">>> " + e.getMessage());
            throw new Exception("Cannot retrieve collection By User.");
        } 
        return findIt;
    }
    */ 
    public boolean insertDocument(Document doc) throws Exception {
        try {
            MongoCollection<Document> collection = database.getCollection(databaseCollection);
            collection.insertOne(doc);
            return true;
        }
        catch(Exception e) {
            throw new Exception("Cannot insert document into collection in db.");
        }        
    }
    
}
