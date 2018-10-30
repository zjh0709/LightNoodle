class Price(object):

    def __init__(self, code: str, date: str=None,
                 opening: float=0, closing: float=0,
                 high: float=0, low: float=0, volume: float=0):
        self.code = code
        self.date = date
        self.opening = opening
        self.closing = closing
        self.high = high
        self.low = low
        self.volume = volume

    @property
    def properties(self):
        return ["code", "date", "opening", "closing", "high", "low", "volume"]

    def to_dict(self):
        return {k: getattr(self, k) for k in self.properties
                if getattr(self, k) is not None}
