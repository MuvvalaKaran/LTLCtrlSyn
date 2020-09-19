import src.read_formula as old_formula
import src.alphabet_set as Alph
from subprocess import Popen, PIPE
import numpy as np
import re
import sys


def is_title(line):
    return CreateBuchi.prog_title.match(line) is not None

def get_title(line):
    assert is_title(line)
    return CreateBuchi.prog_title.search(line).group(1)

def is_node(line):
    return CreateBuchi.prog_node.match(line) is not None

def get_node(line):
    assert is_node(line)
    prefix, label = CreateBuchi.prog_node.search(line).groups()
    return (prefix + "_" + label, label,
            True if prefix == "accept" else False)

def is_edge(line):
    return CreateBuchi.prog_edge.match(line) is not None

def get_edge(line):
    assert is_edge(line)
    label, dst_node = CreateBuchi.prog_edge.search(line).groups()
    return (dst_node, label)

def is_skip(line):
    return CreateBuchi.prog_skip.match(line) is not None

def is_ignore(line):
    return CreateBuchi.prog_ignore.match(line) is not None
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


class CreateBuchi(object):

    prog_title = re.compile('^never\s+{\s+/\* (.+?) \*/$')
    prog_node = re.compile('^([^_]+?)_([^_]+?):$')
    prog_edge = re.compile('^\s+:: (.+?) -> goto (.+?)$')
    prog_skip = re.compile('^\s+(?:skip)$')
    prog_ignore = re.compile('(?:^\s+do)|(?:^\s+if)|(?:^\s+od)|'
                             '(?:^\s+fi)|(?:})|(?:^\s+false);?$')

    def __init__(self, formula, alphabet_set):
        self.formula = formula
        self.alphabet_set = alphabet_set

    def createbuchi(self):

        # formula = old_formula.Read_formula.formula
        # Alph_s = Alph.Alphs_set.Alph_s

        formula = self.formula
        Alph_s = self.alphabet_set

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

        # print(formula)
        full_descrition = True

        if full_descrition:
            try:
                ltl2ba_args = ["src/ltl2ba/ltl2ba","-d", "-f", formula]
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

            # prog_title = re.compile('^Buchi automaton before simplification')
            # prog_title = re.compile("(Buchi automaton after simplification\w)")
            # prog_title1 = re.search("Buchi automaton after simplification",output)
            # prog_title2 = re.search("never {",output)
            # print(prog_title1.span())

            prog_src_node = re.compile("^state (\S*)")
            # prog_edges = re.findall("->")
            sig = np.arange(0, len(Alph_s))
            # y = re.findall("Buchi automaton before simplification", output)
            tmp = []
            match = False
            for line in output.split("\n"):
                # if prog_title.match(line):
                if re.search("^Buchi automaton after simplification",line):
                    match = True
                if(match):
                    tmp.append(line)

            new_output = []
            for counter,i in enumerate(tmp):
                if len(i) == 0:
                    break
                new_output.append(i)
                # print(new_output[counter])
            new_output.pop(0)

            src_nodes = []
            edges = []
            node_counter = -1
            for line in new_output:
                if prog_src_node.match(line) is not None:
                    src_node = prog_src_node.search(line)
                    src_nodes.append(src_node.group(1))
                    node_counter = node_counter + 1
                elif re.search("->",line) is not None:
                    edges.append((node_counter,line))



            # print(src_nodes)
            # print(edges)

            S_names = src_nodes
            states_no = len(S_names)
            B_S = np.arange(0, states_no)  # numeric indices for states
            B_S0 = [True if re.search("init", i) else False for i in S_names]
            for counter, i in enumerate(B_S0):
                if i == True:
                    B_S0 = counter
            tmp_B_F = [True if re.search("^accept", i) else False for i in S_names]  # careful it is actually accept_0

            B_F = []
            for counter, i in enumerate(tmp_B_F):
                if i == True:
                    # B_F = counter
                    B_F.append(counter)
            if isinstance(B_F, type(None)):
                B_F = B_S0

            # print(B_S)
            # print(B_S0)
            # print(B_F)
            # a multidimensional list containning labels - shape = (states_np,states_no)
            B_trans1 = [[[] for i in range(len(S_names))] for i in range(len(S_names))]

            for i in range(states_no):
                edges_of_the_node = []
                for tmp_node_counter,edge in edges:
                    if tmp_node_counter == i: # all 0s and then 1s and so on
                        edges_of_the_node.append(edge)

                # print(edges_of_the_node)
                # for row in edges_of_the_node:
                for j in range(len(edges_of_the_node)):
                    row = edges_of_the_node[j]

                    k = re.search("-> (\S*)",row)
                    tmp_dst_node = k.group(1)

                    for match_index,names in enumerate(S_names):
                        if names == tmp_dst_node:
                            k = match_index
                            break
                    if row[0] == '1':
                        B_trans1[i][k] = sig.tolist()
                        continue

                    # prop = re.search("(\S*) ->",row)
                    # prop = re.search("(?<!-)\S*",row)
                    prop = re.findall("(?<!-)\S*\s",row)
                    prop = [ap.replace(" ", "") for ap in prop]
                    for counter,pr in enumerate(prop):
                        if pr == "&" or pr == "->":
                            prop.pop(counter)

                    labels = []
                    direct = False
                    indirect = False
                    for ap in prop:
                        if re.search('^p',ap) is None and re.search('^!',ap) is None:
                            labels.append(sig.tolist())
                            direct = True
                            continue
                        # listOfLabels = []
                        subLabel = []
                        if re.search('^!',ap) or re.search('^p',ap):
                            # subLabel = []
                            if re.search('^!',ap):
                                ap = re.sub("!", "", ap)
                                if len(ap) > 4:
                                    ap = ap[0] + ap[2:3]
                                # labels = set.intersection(*map(set,labels))
                                indirect = True
                                for counter, elements in enumerate(Alph_s):
                                    if elements.find(ap) == -1:
                                        subLabel.append(counter)
                            elif re.search('^p',ap):
                                if len(ap) > 3:
                                    ap = ap[0] + ap[2:3]
                                indirect = True
                                for counter,elements in enumerate(Alph_s):
                                    if elements.find(ap) != -1:
                                        subLabel.append(counter)
                            # listOfLabels.append(subLabel)
                        labels.append(subLabel)
                    if not direct or indirect:
                        labels = list(set.intersection(*map(set,labels)))
                        indirect = False
                    else:
                        direct = False
                        labels = labels[0]

                    B_trans1[i][k] = list(set(B_trans1[i][k]).union(set(labels)))

            for i in range(len(S_names)):
                for j in range(len(S_names)):
                    B_trans1[i][j].sort()

        else:
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

            # s_ind = [m.start() for m in re.finditer('T0_S7', output)]
            # print(s_ind)

            # regex core
            # prog_title = re.compile('^never\s+{\s+/\* (.+?) \*/$')
            # prog_node = re.compile('^([^_]+?)_([^_]+?):$')
            # prog_edge = re.compile('^\s+:: (.+?) -> goto (.+?)$')
            # prog_skip = re.compile('^\s+(?:skip)$')
            # prog_ignore = re.compile('(?:^\s+do)|(?:^\s+if)|(?:^\s+od)|'
            #                          '(?:^\s+fi)|(?:})|(?:^\s+false);?$')

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

            tmp_B_F = [True if re.search("accept",i) else False for i in S_names]
            B_F = []
            for counter,i in enumerate(tmp_B_F):
                if i == True:
                    B_F.append(counter)

            if isinstance(B_F, type(None)):
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
                            # size_of_sub_string = len(part)
                            look_for_ap = re.findall('([!p]+\d+)',part)
                            for ap in look_for_ap:
                                subLabel = []
                                if True if look_for_not_ap.search(ap) else False:
                                    ap = re.sub("!", "", ap)
                                    if len(ap) == 4:
                                        ap = ap[0] + ap[2:]
                                    for counter, elements in enumerate(Alph_s):
                                        if elements.find(ap) == -1:
                                            subLabel.append(counter)
                                else:
                                    if len(ap) == 4:
                                        ap = ap[0] + ap[2:]
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
                            label = []
                            if True if look_for_not_ap.search(i) else False:
                                i = re.sub("!", "", i)
                                if len(i) == 4:
                                    i = i[0] + i[2:]
                                for counter,elements in enumerate(Alph_s):
                                    if elements.find(i) == -1:
                                        label.append(counter)
                            else:
                                if len(i) == 4:
                                    i = i[0] + i[2:]
                                for counter,elements in enumerate(Alph_s):
                                    if elements.find(i) != -1:
                                        label.append(counter)
                            #insert that label to i,j B_trans
                            labels.append(label)
                        B_trans[int(n)][int(column_index)] = list(set.intersection(*map(set,labels)))
                else:
                    B_trans[int(n)][int(column_index)] = list(sig)
            B_trans[len(S_names)-1][len(S_names)-1] = list(sig) #the accepting state will always have a self transition

            for i in range(len(S_names)):
                for j in range(len(S_names)):
                    B_trans[i][j].sort()

        # storing by default b_trains1 value. Declare it up
        B = {
            "B.S": B_S,
            "B.S0": B_S0,
            "B.F": B_F,
            "B.trans": B_trans1
        }

        return B
        # print("hmmm")
        # yay = B_trans[0][1]
        # print(yay)