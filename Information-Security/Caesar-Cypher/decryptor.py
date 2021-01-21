class Decryptor:


    def __init__(self):
        pass


    def __keyForAll(self, alphabet, sourceFreq, cryptedFreq):
        decryptor_keys = dict.fromkeys(alphabet)
        used_symbols = ''
        for symbol in alphabet:
            detected_key = sourceFreq.findClosestValue(
                cryptedFreq.getFreq(symbol), 
                used_symbols
            )
            decryptor_keys[symbol] = detected_key
            used_symbols += detected_key
    
        return decryptor_keys


    def keyForOne(self, alphabet, sourceFreq, cryptedFreq):
        decryptorKey = alphabet.index(sourceFreq.getMaxValue()[0])


    def decryptAll(self):
        pass


    def decryptOne(self):
        pass


    def decrypt(self):
        pass