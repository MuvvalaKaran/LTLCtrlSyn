import src.read_formula as old_formula
from graphviz.dot import Digraph
import src.alphabet_set as Alph
from subprocess import Popen,PIPE
import numpy as np
import re
import sys
import os

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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
print(output)

s_ind = [m.start() for m in re.finditer('T0_S7', output)]
print(s_ind)

class Graph:
    def __init__(self):
        self.dot = Digraph()

    def title(self, str):
        self.dot.graph_attr.update(label=str)

    def node(self, name, label, accepting=False):
        num_peripheries = '2' if accepting else '1'
        self.dot.node(name, label, shape='circle', peripheries=num_peripheries)

    def edge(self, src, dst, label):
        self.dot.edge(src, dst, label)

    def show(self):
        self.dot.render(view=True)

    def save_render(self, path, on_screen):
        self.dot.render(path, view=on_screen)

    def save_dot(self, path):
        self.dot.save(path)

    def __str__(self):
        return str(self.dot)

class Ltl2baParser:
    prog_title = re.compile('^never\s+{\s+/\* (.+?) \*/$')
    prog_node = re.compile('^([^_]+?)_([^_]+?):$')
    prog_edge = re.compile('^\s+:: (.+?) -> goto (.+?)$')
    prog_skip = re.compile('^\s+(?:skip)$')
    prog_ignore = re.compile('(?:^\s+do)|(?:^\s+if)|(?:^\s+od)|'
                             '(?:^\s+fi)|(?:})|(?:^\s+false);?$')

    @staticmethod
    def parse(ltl2ba_output, ignore_title=True):
        graph = Graph()
        src_node = None
        for line in ltl2ba_output.split('\n'):
            if Ltl2baParser.is_title(line):
                title = Ltl2baParser.get_title(line)
                if not ignore_title:
                    graph.title(title)
            elif Ltl2baParser.is_node(line):
                name, label, accepting = Ltl2baParser.get_node(line)
                graph.node(name, label, accepting)
                src_node = name
            elif Ltl2baParser.is_edge(line):
                dst_node, label = Ltl2baParser.get_edge(line)
                assert src_node is not None
                graph.edge(src_node, dst_node, label)
            elif Ltl2baParser.is_skip(line):
                assert src_node is not None
                graph.edge(src_node, src_node, "(1)")
            elif Ltl2baParser.is_ignore(line):
                pass
            else:
                print("--{}--".format(line))
                raise ValueError("{}: invalid input:\n{}".format(Ltl2baParser.__name__, line))

        return graph

    @staticmethod
    def is_title(line):
        return Ltl2baParser.prog_title.match(line) is not None

    @staticmethod
    def get_title(line):
        assert Ltl2baParser.is_title(line)
        return Ltl2baParser.prog_title.search(line).group(1)

    @staticmethod
    def is_node(line):
        return Ltl2baParser.prog_node.match(line) is not None

    @staticmethod
    def get_node(line):
        assert Ltl2baParser.is_node(line)
        prefix, label = Ltl2baParser.prog_node.search(line).groups()
        return (prefix + "_" + label, label,
                True if prefix == "accept" else False)

    @staticmethod
    def is_edge(line):
        return Ltl2baParser.prog_edge.match(line) is not None

    @staticmethod
    def get_edge(line):
        assert Ltl2baParser.is_edge(line)
        label, dst_node = Ltl2baParser.prog_edge.search(line).groups()
        return (dst_node, label)

    @staticmethod
    def is_skip(line):
        return Ltl2baParser.prog_skip.match(line) is not None

    @staticmethod
    def is_ignore(line):
        return Ltl2baParser.prog_ignore.match(line) is not None

