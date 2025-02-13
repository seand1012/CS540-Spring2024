import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

def main():
    file_name = sys.argv[1]
    data = read_file(file_name)
    q2(data)
    X = q3a(data)
    Y = q3b(data)
    Z = q3c(X)
    I = q3d(Z)
    PI = q3e(X, I)
    B = q3f(PI, Y)
    B1 = q4(B)
    q5(B1)
    q6(B)

def read_file(file_name):
    with open(file_name, 'r', newline = '') as file:
        reader = csv.reader(file)
        next(reader)
        data = list(reader)
    data = np.array(data, dtype=np.int64)
    return data

def q2(data):
    years = []
    frozen_days = []
    
    for row in data:
        year = int(row[0])
        frozen_day = int(row[1])
        years.append(year)
        frozen_days.append(frozen_day)

    plt.figure(figsize=(10,6))
    plt.plot(years, frozen_days, marker='o', linestyle='-')
    plt.xlabel('Year')
    plt.ylabel('Frozen Days')
    plt.title('Year vs. Number of Frozen Days')
    plt.grid(True)
    plt.savefig("plot.jpg")
    
def q3a(data):
    X = np.hstack((np.ones((data.shape[0], 1)), data[:, 0].reshape(-1,1)))
    print("Q3a:")
    print(X)
    return X
    
def q3b(data):
    Y = data[:,1]
    print("Q3b:")
    print(Y)
    return Y

def q3c(X):
    Z = np.dot(X.T, X)
    print("Q3c:")
    print(Z)
    return Z

def q3d(Z):
    I = np.linalg.inv(Z)
    print("Q3d:")
    print(I)
    return I
    
def q3e(X, I):
    PI = np.dot(I, X.T)
    print("Q3e:")
    print(PI)
    return PI
    
def q3f(PI, Y):
    B = np.dot(PI, Y)
    print("Q3f:")
    print(B)
    return B
    
def q4(B):
    x_test = np.array([[1, 2022]])
    y_test = np.dot(x_test, B)
    print("Q4:", y_test[0])
    return y_test
    
def q5(B1):
    if B1 > 0:
        print("Q5a: >")
        print("Q5b: This means the slope is positive, so there is an anticipated increase in ice days")
    elif B1 == 0:
        print("Q5a: =")
        print("Q5b: This means the slope is 0, so there will be no more or less ice days next year")
    else:
        print("Q5a: <")
        print("Q5b: This means there is a negative slope, so there will be fewer ice days for next year")
    
def q6(B):
    x = -B[0]/B[1]
    print("Q6a: " + str(x))
    print("Q6b: This tells us that with the trends of warming, there will be no ice days in 2455, which is very upsetting")
    return x
if __name__ == "__main__":
    main()