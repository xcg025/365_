import pymongo
import userConfig

class DsFootball(object):
    def __init__(self):
        self.client = pymongo.MongoClient(userConfig.MONGO_URL)
        self.db = self.client[userConfig.MONGO_DB_DSFOOTBALL]
        self.collection = self.db[userConfig.MONGO_TABLE_COLLECTIONS]

        # self.client = pymongo.MongoClient('localhost')
        # self.db = self.client['dsfootball']
        # self.collection = self.db['collections']

    def fetch_all(self):
        all = dict()
        for item in self.collection.find():
            all[item['_id']] = item
        return all


if __name__ == '__main__':
    ds = DsFootball()
    print(ds.fetch_all())
    if 'b271547e7e2ebd0ddc65d1e5b00d1d79' in ds.fetch_all():
        print('yes')
    else:
        print('no')