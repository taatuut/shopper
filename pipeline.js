
optional: add search

add geospatial search

copy to new aggregation flow

[{$unwind: {
    path: '$properties.Order.Products'
   }}, {$group: {
    _id: '$properties.Order.Products.id',
    name: {
     $first: '$properties.Order.Products.name'
    },
    count: {
     $sum: '$properties.Order.Products.quantity'
    },
    price: {
     $first: '$properties.Order.Products.price'
    }
   }}, {$project: {
    name: '$name',
    amount: {
     $round: [
      {
       $multiply: [
        {
         $toDecimal: '$count'
        },
        {
         $toDecimal: '$price'
        }
       ]
      },
      2
     ]
    }
   }}]


   {geometry: {$geoWithin: { $geometry: { type: 'Polygon', coordinates: [ [ [ 4.6688651741812635, 52.501405416801134 ], [ 4.593502668153056, 52.24435328111528 ], [ 5.149872017203485, 52.208240518778744 ], [ 5.083297241975081, 52.49811912018655 ], [ 4.6688651741812635, 52.501405416801134 ] ] ] }}}}


   Save as view and display as table