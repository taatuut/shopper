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

import java.util.Random;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

public class App {
    public static void main(String[] args) throws Exception {
        Random random = new Random();
        String uri = System.getenv("atlas_uri");
        if (uri == null) {
            System.out.println("No MongoDB (Atlas) uri. Provide environment variable 'atlas_uri'.");
            System.out.println("For example use 'export' or 'set':");
            System.out.println("export atlas_uri=mongodb+srv://user:pass@mycluster.mongodb.net/test");
            System.out.println();
            System.exit(1);
        }
        String dbName = "shopper";
        String clName = "orders";

        Options options = new Options();
        Option requests = new Option("n", "requests", true, "Number of requests");
        requests.setRequired(true);
        options.addOption(requests);
        Option interval = new Option("r", "interval", true, "Request interval (seconds)");
        interval.setRequired(true);
        options.addOption(interval);

        HelpFormatter formatter = new HelpFormatter();
        CommandLineParser parser = new DefaultParser();
        CommandLine cmd;
        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("Shopper Info", options);
            System.exit(1);
            return;
        }
        Integer n = Integer.parseInt(cmd.getOptionValue("requests"));
        Integer r = Integer.parseInt(cmd.getOptionValue("interval"));
        System.out.println("Number of requests is: " + n);
        System.out.println("Request interval is: " + r);

        try (MongoClient mongoClient = MongoClients.create(uri)) {
            MongoDatabase database = mongoClient.getDatabase(dbName);
            MongoCollection<Document> collection = database.getCollection(clName);
            while (true) {
                for (int i = 0; i < n; i++) {
                    Double lon = Double.parseDouble("5.5");
                    Double lat = Double.parseDouble("52");
                    Double up = Double.parseDouble("25");
                    Double low = Double.parseDouble("-25");
                    Double div = Double.parseDouble("100");
                    lon = lon + ((random.nextDouble(up - low) + low) / div);
                    lat = lat + ((random.nextDouble(up - low) + low) / div);
                    Point centerPoint = new Point(new Position(lon, lat));
                    Bson query = near("geometry", centerPoint, 10000.0, 0.0);
                    System.out.println("query" + query.toString());
                    Document fDoc = collection.find(query).first();
                    if (fDoc != null) {
                        System.out.println(fDoc.toJson());
                    } else {
                        System.out.println("No results with search point (" + lon + "," + lat + ")");
                    }
                }
                Thread.sleep(5 * 1000);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
