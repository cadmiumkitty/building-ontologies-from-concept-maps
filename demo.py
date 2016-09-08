# -*- coding: utf-8 -*-
""" 
demo.py Semantic Web London Demo
"""

import csv
import sys
import re

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, OWL, NamespaceManager

def is_class_case(s):
    return re.search('[A-Z]', s)
    
def to_class_case(s):
    elements = s.split(' ')
    return "".join(e.title() for e in elements)

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

PRODUCT = Namespace('http://www.example.com/ontologies/product/')

namespace_manager = NamespaceManager(Graph())
namespace_manager.bind('product', PRODUCT, override = False)
namespace_manager.bind('owl', OWL, override = False)

graph = Graph()
graph.namespace_manager = namespace_manager

input_file = open(input_file_name, 'r')
reader = csv.reader(input_file, delimiter='\t')

for line in reader:

    subject = line[0]
    predicate = line[1]
    object = line[2]
    
    if is_class_case(subject):
        graph.set( (PRODUCT[to_class_case(subject)], RDF.type, OWL.Class) )

    if is_class_case(object):
        graph.set( (PRODUCT[to_class_case(object)], RDF.type, OWL.Class) )

    if is_class_case(object) and predicate in ['is a', 'is an']:
        graph.set( (PRODUCT[to_class_case(subject)], RDFS.subClassOf, PRODUCT[to_class_case(object)]) )

ttl = graph.serialize(format = 'turtle', indent = 4)

output_file = open(output_file_name, "w")
output_file.write(ttl.decode("utf-8"))