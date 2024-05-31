next = [1]
print(len(next))
# while(len(next) < 2):
    # for i in next: 
    #     next.append(2)
    #     next.append(3)
    #     next.pop(0)
    #     print(len(next))
for i in next:
    print("----") 
    print("i: ",i)
    next.append(2)
    next.append(3)
    next.pop(0)
    print(next)
    if (len(next) == 3):
        break
# print(next)