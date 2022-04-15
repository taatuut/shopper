package com.mongodb.hoppers;

//import static com.mongodb.client.model.Filters.eq;

import org.bson.Document;
import org.bson.conversions.Bson;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import com.mongodb.client.model.geojson.Point;
import com.mongodb.client.model.geojson.Position;
import static com.mongodb.client.model.Filters.near;


public class App 
{
    public static void main( String[] args ) {

        String uri =  System.getenv("atlas_uri");
        Point centerPoint = new Point(new Position(100,1));
        Bson query = near("geometry", centerPoint, 100000.0, 0.0);

        try (MongoClient mongoClient = MongoClients.create(uri)) {
            MongoDatabase database = mongoClient.getDatabase("test");
            MongoCollection<Document> collection = database.getCollection("geom");
            //for (int i = 0; i < 5; i++) {
            while (true) {
                    Document doc = collection.find(query).first();
                    System.out.println(doc.toJson());
                    Thread.sleep(5 * 1000);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}    
