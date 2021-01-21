import random
from frequency_table import FrequencyTable
from bigram_freq_table import BigramFrequencyTable

alphabet = tuple('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')


source_name = 'WaP_random_chapter.txt'


def encryptor(source, key):
    result = ''
    for line in source:
        for symbol in line:
            if symbol.lower() in alphabet:
                crypted_symbol = alphabet[alphabet.index(symbol.lower()) - key]
                if symbol.isupper():
                    crypted_symbol = crypted_symbol.upper()
                result += crypted_symbol
            else:
                result += symbol
    return result



def keyForOne(sourceFreq, cryptedFreq):
    return -(alphabet.index(sourceFreq.getMaxValue()[0]) - 
                alphabet.index(cryptedFreq.getMaxValue()[0]))


def key_finder(source_freq, crypted_freq):
    decryptor_keys = dict.fromkeys(alphabet)
    used_symbols = ''
    for symbol in alphabet:
        detected_key = source_freq.findClosestValue(
            crypted_freq.getFreq(symbol), 
            used_symbols
        )
        decryptor_keys[symbol] = detected_key
        used_symbols += detected_key
    
    return decryptor_keys


def decryptor(source, decryptor_keys):
    result = ''
    for line in source:
        for symbol in line:
            if symbol.lower() in alphabet:
                decrypted_symbol = decryptor_keys[symbol.lower()]
                if symbol.isupper():
                    decrypted_symbol = decrypted_symbol.upper()
                result += decrypted_symbol
            else:
                result += symbol
    return result

def check_for_match(text1, text2):
    cases_amount = 0
    suc_cases_amount = 0
    for text1_line in text1:
        text2_line = text2.readline()
        for iterat in range(len(text1_line)):
            cases_amount += 1
            if text1_line[iterat] == text2_line[iterat]:
                suc_cases_amount += 1
    print(f'Texts matches for {(suc_cases_amount/cases_amount)*100}%')




if __name__ == '__main__':

    caesar_cypher_key = random.randint(1, len(alphabet)-1)
    print(f'\nCaesar Cypher Key: {caesar_cypher_key}\n')
    
    with open(source_name, 'r') as source, open('crypted_file.txt', 'w') as crypted_file:
        crypted_file.write(encryptor(source, caesar_cypher_key))

    #book_bigram_freq_table = BigramFrequencyTable('War_and_Peace_by_Tolstoy.txt', alphabet)
    #crypted_file_bigram_freq_table = BigramFrequencyTable('crypted_file.txt', alphabet)

    whole_book_freq_table = FrequencyTable('War_and_Peace_by_Tolstoy.txt', alphabet)
    crypted_file_freq_table = FrequencyTable('crypted_file.txt', alphabet)
    #decryptor_keys = keyForOne(whole_book_freq_table, crypted_file_freq_table)
    decryptor_keys = key_finder(whole_book_freq_table, crypted_file_freq_table)

    with open('crypted_file.txt', 'r') as crypted_file, open('decrypted_file.txt', 'w') as decrypted_file:
        decrypted_file.write(decryptor(crypted_file, decryptor_keys))
        #decrypted_file.write(encryptor(crypted_file, keyForOne(book_bigram_freq_table, crypted_file_bigram_freq_table)))

    with open('decrypted_file.txt', 'r') as decrypted_file, open(source_name, 'r') as source:
        check_for_match(source, decrypted_file)
