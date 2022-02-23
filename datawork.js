// Online Archive

// number of matches
db.order.countDocuments({ "properties.Timestamp": { $lte: new Date(ISODate().getTime() - 1000 * 3600 * 24 * 3)}})
10527

db.order.findOne({ "properties.Timestamp": { $lte: new Date(ISODate().getTime() - 1000 * 3600 * 24 * 3)}}).sort({ "properties.Timestamp": 1 })

db.order.find({ "properties.Timestamp": { $lte: new Date(ISODate().getTime() - 1000 * 3600 * 24 * 3)}}).sort({ "properties.Timestamp": 1 })

db.order.createIndex({ "properties.Timestamp": 1 })
'properties.Timestamp_1'

// set date dataype for Timestamp

db.order.updateMany(
    {},
    [{ "$set": { "properties.Timestamp": { "$toDate": "$properties.Timestamp" } } }]
);
{ acknowledged: true,
  insertedId: null,
  matchedCount: 265057,
  modifiedCount: 265057,
  upsertedCount: 0 }



