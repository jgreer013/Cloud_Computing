#!/usr/bin/env python

from classDict import buildClassDict
import itertools

# Takes in list of string classNames, outputs a list of all combinations of their sections
# str['className','className',...] -> str[['section','combination'],['section','combination']]
def comb(class_list, classes):
  sections = []
  for clss in class_list:
    sections.append(classes[clss])
  print sections
  return list(itertools.product(*sections)) # Praise itertools for he is good, that my coding may be product-ive

# Takes in a list of classNames and a list of sections, outputs a list of all combinations of their sections
# In the event the student has specific required classes and wishes to find all schedule options based on those constraints
# str['className','className',...], str['section','section'] -> str[['section','combination'],['section','combination']]
def combWithSections(class_list, section_list, classes):
  sections = []
  for sect in section_list:
    sections.append([sect])
  for clss in class_list:
    sections.append(classes[clss])
  return list(itertools.product(*sections))
