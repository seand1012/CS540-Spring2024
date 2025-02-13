import sys
import math


def main():
    q1()
    q2()
    q3()
    q4()

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    # P(Y = English) = 0.6, P(Y = Spanish) = 1 − P(Y = English) = 0.4
    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()
    
    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X={
        'A': 0,
        'B': 0,
        'C': 0,
        'D': 0,
        'E': 0,
        'F': 0,
        'G': 0,
        'H': 0,
        'I': 0,
        'J': 0,
        'K': 0,
        'L': 0,
        'M': 0,
        'N': 0,
        'O': 0,
        'P': 0,
        'Q': 0,
        'R': 0,
        'S': 0,
        'T': 0,
        'U': 0,
        'V': 0,
        'W': 0,
        'X': 0,
        'Y': 0,
        'Z': 0
    }
    with open (filename, encoding = 'utf-8') as f:        
        for letter in f.read():
            # Checks if the input is a letter
            if letter.isalpha():
                # capitalizes the letter, then finds the letter in
                # the dict and increments its count
                letter = letter.capitalize()
                X[letter] = X.get(letter, 0) + 1
    f.close()
    
    return X



# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!

def q1():
    X = shred('letter.txt')
    print("Q1") 
    for letter,count in X.items():
        print(f"{letter} {count}")

def q2():
    e,s = get_parameter_vectors() 
    X = shred('letter.txt')
    print("Q2")
    print(round(X.get('A') * math.log(e[0]), 4))
    print(round(X.get('A') * math.log(s[0]), 4))

def q3():
    e,s = get_parameter_vectors()
    X = shred('letter.txt')
    F_e,F_s = compute_F(e,s,X)
    print("Q3")
    print(round(F_e,4))
    print(round(F_s,4))
    
def q4():
    e,s = get_parameter_vectors()
    X = shred('letter.txt')
    p_english = compute_P(e, s, X)
    print("Q4")
    print(round(p_english, 4))
    
    
def compute_F(e, s, X):
    sum_e = 0
    sum_s = 0
    for i, (letter, count) in enumerate(X.items()):
        # check to make sure we don't go out of bounds
        if i <= len(e)-1 and i <= len(s)-1:
            # Adds each letter's count to the log of its
            # corresponding probability
            sum_e += (count * math.log(e[i]))
            sum_s += (count * math.log(s[i]))
    F_english = math.log(0.6) + sum_e
    F_spanish = math.log(0.4) + sum_s
    
    return F_english,F_spanish

def compute_P(e, s, X):
    F_e,F_s = compute_F(e,s,X)
    ratio = F_s - F_e
    
    if ratio >= 100:
        return 0
    elif ratio <= -100:
        return 1
    else:
        P_english = 1 / (1 + math.exp(ratio))
        return P_english
    
if __name__ == "__main__":
    main()