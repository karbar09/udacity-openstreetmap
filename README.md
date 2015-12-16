# udacity-openstreetmap
Data wrangling with openstreetmap data!

#Problems Encountered
    Street Names in Chinese or English, or both
        Maybe Change address street structure to have different name for "en" and "zh" version
    

#Data Overview
    > File Sizes:
        shanghai_china.osm - 485.4 mb
        shanghai_china.osm.json - 527.8 mb
    
    ##Number of Documents
    > db.shanghai_osm.count()
    2422310
    
    ##Number of Nodes
    > db.shanghai_osm.find({type:"node"}).count()
    2166547

    ##Number of Ways
    > db.shanghai_osm.find({type:"way"}).count()
    255451    


#Additional Ideas
    Some Idea
    Extra Queries
    Conclusion


#Important Queries:

db.shanghai_osm.aggregate([{"$group":{_id:"$address.street",total:{"$sum":1}}},{"$sort":{"total":1}}]);
db.shanghai_osm.find({'address.street':{"$exists":1}}).pretty()
db.shanghai_osm.aggregate([{"$match":{"type":{"$exists":1}}},{"$group":{_id:"$created.user",total:{"$sum":1}}},{"$sort":{"total":1}}])