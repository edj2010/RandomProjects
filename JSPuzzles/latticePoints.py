# Naive search to get an idea

from collections import defaultdict

counts = defaultdict(int)

for a in range(1,200):
    print(a)
    for b in range(1,a):
        for c in range(a):
            for d in range(b):
                if a*a+d*d > a*c+b*d and b*b+c*c > a*c+b*d and a*c+b*d>0:
                    if a*b-c*d==4:
                        print(a,b,c,d)
                    counts[(a*b-c*d)/2]+=1
    b = a
    for c in range(a):
        for d in range(c):
            if a*a+d*d > a*c+b*d and b*b+c*c > a*c+b*d and a*c+b*d>0:
                counts[(a*b-c*d)/2]+=1
            

i = 1
while i < 1000:
    print(i,counts[i])
    i*=2
