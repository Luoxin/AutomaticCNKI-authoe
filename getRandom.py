import random
import time

def getRandom(min,max):
    while True:
        try:
            num=[]
            for i in range(100):
                a=random.random()
                b=time.time()
                num.append(int(a*b))
                random.seed(a*b)

            random.shuffle(num)
            a=random.choice(num)

            a=a%num[0]

            while a > 0:
                a=int(a/random.uniform(min,max))
                # print(a)
                if a >= min and a <= max:
                    break

            if a>=min and a<=max:
                return a
        except:
            pass

if __name__ == '__main__':
    print(getRandom(5,10))

