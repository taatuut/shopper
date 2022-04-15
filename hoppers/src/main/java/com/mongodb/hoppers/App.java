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

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

public class App {
    public static void main(String[] args) throws Exception {

        String uri = System.getenv("atlas_uri");
        if (uri == null) {
            System.out.println("No MongoDB (Atlas) uri. Provide environment variable 'atlas_uri'.");
            System.out.println("For example use 'export' or 'set':");
            System.out.println("export atlas_uri=mongodb+srv://user:pass@mycluster.mongodb.net/test");
            System.out.println();
            System.exit(1);
        }
        String dbName = "test";
        String clName = "geom";

        Options options = new Options();
        Option requests = new Option("n", "requests", true, "Number of requests");
        requests.setRequired(true);
        options.addOption(requests);
        Option interval = new Option("r", "interval", true, "Request interval (seconds)");
        interval.setRequired(true);
        options.addOption(interval);
        Option searchPoint = new Option("s", "searchpoint", true, "Search point (x,y)");
        searchPoint.setRequired(false);
        options.addOption(searchPoint);

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
        Double x = Double.parseDouble("100");
        Double y = Double.parseDouble("1");
        if (cmd.hasOption("s")) {
            String s = cmd.getOptionValue("searchpoint");
            String[] arrS = s.split(",", 2);
            x = Double.parseDouble(arrS[0]);
            y = Double.parseDouble(arrS[1]);
            System.out.println("Search point (x,y) is: (" + x + "," + y + ")");
        }

        Point centerPoint = new Point(new Position(x, y));
        Bson query = near("geometry", centerPoint, 1000000.0, 0.0);

        try (MongoClient mongoClient = MongoClients.create(uri)) {
            MongoDatabase database = mongoClient.getDatabase(dbName);
            MongoCollection<Document> collection = database.getCollection(clName);
            while (true) {
                for (int i = 0; i < n; i++) {
                    Document doc = collection.find(query).first();
                    if (doc != null) {
                        System.out.println(doc.toJson());
                    } else {
                        System.out.println("No results with search point (" + x + "," + y + ")");
                    }
                }
                Thread.sleep(5 * 1000);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
