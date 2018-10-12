''' This is the main script for homework 0 '''



class Class1:

    def __init__(self):
        self.x = 123
        self.y = 345

# GLOBALS
obj1 = Class1()
obj2 = Class1()
const_list_1 = [1, 2, obj1]
const_list_2 = [4, 5, 6]

def reset():
    global obj1, const_list_1, const_list_2
    obj1 = Class1()
    obj2 = Class1()
    const_list_1 = [1, 2, obj1]
    const_list_2 = [4, 5, 6]


def manip_list(list_1, list_2):
    '''do part 1'''
    print(list_1[-1]) # Print last element of list 1
    list_1.pop() # Remove last element of list one
    list_2[1] = list_1[0] # Change 2nd element of l1 to 1st element of l2
    print(list_1 + list_2) # Print concatenation of l1 and l2
    return [list_1, list_2] # Return single list with both l1 and l2

def manip_tuple(arg_1, arg_2):
    '''do part 2'''
    tup = tuple([arg_1, arg_2]) #create tuple of both object parameters
    try:
        tup[1] = 1 # throw error by attempting to modify tuple
    except:
        print("Correctly threw an error") # correctly throw the error


def manip_set(list_1, list_2, obj_1):
    '''do part 3'''
    set1 = set(list_1) # create a set from l1
    set2 = set(list_2) # create a set from l2
    set1.add(obj_1) #add the object to set1
    print("True" if obj_1 in set2 else "False") #test if obj is in Test 2
    print(set1.union(set2)) # print the union of the sets
    print(set1.difference(set2)) # print difference of set 1 and 2
    print(set1.intersection(set2)) # print the intersection of set 1 and 2
    set1.remove(obj_1) # remove object from set 1

def manip_dict(tup_1, tup_2, obj):
    '''do part 4'''
    print(tup_1)
    print(tup_2)
    print(obj)
    res = dict(zip(tup_1, tup_2)) #create dictionary of tup_1[i] : tup_2[i]
    print(res[obj]) # print value mapped to obj
    del res[obj] # remove obj from the dict
    print(len(res)) # print the length of the dictionary
    res[obj] = 0 # assign the object to 0
    return res.items() # print 2 tuple list of dict pairs





if __name__ == '__main__':
    print("Part 1 Lists:")
    total_list = manip_list(const_list_1, const_list_2)
    print(total_list)
    print("-------------")
    reset()
    print("Part 2 Tuples:")
    manip_tuple(obj1, obj2)
    print("-------------")
    reset()
    print("Part 3 Sets:")
    manip_set(const_list_1, const_list_2, obj1)
    print("-------------")
    reset()
    print("Part 1 Dictionaries:")
    dictionary = manip_dict(tuple(const_list_1), tuple(const_list_2), obj1)
    print(dictionary)
