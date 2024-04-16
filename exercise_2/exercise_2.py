def donuts(count):
    # In any case where the user can input a variable that isn't an integer or float, we add a conditional part to the code. First, the code checks whether the input is a float or integer.
    if isinstance(count, (float, int)):  # pass tuple
        if count >= 10:
            return "Number of donuts: many"
        else:
            count=int(count)
            return "Number of donuts :" + str(count)
    # If the input variable something else than expected they will see error message
    else:
        return "We only accept Integers" 

def verbing(s):
    # First, the code checks whether the input is string.
    if type(s) == str:
        # Then, it checks the length of the string, and based on that length, it determines whether to proceed with other parts of the code or not.
        if len(s) >= 3:
            # The code checks if the input ends with 'ing', and if it does, it adds 'ly'.
            if s.endswith("ing") == True:
                return s + "ly"
            else:
                return s + "ing"
        else:
            return s
    # If the input variable something else than expected they will see error message
    else:
        return "We only accept Strings" 

def remove_adjacent(nums):
     # First, the code checks whether the input is lists.
    if type(nums) == list:
        # It checks the possibility of there being an empty element of the list.
        if len (nums) == 0:
            return "It is a empty list"
        # The easiest way to eliminate duplicate elements is to convert lists to sets because in Python, sets do not contain duplicate elements within their type.
        else:
            num = list(set(nums))
            return num
    # If the input variable something else than expected they will see error message
    else:
        return "We only accept Lists" 


def main():
    print('donuts')
    print(donuts(4))
    print(donuts(9))
    print(donuts(9.3))
    print(donuts('twenty'))
    

    print('verbing')
    print(verbing('full'))
    print(verbing('swimming'))
    print(verbing('do'))

    print('remove_adjacent')
    print(remove_adjacent([1, 2, 2, 3]))
    print(remove_adjacent((2, 2, 3, 3, 3)))
    print(remove_adjacent([]))

# Standard boilerplate to call the main() function
if __name__ == '__main__':
    main()



