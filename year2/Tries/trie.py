def query(filename,id_prefix,last_name_prefix):
    """
    This function is to find all the record matched the id prefix and last name prefix
    Time Complexity:Best:O(NM) for reading the file. O(T) for generating the trie.O(k+l) for query which has no match record
                    Worst:O(NM) for reading the file. O(T) for generating the trie.O(k+l+n_k+n_l) for query that has matches
    Space Complexity:Best:O(NM) for reading the file. O(T) for generating the trie. O(k+l) for query which has no match record
                    Worst:O(NM) for reading the file. O(T) for generating the trie.O(k+l+n_k+n_l) for query that has matches
    Error Handle: If the file is empty, return an empty list
    :Precondition: the file is valid, id only contains numbers and last name only contains letters
    :param filename: the file to be read
    :param id_prefix: the id_prefix is used to be a query to find the matched records
    :param last_name_prefix: the last_name_prefix is used to be a query to find the matched records
    :return: return a list that contains all the indexes that has the id_prefix and last_name_prefix
    """
    #reading data and processing
    indices=[]
    file=open(filename,"r")
    data=file.read()
    if len(data)==0:
        #in case it's an empty file
        return indices
    data=data.split("\n")
    for person in range (len(data)):
        info=[]
        temp=data[person].split(" ")
        for items in temp:
            info.append(items)
        data[person]=info
    # generate id prefix trie and filter data using id_prefix
    prefix_trie=built_tries_num(data,12)
    filtered=look_up_prefix_trie(prefix_trie,id_prefix,12)
    if filtered is None:
        return indices
    temp_list=[]
    for elements in range (len(filtered)):
        temp_list.append([])
        temp_list[elements].append(data[filtered[elements]][0])
        temp_list[elements].append(data[filtered[elements]][3])
    filtered=temp_list
    for elements in range (len(filtered)):
        tmp=[]
        for letter in filtered[elements][1]:
            tmp.append(transferToNum(letter))
        filtered[elements][1]=tmp

    # generate last name prefix trie and filter data using last_name_prefix
    filtered_trie=built_tries_num(filtered,54)
    temp_last_name=[]
    for char in last_name_prefix:
        temp_last_name.append(transferToNum(char))
    last_name_prefix=temp_last_name
    result=look_up_prefix_trie(filtered_trie,last_name_prefix,54)
    if result is None:
        return []
    for items in range (len(result)):
        pos=result[items]
        index=int(filtered[pos][0])
        value =data[index]
        indices.append(int(value[0]))
    return indices
def transferToNum(char):
    """
    This function is to convert a letter to a num using ASCII
    Time Complexity:Best:O(1)
                    Worst:O(1)
    Space Complexity:Best:O(1)
                    Worst:O(1)
    Error Handle:None
    :Precondition: the parameter must be a valid char in the ASCII
    :param char: the char to be converted
    :return: a num corresponding to the letter
    """
    if char.isupper():
        num=ord(char)-ord("A")+26
    else:
        num=ord(char)-ord("a")
    return num
def transferToLetter(num):
    """
    This function is to transfer a num to it's corresponding letter
    Time Complexity:Best:O(1)
                    Worst:O(1)
    Space Complexity:Best:O(1)
                    Worst:O(1)
    Error Handle: None
    :Precondition: the parameter must be a number
    :param num: the num to be converted into a letter
    :return: a letter corresponding to the num
    """
    char=chr(ord('a')+int(num))
    return char

def built_tries_num(data,spots):
    """
    This function is to build the prefix trie
        Time Complexity:Best:O(T). It needs to proceed all the IDs and last names
                    Worst:O(T). It needs to proceed all the IDs and last names
    Space Complexity:Best:O(T). The indexes of all IDs and last names need to take T places and putting all IDs and last names into tries
                    would take O(T)
                    Worst:O(T). The indexes of all IDs and last names need to take T places and putting all IDs and last names into tries
                    would take O(T)
    Error Handle: None
    :Precondition: None
    :param data: the list data to be made into a trie
    :param spots: the number of spots a node should have
    :return: a trie that contains all the data
    """
    trie=[0 for i in range (spots)]
    trie[spots-1]=[]
    for person in range (len(data)):
        trie=insert_nodes(trie,data[person][1],person,spots)
    #print(trie)
    return trie
def insert_nodes(trie,word,index,spots):
    """
    This function is to insert the data into the trie
    Time Complexity:Best:O(T). It needs to loop through the incoming word.
                    Worst:O(T). It needs to loop through the incoming word.
    Space Complexity:Best:O(NM). The word is the same with a word that is already in the trie
                    Worst:O(NM). The word is completely different to the words in the trie
    Error Handle:None
    :Precondition: the trie has been initialized
    :param aTrie: the tire to be inserted in
    :param word: the word to be inserted
    :param index: the index of that word in the original data
    :param spots: the number of spots a node should have
    :return: return a trie that has been inserted the word
    """
    node = trie
    for char in word:
        # O(len(word))
        pos = int(char)
        if not node[pos] == 0:
            node[spots-1].append(index)
            node = getChild(node, pos)
        else:
            node[spots - 1].append(index)
            node = createChild(node, pos, spots)
    node[spots - 2] = -1

    return trie

def insert(aTrie,word,index,spots):
    """
    This function is to insert the data into the trie
    Time Complexity:Best:O(K). It needs to loop through the incoming word.
                    Worst:O(k). It needs to loop through the incoming word.
    Space Complexity:Best:O(1). The word is the same with a word that is already in the trie
                    Worst:O(k). The word is completely different to the words in the trie
    Error Handle:None
    :Precondition: the trie has been initialized
    :param aTrie: the tire to be inserted in
    :param word: the word to be inserted
    :param index: the index of that word in the original data
    :param spots: the number of spots should a node have
    :return: return a trie that has been inserted the word
    """
    node=aTrie
    for char in word:
        #O(K)
        pos=int(char)
        if  not node[pos] == 0:
            node=getChild(node,pos)
        else:
            node=createChild(node,pos,spots)
    node[spots-1]=-1
    node.append(index)

    return aTrie

def getChild(node,pos):
    """
    This function is to get the child of the node at the corresponding place
    Time Complexity:Best:O(1)
                    Worst:O(1)
    Space Complexity:Best:O(1)
                    Worst:O(1)
    Error Handle:None
    :Precondition:the node has a child at that postion
    :param node:the node to get child from
    :param pos: the position of the child
    :return: the child node of the node at that position
    """
    return node[pos]
def createChild(node,pos,spot):
    """
    This function is to create a new child at the corresponding place
    Time Complexity:Best: O(1)
                    Worst: O(1)
    Space Complexity:Best:O(1)
                    Worst:O(1)
    Error Handle: None
    :Precondition:The node is a valid node in the trie and the position is a valid position
    :param node: the node to create child on
    :param pos: the position to create child
    :param spot: the number of spots should be in a node
    :return: the newly created child
    """
    child=[0 for i in range(spot)]
    child[spot-1]=[]
    node[pos]=child
    return child

def look_up_prefix_trie(trie,target,spots):
    """
    This function is to find all the records that contains the target prefix
    Time Complexity:Best:O(k) or O(l). Depends on the target size
                    Worst:O(k) or O(l). Depends on the target size
    Space Complexity:Best:O(1) for there is no match
                    Worst:O(n_k) or O(n_l). Depends on the length of matched records
    Error Handle: None
    :Precondition: A prefix trie that contains all the data has been generated
    :param trie: the prefix trie that has been generated
    :param target: the prefix string
    :param spots:  the total spots in a node
    :return:  return a list that contains all the indexes of the data that has the prefix
    """
    has=True
    node=trie
    for char in target:
        pos=int(char)
        if not node[pos] == 0:
            node=getChild(node,pos)
        else:
            has=False

    if has:
        return node[spots-1]
def built_suffix_trie(data):
    """
    This function is to build a suffix trie
    Time Complexity:Best:O(k^2) as it need to use every suffix in the string to construct the trie
                    Worst:O(k^2) as it need to use every suffix in the string to construct the trie
    Space Complexity:Best:O(k) for a string that is repeating a letter
                    Worst:O(k^2) for all chars in the string are identical
    Error Handle:None
    :Precondition:the string has already been split into suffixes
    :param data: the suffixes of the string
    :return: a suffix trie
    """
    trie=[0 for i in range (27)]
    for person in range (len(data)):
        #O(k*k)
        trie=insert(trie,data[person],person,27)
    #print(trie)
    return trie

def find(request,trie):
    """
    This function is to find all the inverse substrings in a string
    Time Complexity:Best:O(k) for all chars in the string are identical
                    Worst:O(k^2+p) k^2 for looking into the reverse suffix trie and compare with the string
                    p for managing the result list
    Space Complexity:Best:O(k^2) for all chars in the string are identical
                    Worst:O(K^2+p).k^2 for the suffix trie and p for the result.
    Error Handle: None
    :Precondition: A reverse suffix trie of the string has been built
    :param request: a list of the chars in the string
    :param trie: the suffix trie of the reverse string
    :return: return a list of reversing substrings and their indexes
    """
    result=[]
    current = trie
    for num in range(len(request)):
        #time: O(k*k), space:O(p)
        find_aux(result,trie,num,request,current,"",num)
    output=[]
    for ele in range (len(result)):
        #o(p)
        if len(output)==0:
            output.append(result[ele])
        else:
            if result[ele][0]==output[len(output)-1][0] and result[ele][1]==output[len(output)-1][1]:
                pass
            else:
                output.append(result[ele])

    return output

def find_aux(result,trie,index,request,current,tmp_string_for_current,pointer):
    """
    This function is to find the substring that is the same in the reverse suffix trie
    Time Complexity:Best:O(1) for no match
                    Worst:O(k) for the original string is a palindrome
    Space Complexity:Best:O(1) for no match
                    Worst:O(p) for the there is reverse substings exists in the original one
    Error Handle:None
    :Precondition: A reverse suffix trie of the string has been built
    :param result: the result list to keep the reverse substrings and their start index
    :param trie: A suffix trie of the reverse string
    :param index: the position of the current char in the string list
    :param request: a list that contains all chars in the string
    :param current: the current node in the suffix trie
    :param tmp_string_for_current: the var to hold the previous matched substrings
    :param pointer: the index of the start point of the current exploring substring
    :return:
    """
    if len(request)==index:
        if len(tmp_string_for_current) > 1:
            result.append([tmp_string_for_current, pointer])
        return
    currentRequestInt=request[index]
    if current[currentRequestInt] == 0 :
        if len(tmp_string_for_current) > 1:
            result.append([tmp_string_for_current, pointer])
        return
    else:
        #time:O(k) space:O(p)
        tmp_string_for_current += transferToLetter(currentRequestInt)
        if len(tmp_string_for_current) > 1:
            if len(result)==0:
                result.append([tmp_string_for_current, pointer])
            elif result[len(result)-2][0]!= tmp_string_for_current:
                result.append([tmp_string_for_current, pointer])
        current = getChild(current, currentRequestInt)
        find_aux(result,trie,index+1,request,current,tmp_string_for_current,pointer)

def reverseSubstrings(filename):
    """
    This function is to find all the substrings and indexes that have a reverse one in the string
    Time Complexity:Best: O(k) for no reverse substrings in the string
                    Worst:O(k^2+p) for the string is repeating one letter.i.e: all of them are inverse of each other
    Space Complexity:Best:O(k+p) for the string is repeating one letter,so the tire would take O(k) and result is O(p)
                    Worst:O(k^2+p) for all the letters in the string are identical
    Error Handle: return empty list for an empty string
    :Precondition:The function needs to take an existing file as parameter
    :param filename: The file to be read
    :return: return a list of reversing substrings and their indexes
    """
    output=[]
    file = open(filename, "r")
    data = file.read()
    if len(data) == 0:
    # in case it's an empty file
        return output

    string=[]
    for i in range (len(data)-1,-1,-1):
        #O(k)
        string.append(transferToNum(data[i]))

    request=[]
    for i in range(len(string) - 1, -1, -1):
        #O(k)
        request.append(string[i])

    suffix = []
    for i in range (len(string)):
        #space:O(k^2),time:O(k)
        current=string[i:]
        suffix.append(current)
    suffix.pop()
    #o(k^2)
    trie=built_suffix_trie(suffix)
    #time O(k^2+p), space O(p)
    output=find(request,trie)
    #print(output)
    return output

if __name__=="__main__":
    print("TASK-1:")
    print("--------------------------------------------")
    file=input("Enter the name of the query database: ")
    id=input("Enter the prefix of the identification number: ")
    lastName=input("Enter the prefix of the last name: ")
    try:
        result=query(file,id,lastName)
        print(str(len(result))+" record found")
        for i in result:
            print("Index number:"+str(i))
    except:
        print("Invalid file name or the identification number is not a number or last name consists other things than letters")
    print("---------------------------------------------")
    print("TASK2:")
    fileName=input("Enter the file name for searching reverse substring: ")
    try:
        data=reverseSubstrings(fileName)
        output=""
        for i in range (len(data)-1):
            output+=data[i][0]+"("+str(data[i][1])+"), "
        output+=data[len(data)-1][0]+"("+str(data[len(data)-1][1])+")"
        print(output)
    except:
        print("Invalid file name")
    #reverseSubstrings("string.txt")
