# Product

Test mgeneratejs template:

`clear;mgeneratejs product_template.json -n 3 | jq`

## Batch load

To ingest a certain amount of products, run the following command in a terminal from the `shopper` folder:

`mgeneratejs product_template.json -n 55555 | mongoimport --uri $mongodb_uri --db=shopper --drop --collection=products`

## Query

```
[{
 $match: {
  product_id: {
   $gte: 112
  }
 }
}, {
 $sort: {
  price: -1
 }
}, {
 $facet: {
  price_buckets: [
   {
    $bucketAuto: {
     groupBy: '$price',
     buckets: 3
    }
   }
  ]
 }
}]
```
