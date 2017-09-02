import cs50

def main():
    while True:
        print("Please indicate the height of the half-pyramid")
        h = cs50.get_int()
        if h > 0 and h < 24:
            break
    build_pyramid(h)
    
def build_pyramid(h):
    r = 1
    for r in range(h):
        for s in range(h + 1 - r):
            print(" ", end = "")
        for n in range(1 + r):
            print("#", end = "")
        print(" ", end = "")
        for f in range(1 + r):
            print("#", end = "")
        print("")
        
if __name__ == "__main__":
    main()