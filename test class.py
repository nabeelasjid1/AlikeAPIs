class mine:
    def recur(self, num):
        print(num, end="")
        if num > 1:
            print(" * ",end="")
            return num * self.recur(self, num-1)
        print(" =")
        return 1

def main():
    a = mine()
    print(mine.recur(mine, 10))

main()