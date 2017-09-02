import cs50

def main():
    while True:
        print("Please indicate how much change is owed.")
        c = cs50.get_float()
        if c > 0:
            break
    get_greedy(c)
    
def get_greedy(c):
    qtr = 0.25
    dime = 0.10
    nick = 0.5
    pen = 0.01
    cu = 0
    while c >= qtr:
        c = c - qtr
        cu += 1
    while c >= dime:
        c = c - dime
        cu += 1    
    while c >= nick:
        c = c - nick
        cu += 1    
    while c >= pen:
        c = c - pen
        cu += 1
    print("{}".format(cu))
        
if __name__ == "__main__":
    main()