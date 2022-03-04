if __name__ == '__main__':
    di = {"1": [1, 2, 3, 4], "3": 4}
    values = {}
    for i in di.keys():
        values[i] = di[i]
    print(values)
