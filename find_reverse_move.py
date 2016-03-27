def exchange(s): 
    dic = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'} 
    seq = list(s) 
    seq = [dic[move] for move in seq] 
    return ''.join(seq)

def reverse(s):
    return exchange(s[::-1])

print reverse("rdldurldurdluurddluurddluurdlrldrulurdld")
