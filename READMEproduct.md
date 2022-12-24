# Product

Test mgeneratejs template:

`clear;mgeneratejs product_template.json -n 3 | jq`

# Batch load

To ingest a certain amount of products, run the following command in a terminal from the `shopper` folder:

`mgeneratejs product_template.json -n 55555 | mongoimport --uri $mongodb_uri --db=shopper --drop --collection=products`

# Indexes

## Primary

`_id_`

## Secondary

`price_-1`

# Query

Run `aggregate` with `explain` e.g. in `mongosh` in **MongoDB Compass**.

Format is `db.products.explain().aggregate`

## On M10 (Production like)

```
db.products.aggregate([{
 $match: { "$and":[
  {product_id: {$gte: 112}},
  {brand: "Albert Heijn"}
  ]
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
}])
{ price_buckets: 
   [ { _id: { min: Decimal128("1"), max: Decimal128("7.35") },
       count: 4219 },
     { _id: { min: Decimal128("7.35"), max: Decimal128("13.68") },
       count: 4215 },
     { _id: { min: Decimal128("13.68"), max: Decimal128("20") },
       count: 4212 } ] }
```

```
db.products.explain("executionStats").aggregate([{
 $match: { "$and":[
  {product_id: {$gte: 112}},
  {brand: "Albert Heijn"}
  ]
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
}])
{ explainVersion: '1',
  stages: 
   [ { '$cursor': 
        { queryPlanner: 
           { namespace: 'shopper.products',
             indexFilterSet: false,
             parsedQuery: 
              { '$and': 
                 [ { brand: { '$eq': 'Albert Heijn' } },
                   { product_id: { '$gte': 112 } } ] },
             queryHash: 'D969656A',
             planCacheKey: '29F42290',
             maxIndexedOrSolutionsReached: false,
             maxIndexedAndSolutionsReached: false,
             maxScansToExplodeReached: false,
             winningPlan: 
              { stage: 'PROJECTION_SIMPLE',
                transformBy: { price: 1, _id: 0 },
                inputStage: 
                 { stage: 'FETCH',
                   filter: 
                    { '$and': 
                       [ { brand: { '$eq': 'Albert Heijn' } },
                         { product_id: { '$gte': 112 } } ] },
                   inputStage: 
                    { stage: 'IXSCAN',
                      keyPattern: { price: -1 },
                      indexName: 'price_-1',
                      isMultiKey: false,
                      multiKeyPaths: { price: [] },
                      isUnique: false,
                      isSparse: false,
                      isPartial: false,
                      indexVersion: 2,
                      direction: 'forward',
                      indexBounds: { price: [ '[MaxKey, MinKey]' ] } } } },
             rejectedPlans: 
              [ { stage: 'SORT',
                  sortPattern: { price: -1 },
                  memLimit: 104857600,
                  type: 'simple',
                  inputStage: 
                   { stage: 'PROJECTION_SIMPLE',
                     transformBy: { price: 1, _id: 0 },
                     inputStage: 
                      { stage: 'FETCH',
                        filter: { product_id: { '$gte': 112 } },
                        inputStage: 
                         { stage: 'IXSCAN',
                           keyPattern: { brand: 1 },
                           indexName: 'brand_1',
                           isMultiKey: false,
                           multiKeyPaths: { brand: [] },
                           isUnique: false,
                           isSparse: false,
                           isPartial: false,
                           indexVersion: 2,
                           direction: 'forward',
                           indexBounds: { brand: [ '["Albert Heijn", "Albert Heijn"]' ] } } } } } ] },
          executionStats: 
           { executionSuccess: true,
             nReturned: 12646,
             executionTimeMillis: 156,
             totalKeysExamined: 55555,
             totalDocsExamined: 55555,
             executionStages: 
              { stage: 'PROJECTION_SIMPLE',
                nReturned: 12646,
                executionTimeMillisEstimate: 8,
                works: 55556,
                advanced: 12646,
                needTime: 42909,
                needYield: 0,
                saveState: 57,
                restoreState: 57,
                isEOF: 1,
                transformBy: { price: 1, _id: 0 },
                inputStage: 
                 { stage: 'FETCH',
                   filter: 
                    { '$and': 
                       [ { brand: { '$eq': 'Albert Heijn' } },
                         { product_id: { '$gte': 112 } } ] },
                   nReturned: 12646,
                   executionTimeMillisEstimate: 6,
                   works: 55556,
                   advanced: 12646,
                   needTime: 42909,
                   needYield: 0,
                   saveState: 57,
                   restoreState: 57,
                   isEOF: 1,
                   docsExamined: 55555,
                   alreadyHasObj: 0,
                   inputStage: 
                    { stage: 'IXSCAN',
                      nReturned: 55555,
                      executionTimeMillisEstimate: 4,
                      works: 55556,
                      advanced: 55555,
                      needTime: 0,
                      needYield: 0,
                      saveState: 57,
                      restoreState: 57,
                      isEOF: 1,
                      keyPattern: { price: -1 },
                      indexName: 'price_-1',
                      isMultiKey: false,
                      multiKeyPaths: { price: [] },
                      isUnique: false,
                      isSparse: false,
                      isPartial: false,
                      indexVersion: 2,
                      direction: 'forward',
                      indexBounds: { price: [ '[MaxKey, MinKey]' ] },
                      keysExamined: 55555,
                      seeks: 1,
                      dupsTested: 0,
                      dupsDropped: 0 } } } } },
       nReturned: 12646,
       executionTimeMillisEstimate: 138 },
     { '$facet': 
        { price_buckets: 
           [ { '$internalFacetTeeConsumer': {},
               nReturned: 12646,
               executionTimeMillisEstimate: 138 },
             { '$bucketAuto': 
                { groupBy: '$price',
                  buckets: 3,
                  output: { count: { '$sum': { '$const': 1 } } } },
               nReturned: 3,
               executionTimeMillisEstimate: 144 } ] },
       nReturned: 1,
       executionTimeMillisEstimate: 144 } ],
  serverInfo: 
   { host: 'atlas-rae0qu-shard-00-01.mz3yq.mongodb.net',
     port: 27017,
     version: '6.0.3',
     gitVersion: 'f803681c3ae19817d31958965850193de067c516' },
  serverParameters: 
   { internalQueryFacetBufferSizeBytes: 104857600,
     internalQueryFacetMaxOutputDocSizeBytes: 104857600,
     internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
     internalDocumentSourceGroupMaxMemoryBytes: 104857600,
     internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
     internalQueryProhibitBlockingMergeOnMongoS: 0,
     internalQueryMaxAddToSetBytes: 104857600,
     internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600 },
  command: 
   { aggregate: 'products',
     pipeline: 
      [ { '$match': { '$and': [ { product_id: { '$gte': 112 } }, { brand: 'Albert Heijn' } ] } },
        { '$sort': { price: -1 } },
        { '$facet': { price_buckets: [ { '$bucketAuto': { groupBy: '$price', buckets: 3 } } ] } } ],
     cursor: {},
     '$db': 'shopper' },
  ok: 1,
  '$clusterTime': 
   { clusterTime: Timestamp({ t: 1671801291, i: 1 }),
     signature: 
      { hash: Binary(Buffer.from("b28afe4cccb8cfd5966e7873023e416235f64628", "hex"), 0),
        keyId: 7180326067754762000 } },
  operationTime: Timestamp({ t: 1671801291, i: 1 }) }
```

## On M0

```
db.products.explain().aggregate([{
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
}])
{ explainVersion: '1',
  stages: 
   [ { '$cursor': 
        { queryPlanner: 
           { namespace: '621434f943d3e75ba8bce014_shopper.products',
             indexFilterSet: false,
             parsedQuery: { product_id: { '$gte': 112 } },
             queryHash: '60E474BD',
             planCacheKey: '393D1823',
             maxIndexedOrSolutionsReached: false,
             maxIndexedAndSolutionsReached: false,
             maxScansToExplodeReached: false,
             winningPlan: 
              { stage: 'SORT',
                sortPattern: { price: -1 },
                memLimit: 33554432,
                type: 'simple',
                inputStage: 
                 { stage: 'PROJECTION_SIMPLE',
                   transformBy: { price: 1, _id: 0 },
                   inputStage: 
                    { stage: 'COLLSCAN',
                      filter: { product_id: { '$gte': 112 } },
                      direction: 'forward' } } },
             rejectedPlans: [] } } },
     { '$facet': 
        { price_buckets: 
           [ { '$teeConsumer': {} },
             { '$bucketAuto': 
                { groupBy: '$price',
                  buckets: 3,
                  output: { count: { '$sum': { '$const': 1 } } } } } ] } } ],
  serverInfo: 
   { host: 'ez-free-cluster-shard-00-02.mz3yq.mongodb.net',
     port: 27017,
     version: '5.0.14',
     gitVersion: '1b3b0073a0b436a8a502b612f24fb2bd572772e5' },
  serverParameters: 
   { internalQueryFacetBufferSizeBytes: 104857600,
     internalQueryFacetMaxOutputDocSizeBytes: 104857600,
     internalLookupStageIntermediateDocumentMaxSizeBytes: 16793600,
     internalDocumentSourceGroupMaxMemoryBytes: 104857600,
     internalQueryMaxBlockingSortMemoryUsageBytes: 33554432,
     internalQueryProhibitBlockingMergeOnMongoS: 0,
     internalQueryMaxAddToSetBytes: 104857600,
     internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600 },
  command: 
   { aggregate: 'products',
     pipeline: 
      [ { '$match': { product_id: { '$gte': 112 } } },
        { '$sort': { price: -1 } },
        { '$facet': { price_buckets: [ { '$bucketAuto': { groupBy: '$price', buckets: 3 } } ] } } ],
     cursor: {},
     '$db': 'shopper' },
  ok: 1,
  '$clusterTime': 
   { clusterTime: Timestamp({ t: 1671798036, i: 58 }),
     signature: 
      { hash: Binary(Buffer.from("5ede9e175aed85d9e0624784ed6346b20186c4e2", "hex"), 0),
        keyId: 7148513146209042000 } },
  operationTime: Timestamp({ t: 1671798036, i: 58 }) }
```

```
db.products.explain("executionStats").aggregate([{
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
}])
{ explainVersion: '1',
  stages: 
   [ { '$cursor': 
        { queryPlanner: 
           { namespace: '621434f943d3e75ba8bce014_shopper.products',
             indexFilterSet: false,
             parsedQuery: { product_id: { '$gte': 112 } },
             queryHash: '60E474BD',
             planCacheKey: '393D1823',
             maxIndexedOrSolutionsReached: false,
             maxIndexedAndSolutionsReached: false,
             maxScansToExplodeReached: false,
             winningPlan: 
              { stage: 'SORT',
                sortPattern: { price: -1 },
                memLimit: 33554432,
                type: 'simple',
                inputStage: 
                 { stage: 'PROJECTION_SIMPLE',
                   transformBy: { price: 1, _id: 0 },
                   inputStage: 
                    { stage: 'COLLSCAN',
                      filter: { product_id: { '$gte': 112 } },
                      direction: 'forward' } } },
             rejectedPlans: [] },
          executionStats: 
           { executionSuccess: true,
             nReturned: 55443,
             executionTimeMillis: 415,
             totalKeysExamined: 0,
             totalDocsExamined: 55555,
             executionStages: 
              { stage: 'SORT',
                nReturned: 55443,
                executionTimeMillisEstimate: 199,
                works: 111001,
                advanced: 55443,
                needTime: 55557,
                needYield: 0,
                saveState: 113,
                restoreState: 113,
                isEOF: 1,
                sortPattern: { price: -1 },
                memLimit: 33554432,
                type: 'simple',
                totalDataSizeSorted: 5100756,
                usedDisk: false,
                inputStage: 
                 { stage: 'PROJECTION_SIMPLE',
                   nReturned: 55443,
                   executionTimeMillisEstimate: 63,
                   works: 55557,
                   advanced: 55443,
                   needTime: 113,
                   needYield: 0,
                   saveState: 113,
                   restoreState: 113,
                   isEOF: 1,
                   transformBy: { price: 1, _id: 0 },
                   inputStage: 
                    { stage: 'COLLSCAN',
                      filter: { product_id: { '$gte': 112 } },
                      nReturned: 55443,
                      executionTimeMillisEstimate: 43,
                      works: 55557,
                      advanced: 55443,
                      needTime: 113,
                      needYield: 0,
                      saveState: 113,
                      restoreState: 113,
                      isEOF: 1,
                      direction: 'forward',
                      docsExamined: 55555 } } } } },
       nReturned: 55443,
       executionTimeMillisEstimate: 238 },
     { '$facet': 
        { price_buckets: 
           [ { '$teeConsumer': {},
               nReturned: 55443,
               executionTimeMillisEstimate: 261 },
             { '$bucketAuto': 
                { groupBy: '$price',
                  buckets: 3,
                  output: { count: { '$sum': { '$const': 1 } } } },
               nReturned: 3,
               executionTimeMillisEstimate: 416 } ] },
       nReturned: 1,
       executionTimeMillisEstimate: 416 } ],
  serverInfo: 
   { host: 'ez-free-cluster-shard-00-02.mz3yq.mongodb.net',
     port: 27017,
     version: '5.0.14',
     gitVersion: '1b3b0073a0b436a8a502b612f24fb2bd572772e5' },
  serverParameters: 
   { internalQueryFacetBufferSizeBytes: 104857600,
     internalQueryFacetMaxOutputDocSizeBytes: 104857600,
     internalLookupStageIntermediateDocumentMaxSizeBytes: 16793600,
     internalDocumentSourceGroupMaxMemoryBytes: 104857600,
     internalQueryMaxBlockingSortMemoryUsageBytes: 33554432,
     internalQueryProhibitBlockingMergeOnMongoS: 0,
     internalQueryMaxAddToSetBytes: 104857600,
     internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600 },
  command: 
   { aggregate: 'products',
     pipeline: 
      [ { '$match': { product_id: { '$gte': 112 } } },
        { '$sort': { price: -1 } },
        { '$facet': { price_buckets: [ { '$bucketAuto': { groupBy: '$price', buckets: 3 } } ] } } ],
     cursor: {},
     '$db': 'shopper' },
  ok: 1,
  '$clusterTime': 
   { clusterTime: Timestamp({ t: 1671798505, i: 30 }),
     signature: 
      { hash: Binary(Buffer.from("c70cce1c2f977a04725fd2bfa879fdaa4aa48c87", "hex"), 0),
        keyId: 7148513146209042000 } },
  operationTime: Timestamp({ t: 1671798505, i: 30 }) }
```

```
db.products.explain("executionStats").aggregate([{
 $match: { "$and":[
  {product_id: {$gte: 112}},
  {brand: "Albert Heijn"}
  ]
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
}])
{ explainVersion: '1',
  stages: 
   [ { '$cursor': 
        { queryPlanner: 
           { namespace: '621434f943d3e75ba8bce014_shopper.products',
             indexFilterSet: false,
             parsedQuery: 
              { '$and': 
                 [ { brand: { '$eq': 'Albert Heijn' } },
                   { product_id: { '$gte': 112 } } ] },
             queryHash: '9848F89E',
             planCacheKey: '5EBF9451',
             maxIndexedOrSolutionsReached: false,
             maxIndexedAndSolutionsReached: false,
             maxScansToExplodeReached: false,
             winningPlan: 
              { stage: 'PROJECTION_SIMPLE',
                transformBy: { price: 1, _id: 0 },
                inputStage: 
                 { stage: 'FETCH',
                   filter: 
                    { '$and': 
                       [ { brand: { '$eq': 'Albert Heijn' } },
                         { product_id: { '$gte': 112 } } ] },
                   inputStage: 
                    { stage: 'IXSCAN',
                      keyPattern: { price: -1 },
                      indexName: 'price_-1',
                      isMultiKey: false,
                      multiKeyPaths: { price: [] },
                      isUnique: false,
                      isSparse: false,
                      isPartial: false,
                      indexVersion: 2,
                      direction: 'forward',
                      indexBounds: { price: [ '[MaxKey, MinKey]' ] } } } },
             rejectedPlans: [] },
          executionStats: 
           { executionSuccess: true,
             nReturned: 12646,
             executionTimeMillis: 286,
             totalKeysExamined: 55555,
             totalDocsExamined: 55555,
             executionStages: 
              { stage: 'PROJECTION_SIMPLE',
                nReturned: 12646,
                executionTimeMillisEstimate: 201,
                works: 55556,
                advanced: 12646,
                needTime: 42909,
                needYield: 0,
                saveState: 56,
                restoreState: 56,
                isEOF: 1,
                transformBy: { price: 1, _id: 0 },
                inputStage: 
                 { stage: 'FETCH',
                   filter: 
                    { '$and': 
                       [ { brand: { '$eq': 'Albert Heijn' } },
                         { product_id: { '$gte': 112 } } ] },
                   nReturned: 12646,
                   executionTimeMillisEstimate: 194,
                   works: 55556,
                   advanced: 12646,
                   needTime: 42909,
                   needYield: 0,
                   saveState: 56,
                   restoreState: 56,
                   isEOF: 1,
                   docsExamined: 55555,
                   alreadyHasObj: 0,
                   inputStage: 
                    { stage: 'IXSCAN',
                      nReturned: 55555,
                      executionTimeMillisEstimate: 77,
                      works: 55556,
                      advanced: 55555,
                      needTime: 0,
                      needYield: 0,
                      saveState: 56,
                      restoreState: 56,
                      isEOF: 1,
                      keyPattern: { price: -1 },
                      indexName: 'price_-1',
                      isMultiKey: false,
                      multiKeyPaths: { price: [] },
                      isUnique: false,
                      isSparse: false,
                      isPartial: false,
                      indexVersion: 2,
                      direction: 'forward',
                      indexBounds: { price: [ '[MaxKey, MinKey]' ] },
                      keysExamined: 55555,
                      seeks: 1,
                      dupsTested: 0,
                      dupsDropped: 0 } } } } },
       nReturned: 12646,
       executionTimeMillisEstimate: 254 },
     { '$facet': 
        { price_buckets: 
           [ { '$teeConsumer': {},
               nReturned: 12646,
               executionTimeMillisEstimate: 259 },
             { '$bucketAuto': 
                { groupBy: '$price',
                  buckets: 3,
                  output: { count: { '$sum': { '$const': 1 } } } },
               nReturned: 3,
               executionTimeMillisEstimate: 286 } ] },
       nReturned: 1,
       executionTimeMillisEstimate: 286 } ],
  serverInfo: 
   { host: 'ez-free-cluster-shard-00-02.mz3yq.mongodb.net',
     port: 27017,
     version: '5.0.14',
     gitVersion: '1b3b0073a0b436a8a502b612f24fb2bd572772e5' },
  serverParameters: 
   { internalQueryFacetBufferSizeBytes: 104857600,
     internalQueryFacetMaxOutputDocSizeBytes: 104857600,
     internalLookupStageIntermediateDocumentMaxSizeBytes: 16793600,
     internalDocumentSourceGroupMaxMemoryBytes: 104857600,
     internalQueryMaxBlockingSortMemoryUsageBytes: 33554432,
     internalQueryProhibitBlockingMergeOnMongoS: 0,
     internalQueryMaxAddToSetBytes: 104857600,
     internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600 },
  command: 
   { aggregate: 'products',
     pipeline: 
      [ { '$match': { '$and': [ { product_id: { '$gte': 112 } }, { brand: 'Albert Heijn' } ] } },
        { '$sort': { price: -1 } },
        { '$facet': { price_buckets: [ { '$bucketAuto': { groupBy: '$price', buckets: 3 } } ] } } ],
     cursor: {},
     '$db': 'shopper' },
  ok: 1,
  '$clusterTime': 
   { clusterTime: Timestamp({ t: 1671798870, i: 124 }),
     signature: 
      { hash: Binary(Buffer.from("318d78699e69f5b43a81d7dd8e4e963a5b954594", "hex"), 0),
        keyId: 7148513146209042000 } },
  operationTime: Timestamp({ t: 1671798870, i: 124 }) }
```