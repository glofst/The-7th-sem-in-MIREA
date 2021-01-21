from import_data import ImportData


class SetK():
    def __init__(self, dic_F):
        self.dic_F = dic_F
        self.multi = []


def print_trans(transactions):
    print('\n<---------------Транзакции--------------->\n')
    for i, key in enumerate(transactions):
        print(f"{key}: {', '.join(transactions.get(key))}")


def get_sets_freq(f, trans, n):

    sets = []
    for k in range(n):
        F = SetK({})
        for key in trans:
            products = trans.get(key)
            if k == 0:
                for product in products:
                    if product not in F.dic_F:
                        F.dic_F.update({product: 1})
                    else:
                        F.dic_F[product] += 1
            elif k == 1:
                c = len(products)
                for i in products:
                    for j in products:
                        if i == j:
                            continue
                        pair = set([i,j])
                        if pair not in F.multi:
                            F.multi.append(pair)
                            F.dic_F.update({F.multi.index(pair): 1})
                        else:
                            F.dic_F[F.multi.index(pair)] += 1
        if k == 2:
            pairs = sets[k-1].multi
            for id, pair in enumerate(pairs):
                if sets[k-1].dic_F[id] >= f:
                    for i, sec_pair in enumerate(pairs):
                        if sets[k-1].dic_F[i] < f:
                            continue
                        if pairs.index(pair) == pairs.index(sec_pair):
                            continue
                        elif not pair.isdisjoint(sec_pair):
                            triad = pair | sec_pair
                            if triad not in F.multi:
                                F.multi.append(triad)
                                try:
                                    weigth = sets[k-1].dic_F[pairs.index(pair ^ sec_pair)]
                                    if weigth > f:
                                        F.dic_F.update({F.multi.index(triad): 1})
                                    else:
                                        F.dic_F.update({F.multi.index(triad): 0})
                                except:
                                    continue
                            else:
                                continue
                        else:
                            continue
                else:
                    continue
        sets.append(F)

        if k == 0:
            print(f'\n<----Наборы, состоящие из {k+1} предмета---->\n\n{sets[k].dic_F}')
        elif k == 1:
            print(f'\n<----Наборы, состоящие из {k+1} предметов---->\n')
            for key in sets[k].dic_F:
                sets[k].dic_F[key] /= 2
                pair = sets[k].multi[key]
                print(f'{pair}: {int(sets[k].dic_F[key])}')
        else:
            print(f'\n<----Наборы, состоящие из {k+1} предметов---->\n')
            for key in sets[k].dic_F:
                triad = sets[k].multi[key]
                print(f'{triad}: {int(sets[k].dic_F[key])}')
    return sets


def assosiation_rules(sets, trans, c_level):
    frequent_recruitments = {}
    count_trans = len(trans)
    print('\n<----------Кандидаты в ассоциативные правила---------->')
    for id, cur_set in reversed(list(enumerate(sets))):
        if id <= 0:
            break
        for recruitment in cur_set.dic_F:
            if (id == 2 and cur_set.dic_F[recruitment] == 1) or id == 1:
                s = cur_set.multi[recruitment]
                print(f'\nНабор: {s}')
                for el in s:
                    one = set([el])
                    pair = s ^ one
                    S = support(count_trans, sets, pair, one)
                    C = credibility(sets, pair, one)
                    s_B = support(count_trans, sets, one)
                    L = lift(C, s_B)
                    values = f'S = {fix(S, 2)}%, C = {fix(C, 2)}%, L = {fix(L, 2)}'
                    print(f'Если {pair}, то {one} => {values}')
                    if C >= c_level and ' - '.join(s) not in frequent_recruitments:
                        frequent_recruitments.update({' - '.join(s): values})
    return frequent_recruitments

def support(count_trans, sets, a, b = set()):
    return probability(sets, a, b)/count_trans*100


def credibility(sets, a, b):
    try:
       return probability(sets, a, b)/probability(sets, a)*100
    except ZeroDivisionError as error:
        print(f'ERROR: in C {error}')
        return -1


def probability(sets, a, b = set()):  
    ab = set(a) ^ b
    weight = 0
    for s in sets:
        try:
            if sets.index(s) == 0 and len(ab) == 1:
                weight = s.dic_F[''.join(ab)]
            else:
                weight = s.dic_F[s.multi.index(ab)]
        except Exception as error:
            continue
    return weight


def lift(cred, sup):
    try:
        return cred/sup
    except ZeroDivisionError as error:
        return -1


def fix(numObj, digits=0):
    return f'{numObj:.{digits}f}'


if __name__ == '__main__':
    file = ImportData('resources/transaktions.txt')
    f = 2
    c_level = 50

    file.read_file()
    trans = file.transactions.copy()
    print_trans(trans)
    sets = get_sets_freq(f, trans, 3)
    frequent_Fs = assosiation_rules(sets, trans, c_level)
    print(f'\n<----------Ассоциативные правила с достоверностью {c_level}%---------->\n')
    for key in frequent_Fs: 
        print(f'{key} => {frequent_Fs[key]}')
