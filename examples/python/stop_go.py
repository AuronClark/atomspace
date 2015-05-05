#! /usr/bin/env python
#
# stop_go.py
#
"""
Example of how to use the pattern matcher to callback into Python.
"""

from opencog.atomspace import AtomSpace, TruthValue, types, get_type_name
from opencog.scheme_wrapper import load_scm, scheme_eval, scheme_eval_h, __init__


green = 0
red = 0

def initialize_counts():
    global red
    global green
    green = 0
    red = 0

def increment_green():
    global green
    green += 1
    print "green light"

def increment_red():
    global red
    red += 1
    print "red light"



atomspace = AtomSpace()
__init__(atomspace)

data = ["opencog/atomspace/core_types.scm",
        "opencog/scm/utilities.scm"]

for item in data:
    load_scm(atomspace, item)

# Define several animals and something of a different type as well
scheme_animals = \
    '''
    (InheritanceLink (ConceptNode "Frog") (ConceptNode "animal"))
    (InheritanceLink (ConceptNode "Zebra") (ConceptNode "animal"))
    (InheritanceLink (ConceptNode "Deer") (ConceptNode "animal"))
    (InheritanceLink (ConceptNode "Spaceship") (ConceptNode "machine"))
    '''
scheme_eval_h(atomspace, scheme_animals)

# Define a graph search query
scheme_query = \
    '''
    (define find-animals
      (BindLink
        ;; The variable to be bound
        (VariableNode "$var")
        (ImplicationLink
          ;; The pattern to be searched for
          (InheritanceLink
             (VariableNode "$var")
             (ConceptNode "animal")
          )

          ;; The value to be returned.
          (VariableNode "$var")
        )
      )
    )
    '''
scheme_eval_h(atomspace, scheme_query)

# Run the above pattern and print the result
result = scheme_eval_h(atomspace, '(cog-bind find-animals)')
print "The result of pattern matching is:\n\n" + str(atomspace[result])