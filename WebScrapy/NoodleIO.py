import datetime

import pymongo


class NoodleIO(object):

    def __init__(self):
        self.host = "master"
        self.port = 17585
        self.db = "noodle"
        self.client = pymongo.MongoClient(host=self.host,
                                          port=self.port,
                                          connect=False)
        self.db = self.client.get_database(self.db)

    def __del__(self):
        self.client.close()

    def save(self, table: str, data: dict, spec_key: list=[], update_columns: list=None) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %X")
        spec = {k: data[k] for k in spec_key}
        document = {k: data[k] for k in update_columns} if update_columns else data
        document.setdefault("timestamp", timestamp)
        self.db.get_collection(table).update(spec=spec,
                                             document=document,
                                             upsert=True)
        return document

    def load(self, table: str, spec: dict={}, find_columns: list=[],
             limit: int=None, order_by: dict ={}):
        columns = {c: 1 for c in find_columns}
        columns.update({"_id": 0})
        data = self.db.get_collection(table).find(spec, columns)
        if order_by:
            data = data.sort(list(order_by.items()))
        if limit:
            data = data.limit(limit)
        return list(data)




