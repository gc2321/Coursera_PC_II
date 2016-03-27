"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
codeskulptor.set_timeout(100000000)

WORDFILE = "assets_scrabble_words3.txt"

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative and not use set().
    """
    list2=[]
    for each in list1:
        if each not in list2:
            list2.append(each)            

    return list2 

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """    
    return [val for val in list1 if val in list2]

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """ 
    list3 =list1+list2
    new_list=[]
    while list3:
        minimum = list3[0]  
        for num in list3: 
            if num < minimum:
                minimum = num
                
        new_list.append(minimum)
        list3.remove(minimum)    

    return new_list

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if list1 == []:
        return list1
    else:
        pivot = list1[0]
        lesser = [num for num in list1 if num < pivot]
        equal = [num for num in list1 if num == pivot]
        greater = [num for num in list1 if num > pivot]
        return merge(merge_sort(lesser)+equal, merge_sort(greater))
    
# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """ 
    word_list=[]
    if word == "":
        return [""]
    else:
        first = word[0]
        all_but_first = gen_all_strings(word[1:])
        
        word_list.append(first)
        
        for let in all_but_first:
            word_list.append(let)  
            
            if let!="":
                word_list.append(first+let)
                word_list.append(let+first)
                num = 1
                while num < len(let): 
                    word_list.append(let[:num]+first+let[num:])
                    num +=1
                         
    return word_list 

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
                          
    return net_file.read().split('\n')

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
