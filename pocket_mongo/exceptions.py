class PocketMongoConfigError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        Exception.__init__(
            self,
            'A configuration error has occurred: %s. '
            'Make sure you have called pocket_mongo.config' % msg,
        )
