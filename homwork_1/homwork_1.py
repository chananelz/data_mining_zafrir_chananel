# homework 01
# Zafrir Fourerr   318260023
# Chananel Zaguri 206275711
# This function read k txt fill and creat k arff fill correspondingly
# In the arff fill each line describe a patient and contain:
# ID
# Time
# category low/high
# הערה חשובה- המרצה אמר שלנפות זה להשים סימן שאלה ולא להתעלם לגמרי.
from math import sqrt


def convert2arff(k):
    for i in range(1, k + 1):  # Go over each file
        fout = open("temp" + str(i) + ".arff", "w")  # read fill
        fout.write("@relation patients_temperatures\n")  # write the opening
        fout.write("@attribute patients_ID numeric\n")
        fout.write("@attribute time numeric\n")
        fout.write("@attribute temperatue {Low,High} \n\n")
        fout.write("@data\n")

        fin = open(str(i) + ".txt", "r")  # open the txt fill
        for time in range(60 * 12):  # slicing - we take into account only 12 hours
            s = fin.readline().split()
            for patient in range(len(s)):  # go over each patient
                temp = float(s[patient])
                roll_up = ""  # save the category
                if temp < 36 or temp > 43:  # check if we need to convert fahrenheit -> celsius
                    temp = (temp - 32) / 1.8  # convert according to the formula
                if temp < 36 or temp > 43:
                    temp = "?"  # if we have error in the data leave out this data
                if temp == "?":
                    continue
                    # roll_up = "?"
                else:
                    if temp > 37:  # we want to classify the data to two section "High" and "Low"
                        roll_up = "High"
                    else:
                        roll_up = "Low"

                fout.write(str(patient + 1) + "," + str(time) + "," + roll_up + "\n")  # write the data in arff fill
        fin.close()  # close the data
    fout.close()


def stdv(k):
    fin = open(str(k) + ".txt", "r")  # open the relevant txt fill
    sum = 0  # this var save the sum
    powSum = 0  # this var save power of the sum
    count = 0  # this var save how many valid instances we have
    for time in range(1440):  # go over 24H
        s = fin.readline().split()  # get the data about each ill
        for patient in range(len(s)):  # go over line
            temp = float(s[patient])  # convert to float
            if temp < 36 or temp > 43:  # convert from Fahrenheit to Celsius
                temp = (temp - 32) / 1.8
            if temp < 36 or temp > 43:  # if the data not valid pass this piece of data
                continue
            sum += temp  # update the var
            powSum += temp * temp
            count = count + 1

    mean = sum / (count)  # calculate the mean
    variance = (powSum / (count)) - mean * mean  # calculate the variance
    fin.close()
    return sqrt(variance)  # return stdv


convert2arff(3)
print(stdv(1))
