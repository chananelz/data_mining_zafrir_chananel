# Zafrir Fourerr   318260023
# Chananel Zaguri 206275711
import copy
import random
from itertools import combinations

N = 5  # no. of attributes
MINSUP = 0.15


# Creates a file named filename containing m sorted itemsets of items 0..N-1
def createfile(m, filename):
    f = open(filename, "w")
    for line in range(m):
        itemset = []
        for i in range(random.randrange(N) + 1):
            item = random.randrange(N)  # random integer 0..N-1
            if item not in itemset:
                itemset += [item]
        itemset.sort()
        for i in range(len(itemset)):
            f.write(str(itemset[i]) + " ")
        f.write("\n")
    f.close()


# Returns true iff all of smallitemset items are in bigitemset (the itemsets are sorted lists)
def is_in(smallitemset, bigitemset):
    s = b = 0  # s = index of smallitemset, b = index of bigitemset
    while s < len(smallitemset) and b < len(bigitemset):
        if smallitemset[s] > bigitemset[b]:
            b += 1
        elif smallitemset[s] < bigitemset[b]:
            return False
        else:
            s += 1
            b += 1
    return s == len(smallitemset)


# Returns a list of itemsets (from the list itemsets) that are frequent
# in the itemsets in filename
def frequent_itemsets(filename, itemsets):
    f = open(filename, "r")
    filelength = 0  # filelength is the no. of itemsets in the file. we
    # use it to calculate the support of an itemset
    count = [0] * len(itemsets)  # creates a list of counters
    line = f.readline()
    while line != "":
        filelength += 1
        line = line.split()  # splits line to separate strings
        for i in range(len(line)):
            line[i] = int(line[i])  # converts line to integers
        for i in range(len(itemsets)):
            if is_in(itemsets[i], line):
                count[i] += 1
        line = f.readline()
    f.close()
    freqitemsets = []  # this list will save the itemsets that have enough support
    abs_support = []   # this list will save the support of each from the itemset
    for i in range(len(itemsets)):
        if count[i] >= MINSUP * filelength:
            freqitemsets += [itemsets[i]]
            abs_support += [count[i]]
    return freqitemsets, abs_support    # return the tow list


def create_kplus1_itemsets(kitemsets, filename):
    kplus1_itemsets = []
    # importent! why we choose to use set? because the implementation of set in python is with hash table
    # and because of that the search in set is mach faster. Hash table is on of the improvement to apriori algorithm
    # that we learned on class.
    set_kitemsets = set()
    for item in kitemsets:
        set_kitemsets.add(frozenset(item))  # add item to set structure

    for i in range(len(kitemsets) - 1):
        j = i + 1  # j is an index
        # compares all pairs, without the last item, (note that the lists are sorted)
        # and if they are equal than adds the last item of kitemsets[j] to kitemsets[i]
        # in order to create k+1 itemset
        while j < len(kitemsets) and kitemsets[i][:-1] == kitemsets[j][:-1]:

            candidate = kitemsets[i] + [kitemsets[j][-1]]  # take candidate from kitemsets

            comb = combinations(candidate, len(kitemsets[0]))  # all the combinations of sub group of candidate
            comb = list(comb)  # turned to list
            flag = True
            for item in comb:
                list_comb = []
                for itm in item:
                    list_comb.append(itm)  # append the combination to the new list -regular list

                if frozenset(list_comb) not in set_kitemsets:  # if one of the comb is not in the original set
                    flag = False  # stop and return false
                    break
            if flag:
                kplus1_itemsets += [kitemsets[i] + [kitemsets[j][-1]]]  # if all the combination is in the original set
                # then append it to  kplus1_itemsets
            j += 1
    # checks which of the k+1 itemsets are frequent
    return frequent_itemsets(filename, kplus1_itemsets)


def create_1itemsets(filename):
    it = []
    for i in range(N):
        it += [[i]]
    return frequent_itemsets(filename, it)


def minsup_itemsets(filename):
    kitemsets, coutkitemsets = create_1itemsets(filename) # get the tow list
    kitemsets_without_count = copy.deepcopy(kitemsets)    # we need to use deep copy because we need original copy of the itemsets
    for i in range(len(kitemsets)):
        kitemsets[i].append(coutkitemsets[i])             # merge the toe list

    minsupsets = kitemsets
    while kitemsets != []:
        kitemsets, coutkitemsets = create_kplus1_itemsets(kitemsets_without_count, filename) # get the tow list
        kitemsets_without_count = copy.deepcopy(kitemsets)                          # we need to use deep copy because we need original copy of the itemsets
        for i in range(len(kitemsets)):
            kitemsets[i].append(coutkitemsets[i])                                # merge the toe list
        minsupsets += kitemsets                                                   # update minsupsets
    return minsupsets


createfile(100, "itemsets.txt")
print(minsup_itemsets("itemsets.txt"))
