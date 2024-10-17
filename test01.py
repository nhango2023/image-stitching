class test():
    def  __init__(self):
        self.x = 2

def change (x):
    x=3


test1 = test()
change(test1.x)

print(test1.x)