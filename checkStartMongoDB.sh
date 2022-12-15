#!/bin/bash

# checkStartMongoDB.sh

echo "`date` Start checkStartMongoDB.sh"

echo "`date` Start MongoDB process status check"

# Check if mongod is running on local machine, if not start
# -x flag ensures to only return true if name of process (or command line if -f is specified) exactly matches the pattern. 

if pgrep -x "mongod" > /dev/null
then
    echo "`date` MongoDB already running on local machine"
else
    echo "`date` Start MongoDB on local machine"
    df=/tmp/mongodb/data
    lf=/tmp/mongodb/log
    rm -rf $df
    rm -rf $lf
    mkdir -p $df
    mkdir -p $lf
    mongod --fork --logpath $lf/mongod.log --dbpath $df 
fi

echo "`date` End MongoDB process status check"
echo "`date` End checkStartMongoDB.sh"