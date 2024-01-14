# Problem Set 4a
# Name: Bobby Albani
# Collaborators: None
# Time spent: 0:30

from tree import Node  # Imports the Node object used to construct trees

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the tests named data_representation should pass.
tree_1 = Node(8, Node(2, Node(1), Node(6)), Node(10))
tree_2 = Node(7, Node(2, Node(1), Node(5, Node(3), Node(6))), Node(9, Node(8), Node(10)))
tree_3 = Node(5, Node(3, Node(2), Node(4)), Node(14, Node(12), Node(21, Node(20), Node(26))))

def find_tree_height(tree):
    '''
    Find the height of the given tree
    Input:
        tree: An element of type Node constructing a tree
    Output:
        The integer depth of the tree
    '''
    #If there is no children, the height is 0
    if tree.get_left_child() == None and tree.get_right_child() == None:
        return 0
    
    #If there is one child on the right, return 1 + heigh of right tree
    elif tree.get_left_child() == None and tree.get_right_child()!= None:
        return 1 + find_tree_height(tree.get_right_child())
    
    #Do the same if there is only one child on the left. 
    elif tree.get_left_child() != None and tree.get_right_child() == None:
        return 1 + find_tree_height(tree.get_left_child())
    
    #If both sids have children, return the one that has the biggest height
    elif tree.get_left_child() != None and tree.get_right_child() != None:
        return max(1 + find_tree_height(tree.get_left_child()), 1 + find_tree_height(tree.get_right_child()))
    

def is_heap(tree, compare_func):
    '''
    Determines if the tree is a max or min heap depending on compare_func
    Inputs:
        tree: An element of type Node constructing a tree
        compare_func: a function that compares the child node value to the parent node value
            i.e. compare_func(child_value,parent_value) for a max heap would return False if child_value > parent_value and True otherwise
                 compare_func(child_value,parent_value) for a min meap would return False if child_value < parent_value and True otherwise
    Output:
        True if the entire tree satisfies the compare_func function; False otherwise
    '''
    #If there are no children, the tree is a max or min heap
    if tree.get_left_child() == None and tree.get_right_child() == None:
        return True
    
    #If there is only the right child
    elif tree.get_left_child() == None and tree.get_right_child()!= None:
        #If it doesn't pass the compare function, return false, otherwise call is_heap with right child
        if compare_func(tree.get_right_child().get_value(), tree.get_value()) == False:
            return False
        else:
            return is_heap(tree.get_right_child(), compare_func)
    
    #If there is only the left child
    elif tree.get_left_child() != None and tree.get_right_child() == None:
        #Does the same as the right child
        if compare_func(tree.get_left_child().get_value(), tree.get_value()) == False:
            return False
        else:
            return is_heap(tree.get_left_child(), compare_func)

    #If both sides have children
    elif tree.get_left_child() != None and tree.get_right_child() != None:
        #Both sides have to return true from the compare function, if so return right AND left (Both must be true)
        if compare_func(tree.get_left_child().get_value(), tree.get_value()) == True and compare_func(tree.get_right_child().get_value(), tree.get_value()) == True:
            return is_heap(tree.get_left_child(), compare_func) and is_heap(tree.get_right_child(), compare_func)
        else:
            return False
    
    return True
            

if __name__ == '__main__':
    # You can use this part for your own testing and debugging purposes.
    # IMPORTANT: Do not erase the pass statement below if you do not add your own code
    print(find_tree_height(tree_1)) # should be 2
    print(find_tree_height(tree_2)) # should be 3
    print(find_tree_height(tree_3)) # should be 3
