class Key:

    def __init__(self, n, k):
        self.n = n
        self.k = k

    def crypt(self, symbol):
        return pow(symbol, self.k, self.n)
