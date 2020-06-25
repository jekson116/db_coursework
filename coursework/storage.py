import pymongo


def mongo_collection():
    url = 'mongodb://admin1:admin1@ds263048.mlab.com:63048/terrorism?retryWrites=false'
    return pymongo.MongoClient(url).get_database('terrorism').get_collection('attacks')
