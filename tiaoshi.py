def queen(n):
    str = '.' * n
    list = []
    for i in range(1,n+1):
        list.append(str)
    # print(list)
    for a in range(n):
        for b in range(n):
            list[a] = list[a].replace(list[a][b],'Q')
    print(list)
if __name__ == '__main__':
    queen(4)
