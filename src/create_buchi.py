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

# @staticmethod
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
    ret = []
    for i in list:
        if i not in ret:
            ret.append(i)
    return ret

formula = old_formula.Read_formula.formula
Alph_s = Alph.Alphs_set.Alph_s

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
    # print(str(counter) + " " + line)
    # counter = counter + 1
    if is_title(line):
        title = get_title(line)
    elif is_node(line):
        name, label, accepting  = get_node(line)  # the third value is boolean based on if it has "accepting" as prefix
        # print(name +  " " + label + " " + str(accepting))
        S_names.append(name)
        src_node = name
        # print(label)
        node_counter = node_counter + 1
    elif is_edge(line):
        assert src_node is not None
        dst_node, label = get_edge(line)
        edges.append((node_counter,label))
        dst_nodes.append(dst_node)

        # print(dst_node)
        # print(label)
    elif is_skip(line):
        assert src_node is not None
    elif is_ignore(line):
        pass
    # else:
        # print("--{}--".format(line))
        # raise ValueError("{}: invalid input:\n{}")

states_no = len(S_names) # no . of state
# print(S_names)
B_S = np.arange(0,states_no) # numeric indices for states
B_S0 = [True if re.search("init", i) else False for i in S_names]
for counter,i in enumerate(B_S0):
    if i == True:
        B_S0 = counter
B_F = [True if re.search("accept",i) else False for i in S_names]
for counter,i in enumerate(B_F):
    if i == True:
        B_F = counter

 # a multidimensional list containning labels - shape = (states_np,states_no)
B_trans = [[[] for i in range(len(S_names))] for i in range(len(S_names))]
B_trans[0][0] = "Hey, I should be in the first block"
# print(edges)
for i in range(states_no):
    if i != states_no:
        str = output

Edges_no = len(edges)
# print(edges)

# ONLY {& (and), ! (not), 1 (any=True)} can appear on each row with respect to propositions (|| (OR) operator results in 2 rows)
# if 1 appears, it is the first element and there is no atomic proposition on current row
# print(B_S)

counter = 0
# n is i and transition state is our k
for n,edge in edges: # n represents the node counter
    transiting_to_state = dst_nodes[counter]
    counter = counter + 1
    # print(transiting_to_state)
    for index,j in enumerate(S_names):
        if(transiting_to_state == j):
            column_index = index
    # print(edge)
    # look_for_ap = re.compile('(([p]+\d+)+)')
    look_for_ap = re.findall('([!p]+\d+)',edge) # normal
    # look_for_ap_wo_not = re.findall('([p]+\d+)', edge) # without the ! sign
    # lets remove strings(ap) that are repeated
    p = remove_redundancy_from_list(look_for_ap)
    # print(p)
    # label = sig
    labels = []
    look_for_not_ap = re.compile('^!')
    # for i in p:
    #     tmp = look_for_not_ap.search(i)
    #     print(tmp)

    for i in p:
        label = []
        if True if look_for_not_ap.search(i) else False:
            # print("Found a negative Ap")
            i = re.sub("!","",i)
            for counter,elements in enumerate(Alph_s):
                if elements.find(i) == -1:
                    label.append(counter)
        else:
            for counter,elements in enumerate(Alph_s):
                if elements.find(i) != -1:
                    label.append(counter)
            # label = sig
        labels.append(label)
        print(label)
        print("**********************************************")
