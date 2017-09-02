import cs50
import sys

def main():
    # control for appropriate input
    if len(sys.argv) != 2:
        print("Inappropriate command line arguments: requires two arguments")
        exit(1)
    if sys.argv[1].isdigit():
        print("Inappropriate command line argument: no digits allowed")
        exit(2)
    # normal program operation
    else:
        p = input("Enter plaintext to encipher: ")
        encipher(p)
        
def encipher(p):
    k = sys.argv[1]
    j = 0
    alphaoffset = 26
    print("Ciphertext: ", end = "")
    # iterate through plaintext input
    for c in range(len(p)):
        # separate non-alphabet characters
        if p[c].isalpha():
            if p[c].isupper():
                # loop through cipher argument
                ml = j%len(k)
                # normalize array value to current case
                uc = k[ml].upper()
                # find alphavalue for cipher key value
                cc = ord(uc) - ord("A")
                # find alphavalue for plaintext value
                cb = ord(p[c]) - ord("A")
                # find offset value
                cp = (cc + cb)%alphaoffset
                # apply offset and print
                cf = cp + ord("A")
                print("{}".format(chr(cf)), end = "")
                j += 1
            if p[c].islower():       
                # loop through cipher argument
                ml = j%len(k)
                # normalize array value to current case
                uc = k[ml].lower()
                # find alphavalue for cipher key value
                cc = ord(uc) - ord("a")
                # find alphavalue for plaintext value
                cb = ord(p[c]) - ord("a")
                # find offset value
                cp = (cc + cb)%alphaoffset
                # apply offset and print
                cf = cp + ord("a")
                print("{}".format(chr(cf)), end = "")
                j += 1       
        else:
            print(p[c], end = "")
            
    print("")
        
if __name__ == "__main__":
    main()