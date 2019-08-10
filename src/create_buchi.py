import src.read_formula as old_formula
from graphviz.dot import Digraph
import src.alphabet_set as Alph
from subprocess import Popen,PIPE
import numpy as np
import re
import sys
import os

def is_title(line):
    return prog_title.match(line) is not None

def get_title(line):
    assert is_title(line)
    return prog_title.search(line).group(1)

def is_node(line):
    return prog_node.match(line) is not None

def get_node(line):
    assert is_node(line)
    prefix, label = prog_node.search(line).groups()
    return (prefix + "_" + label, label,
            True if prefix == "accept" else False)

def is_edge(line):
    return prog_edge.match(line) is not None

def get_edge(line):
    assert is_edge(line)
    label, dst_node = prog_edge.search(line).groups()
    return (dst_node, label)

def is_skip(line):
    return prog_skip.match(line) is not None

def is_ignore(line):
    return prog_ignore.match(line) is not None
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def remove_redundancy_from_list(list):
    newlist = [ii for n, ii in enumerate(list) if ii not in list[:n]]
    return newlist

def addinglistwithoutredundancy(list):
    list_size = len(list)
    new_list = list[0]
    for i in range(list_size - 1):
        list_two = set(list[i+1])
        new_list.extend(y for y in list_two if y in new_list)
    return new_list

def unionoflists(list):
    list_size = len(list)
    new_list = list[0]
    for i in range(list_size - 1):
        list_two = set(list[i+1])
        new_list.extend(y for y in list_two if y not in new_list)
    return new_list

formula = old_formula.Read_formula.formula
Alph_s = Alph.Alphs_set.Alph_s

#ltl2ba produces p010 instead of p10 so need to make tmp change to the ALph_s set
# new_Alph_s = []
# for word in Alph_s:
#     word = re.sub("p10","p010",word)
#     new_Alph_s.append(word)




formula = re.sub('&','&&',formula)
formula = re.sub('\|','||',formula)
formula = re.sub('R','V',formula)
formula = re.sub('F','<>',formula)
formula = re.sub('G','[]',formula)

try:
    ltl2ba_args = ["ltl2ba/ltl2ba", "-f", formula]
    process = Popen(ltl2ba_args, stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

except FileNotFoundError as e:
    eprint("{}: ltl2ba not found.\n")
    eprint("Please download ltl2ba from\n")
    eprint("\thttp://www.lsv.fr/~gastin/ltl2ba/ltl2ba-1.2b1.tar.gz\n")
    eprint("compile the sources and add the binary to your $PATH, e.g.\n")
    eprint("\t~$ export PATH=$PATH:path-to-ltlb2ba-dir\n")
    eprint("or create a directory inside src of compiled ltl2ba version \n")
    sys.exit(1)

output = output.decode('utf-8')
# print(output)

sig = np.arange(0,len(Alph_s))
str1 = "Buchi automaton after simplification"
str2 = "never {"

output = output.replace(str1,"")
output = output.replace(str2,"")
# print(output)

s_ind = [m.start() for m in re.finditer('T0_S7', output)]
# print(s_ind)

# regex core
prog_title = re.compile('^never\s+{\s+/\* (.+?) \*/$')
prog_node = re.compile('^([^_]+?)_([^_]+?):$')
prog_edge = re.compile('^\s+:: (.+?) -> goto (.+?)$')
prog_skip = re.compile('^\s+(?:skip)$')
prog_ignore = re.compile('(?:^\s+do)|(?:^\s+if)|(?:^\s+od)|'
                         '(?:^\s+fi)|(?:})|(?:^\s+false);?$')

S_names = [] # they are all the source nodes
dst_nodes = []
edges = []
src_node = None
node_counter = -1
for line in output.split("\n"):

    if is_title(line):
        title = get_title(line)
    elif is_node(line):
        name, label, accepting  = get_node(line)  # the third value is boolean based on if it has "accepting" as prefix
        S_names.append(name)
        src_node = name
        node_counter = node_counter + 1
    elif is_edge(line):
        assert src_node is not None
        dst_node, label = get_edge(line)
        edges.append((node_counter,label))
        dst_nodes.append(dst_node)
    elif is_skip(line):
        assert src_node is not None
    elif is_ignore(line):
        pass

states_no = len(S_names) # no . of state

B_S = np.arange(0,states_no) # numeric indices for states
B_S0 = [True if re.search("init", i) else False for i in S_names]
for counter,i in enumerate(B_S0):
    if i == True:
        B_S0 = counter
B_F = [True if re.search("accept",i) else False for i in S_names]
for counter,i in enumerate(B_F):
    if i == True:
        B_F = counter

if len(B_F) == 0:
    B_F = B_S0

 # a multidimensional list containning labels - shape = (states_np,states_no)
B_trans = [[[] for i in range(len(S_names))] for i in range(len(S_names))]

for i in range(states_no):
    if i != states_no:
        str = output

Edges_no = len(edges)

# ONLY {& (and), ! (not), 1 (any=True)} can appear on each row with respect to propositions (|| (OR) operator results in 2 rows)
# if 1 appears, it is the first element and there is no atomic proposition on current row
# print(B_S)
counter_for_ORs = 0
counter_dst_nodes = 0

for n,edge in edges: # n represents the node counter
    transiting_to_state = dst_nodes[counter_dst_nodes]
    counter_dst_nodes = counter_dst_nodes + 1
    for index,j in enumerate(S_names):
        if(transiting_to_state == j):
            column_index = index
            break
    if edge != '(1)':
        look_for_ap = re.findall('([!p]+\d+)',edge) # normal
        look_for_not_ap = re.compile('^!')
        look_for_ORs = edge.split(" || ")

        if(len(look_for_ORs) > 1):
            part_Label = []
            for part in look_for_ORs:
                labels = []
                size_of_sub_string = len(part)
                look_for_ap = re.findall('([!p]+\d+)',part)

                for ap in look_for_ap:
                    if len(ap) == 4:
                        ap = ap[0] + ap[2:]
                    subLabel = []
                    if True if look_for_not_ap.search(ap) else False:
                        ap = re.sub("!","",ap)
                        for counter, elements in enumerate(Alph_s):
                            if elements.find(ap) == -1:
                                subLabel.append(counter)
                    else:
                        for counter, elements in enumerate(Alph_s):
                            if elements.find(ap) != -1:
                                subLabel.append(counter)
                    labels.append(subLabel)

                labels = set.intersection(*map(set,labels))
                part_Label.append(list(labels))

            part_Label = unionoflists(part_Label)
            B_trans[int(n)][int(column_index)] = part_Label

        else:
            labels = []
            for i in look_for_ap:
                if len(i) == 4:
                     i = i[0] + i[2:]
                label = []
                if True if look_for_not_ap.search(i) else False:

                    i = re.sub("!","",i)
                    for counter,elements in enumerate(Alph_s):
                        if elements.find(i) == -1:
                            label.append(counter)
                else:
                    for counter,elements in enumerate(Alph_s):
                        if elements.find(i) != -1:
                            label.append(counter)
                #insert that label to i,j B_trans
                labels.append(label)
            B_trans[int(n)][int(column_index)] = list(set.intersection(*map(set,labels)))
    else:
        B_trans[int(n)][int(column_index)] = list(sig)
B_trans[len(S_names)-1][len(S_names)-1] = list(sig) #the accepting state will always have a self transition
