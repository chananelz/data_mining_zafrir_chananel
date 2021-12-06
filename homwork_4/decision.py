'''
Zafrir Fourerr 318260023
Chananel Zaguri 206275711

This program implement decision tree on mindset dataset hw4
'''

import math

MAX_DEPTH = 10  # we save max depth as a const because it make sense but the user can change it. (In python you can change const var)
THRESHOLD = 130  # we save threshold as a const because it make sense but the user can change it. (In python you can change const var)
TRAIN_IMAGES_PATH = r"C:\Users\user1\Desktop\pythonProjects\data_mining_zafrir_chananel\homwork_4\files\train-images.idx3-ubyte"
TRAIN_LABELS_PATH = r"C:\Users\user1\Desktop\pythonProjects\data_mining_zafrir_chananel\homwork_4\files\train-labels.idx1-ubyte"
TEST_IMAGES_PATH = r"C:\Users\user1\Desktop\pythonProjects\data_mining_zafrir_chananel\homwork_4\files\t10k-images.idx3-ubyte"
TEST_LABELS_PATH = r"C:\Users\user1\Desktop\pythonProjects\data_mining_zafrir_chananel\homwork_4\files\t10k-labels.idx1-ubyte"

# --------------------------------------------------------------------------------------------------------------------------------
# ONLY FOR DEBUGGING - TAKE DATA FROM TXT FILE
"""
הערה לבודק התרגיל: מכיוון שמדובר בכמות נתונים גדולה שלא ניתן לדבגה עם חומרה פשוטה לקחנו את המידע בפורמט טקסט כדי שיהיה ניתן לקרוא את המידע והקטנו את היקף המידע
 הדבר נעשה באישור המרצה גיא קלמן להלן הפונקציות המקבילות למה שהיה היה אמור להיות באמת הם מחזירות רשימות מוקטנות
"""

# כאן נשמרים המקומות שמהם לוקחים את הקבצים החלקיים
TRAIN_IMAGES_PATH_TXT = r"C:\Users\user1\Desktop\pythonProjects\data_mining_zafrir_chananel\homwork_4\files\digits-training.txt"
TEST_LABELS_PATH_TXT = r"C:\Users\user1\Desktop\pythonProjects\data_mining_zafrir_chananel\homwork_4\files\digits-testing.txt"


def preprocess_change2Binary_semi():
    """
    get file name and preprocess the data on the file
    :return: n two list - images and labels
    """
    fimages = open(TRAIN_IMAGES_PATH_TXT, "r")

    list_images = []
    list_labels = []

    # read all the lines in the data
    for line in fimages.readlines():
        fields = line.split(',')
        image = []
        for i in range(len(fields) - 1):
            image.append(check_value(int(fields[i])))  # convert the data to 0/1
        image.append(
            'x')  # we enter x and after that we will delete it we need to do that because we did it in the original script
        list_labels.append(int(fields[-1]))
        list_images.append(image)

    fimages.close()
    print("End")
    return list_images, list_labels  # return two list - images and labels


def get_test_row_semi():
    """
    this method help us in part C when we need one row for test the model
    :return: one image
    """
    fimages = open(TEST_LABELS_PATH_TXT, "r")  # read only data about one image
    for line in fimages.readlines():
        fields = line.split(',')
        image = []
        for i in range(len(fields) - 1):
            image.append(check_value(int(fields[i])))  # convert the data to 0/1
        return image


def get_test_rows_semi():
    """
    this method get all the test data
    :return:  list with all the test images
    """
    fimages = open(TEST_LABELS_PATH_TXT, "r")
    list_images = []
    for line in fimages.readlines():
        fields = line.split(',')
        image = []
        for i in range(len(fields) - 1):
            image.append(check_value(int(fields[i])))  # convert the data to 0/1
        image.append(int(fields[-1]))
        list_images.append(image)
    return list_images


# -----------------------------------------------------------------------------------------------------------------------------------
# ORIGINAL SCRIPT - GET DATA FROM UBYTE FILE

def preprocess_change2Binary():
    """
    get file name and preprocess the data on the file
    :return: n two list - images and labels
    """
    fimages = open(TRAIN_IMAGES_PATH, "rb")
    flabels = open(TRAIN_LABELS_PATH, "rb")
    list_images = []
    list_labels = []

    flabels.seek(8)  # we need this comannds because we use ubyte format
    fimages.seek(16)
    x = fimages.read(1)
    while x != b"":
        image = []
        image.append(check_value(ord(x)))  # convert the data to 0/1 according to the threshold
        for i in range(783):  # get over all attribute = pixel
            image.append(check_value(ord((fimages.read(1)))))
        image.append('x')
        list_labels.append(ord(flabels.read(1)))  # we use ord because we deal with ubyte format
        list_images.append(image)
        x = fimages.read(1)
    fimages.close()
    flabels.close()
    print("End")
    return list_images, list_labels


def get_test_rows():
    """
    run the files of labels test and images test
    :return: list of labels and their targets together for test
    """
    fimages = open(TEST_IMAGES_PATH, "rb")
    flabels = open(TEST_LABELS_PATH, "rb")
    list_images = []
    flabels.seek(8)  # we need this comannds because we use ubyte format
    fimages.seek(16)
    x = fimages.read(1)
    while x != b"":
        image = []
        image.append(check_value(ord(x)))  # convert the data to 0/1 according to the threshold
        for i in range(783):  # get over all attribute = pixel
            image.append(check_value(ord((fimages.read(1)))))
        image.append(ord(flabels.read(1)))
        list_images.append(image)
        x = fimages.read(1)
    fimages.close()
    flabels.close()
    print("End")
    return list_images


# -----------------------------------------------------------------------------------------------------------------------------------

def threshold():
    """
    run all over appropriate threshold and check the most threshold that satisfies the most accuracy
    :return: the best thershold to divide the data to binary
    """
    global THRESHOLD
    best_threshold = -1  # this var save the threshold with the best accuracy
    best_threshold_accuracy = -1  # this var save the accuracy of the threshold with the best accuracy
    model_threshold = build_models(preprocess_change2Binary_semi())  # build models from the data
    for i in range(0, 256):   # go over all the potential threshold
        THRESHOLD = i    # update the threshold
        accuracy = tester(model_threshold, get_test_rows_semi())  # get the accuracy with that threshold
        if accuracy > best_threshold_accuracy:  # update best_threshold
            best_threshold_accuracy = accuracy
            best_threshold = THRESHOLD
    print(best_threshold_accuracy)
    THRESHOLD = 130
    return best_threshold


def tester(models, test_list):
    """
    run the classify method for test
    :param models:
    :param test_list:
    :return: accuracy of the model based on test
    """
    counter = 0  # save how many good classifier was
    for test_image in test_list:
        real_target = test_image[-1]  # save the target from the test
        del test_image[-1]
        all_target = classify(models, test_image)  # save the targets
        if len(all_target) == 1 and real_target == all_target[0]:
            counter += 1
    return (counter / (len(test_list))) * 100  # return the accuracy of the model


def classify(models, test_img):
    """
    run all over the models and get the models classify to 1
    :param models:
    :param test_img:
    :return: the indexes of the models satisfies the test data
    """
    index_list = []
    for i in range(10):  # go over all the potential target
        if classifier(models[i], test_img) == 1:
            index_list.append(i)
    return index_list


def check_value(x):
    """
    check the value of threshold to change the data to binary
    :param x:
    :return: 1- bigger than threshold or equal  , 0-otherwise
    """
    if x >= THRESHOLD:
        return 1
    else:
        return 0


def build_models(list_images_labels):
    """
    run ten times and create model based on train data and  index
    :param list_images_labels:
    :return: ten models for train every digits (0-9)
    """
    list_images = list_images_labels[0]
    list_labels = list_images_labels[1]
    module = []  # save the modules for every digit (0-9)
    for i in range(10):
        module.append(build_one_module(list_images, list_labels, i))
    return module


def build_one_module(list_images, list_labels, index):
    """
    change the target to be 1 or 0 according to the index
    :param list_images:
    :param list_labels:
    :param index:
    :return: one model based on train data
    """
    for j in range(len(list_labels)):  # change the labels of image according to the index
        if list_labels[j] == index:
            list_images[j][-1] = 1
        else:
            list_images[j][-1] = 0
    return build(list_images, MAX_DEPTH)


def buildclassifier(train_images, train_labels, d):
    """
    build classifer according to train data and limited depth
    :param train_images:
    :param train_labels:
    :param d:
    :return: func-"build models" that generate the models after change the values to binary
    """
    global TRAIN_IMAGES_PATH  # we use global because on the one hand the method need to get the file path but
    global TRAIN_LABELS_PATH  # on the other hand it more correct that all the path will save at the beginning
    global MAX_DEPTH

    TRAIN_IMAGES_PATH = train_images
    TRAIN_LABELS_PATH = train_labels
    MAX_DEPTH = d

    return build_models(preprocess_change2Binary_semi())


def split(examples, used, trait):
    """
    examples is a list of lists. every list contains the attributes, the last item is the class. all items are 0/1.
    splits examples into two lists based on trait (attribute).
    updates used that trait was used.
    """
    newEx = [[], []]  # newEx is a list of two lists, list of Ex that Ex[trait]=0 and list of Ex that Ex[trait]=1
    if trait < 0 or trait > len(examples[0]) - 2 or used[trait] == 0:
        return newEx  # illegal trait
    for e in examples:  # e is a list that represent a instance
        newEx[e[trait]] += [e]
    used[trait] = 0  # used is a list that marks trait as used
    return newEx


def isSameClass(examples):  # TODO  cover this function
    """
    returns 0 if all the examples are classified as 0.
    returns 1 if all the examples are classified as 1.
    returns 7  if there are no examples.
    returns -2 if there are more zeros than ones.
    returns -1 if there are more or equal ones than zeros.
    """
    if examples == []:
        return 7
    zo = [0, 0]  # zo is a counter of zeros and ones in class
    for e in examples:
        zo[e[-1]] += 1
    if zo[0] == 0:
        return 1
    if zo[1] == 0:
        return 0
    if zo[0] > zo[1]:
        return -2
    else:
        return -1


def infoInTrait(examples, i):  # TODO  cover this function
    """
    calculates the information in trait i using Shannon's formula
    """
    count = [[0, 0], [0, 0]]  # [no. of ex. with attr.=0 and clas.=0,no. of ex. with attr.=0 and clas.=1],
    # [no. of ex. with attr.=1 and clas.=0,no. of ex. with attr.=1 and clas.=1]
    for e in examples:
        count[e[i]][e[-1]] += 1
    x = 0
    # Shannon's formula
    if count[0][0] != 0 and count[0][1] != 0:
        x = count[0][0] * math.log((count[0][0] + count[0][1]) / count[0][0]) + count[0][1] * math.log(
            (count[0][0] + count[0][1]) / count[0][1])
    if count[1][0] != 0 and count[1][1] != 0:
        x += count[1][0] * math.log((count[1][0] + count[1][1]) / count[1][0]) + \
             count[1][1] * math.log((count[1][0] + count[1][1]) / count[1][1])
    return x


def minInfoTrait(examples, used):
    """
    used[i]=0 if trait i was already used. 1 otherwise.

    Returns the number of the trait with max. info. gain.
    If all traits were used returns -1.
    """
    minTrait = m = -1
    for i in range(len(used)):
        if used[i] == 1:
            info = infoInTrait(examples, i)
            if info < m or m == -1:
                m = info
                minTrait = i
    return minTrait


def build(examples, max_depth=10):  # builds used
    global MAX_DEPTH  # update MAX_DEPTH
    MAX_DEPTH = max_depth
    used = [1] * (len(examples[0]) - 1)  # used[i]=1 means that attribute i hadn't been used
    return recBuild(examples, used, 0, 0)


def recBuild(examples, used, parentMaj, depth):
    """
    Builds the decision tree.
    parentMaj = majority class of the parent of this node. the heuristic is that if there is no decision returns parentMaj
    """
    cl = isSameClass(examples)
    if cl == 0 or cl == 1:  # all zeros or all ones
        return [[], cl, []]
    if cl == 7 or depth == MAX_DEPTH:  # examples is empty
        return [[], parentMaj, []]
    trait = minInfoTrait(examples, used)
    if trait == -1:  # there are no more attr. for splitting
        return [[], cl + 2, []]  # cl+2 - makes cl 0/1 (-2+2 / -1+2)
    x = split(examples, used, trait)
    left = recBuild(x[0], used[:], cl + 2, depth + 1)
    right = recBuild(x[1], used[:], cl + 2, depth + 1)
    return [left, trait, right]


def recClassifier(dtree, traits):  # dtree is the tree, traits is an example to be classified
    if dtree[0] == []:  # there is no left child, means arrive to a leaf
        return dtree[1]
    return recClassifier(dtree[traits[dtree[1]] * 2], traits)  # o points to the left child, 2 points to the right child


def classifier(dtree, traits):  # same as the former without recursion
    while dtree[0] != []:
        dtree = dtree[traits[dtree[1]] * 2]  # dtree[1] - atrebut , traits[dtree[1]] value of the ficher
    return dtree[1]


# part A - add to the method parameter - max depth
e = [[1, 0, 0, 0, 0],
     [0, 1, 1, 0, 1],
     [1, 1, 1, 0, 0],
     [1, 1, 0, 1, 0],
     [0, 0, 1, 1, 1],
     [1, 0, 1, 1, 0],
     [1, 0, 0, 1, 1]]
t = build(e, 15)

# part B - creat buildclassifie method:
x = buildclassifier(TRAIN_IMAGES_PATH, TRAIN_LABELS_PATH, 20)

# part C - creat classify method:

list_target = classify(x, get_test_row_semi())
print(list_target)

# part D - creat tester method
print(tester(x, get_test_rows()))

# part C - creat threshold method
print(threshold())

print("end======")
