def findmax(db):
    """Returns the maximum element from a database (dictionary)"""
    db2 = [i for i in db.values() if isinstance(i, int) or isinstance(i, float)]
    maximum = max(db2)
    return maximum

def findmin(db):
    """Returns the minimum element from a database (dictionary)"""
    db2 = [i for i in db.values() if isinstance(i, int) or isinstance(i, float)]
    minimum = min(db2)
    return minimum

def main():
    db = {'a': 4, 'b': 6.5, 'c': 'der'}
    max_value = findmax(db)
    print(max_value)
    min_value = findmin(db)
    print(min_value)

if __name__ == '__main__':
    main()
