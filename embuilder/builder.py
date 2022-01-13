import yaml
from rdflib import BNode

class EMB():
    def __init__(self, config):
      self.config = config

    def transform(self,prefixes,triplets):
      self.prefixes = prefixes
      self.triplets = triplets
      self.main_dict = dict()

      # prefixes object:
      prefixes_dict = dict(prefixes=self.prefixes) # create prefixes object
      self.main_dict.update(prefixes_dict) # append prefixes object into main

      # sources object:
      sources_dict = dict(sources= dict(
                            source_prov=dict(
                              access = str("|||DATA|||"),
                              referenceFormulation= str("|||FORMULATION|||"),
                              iterator = str("$"))))
      sources_dict["sources"][self.config["source_name"]] = sources_dict["sources"].pop("source_prov") # rename source_name using an unique name from config
      self.main_dict.update(sources_dict)

      # mapping object:
      mapping_dict = dict(mapping = dict())
      for e in self.triplets:
          triplet_map = dict(name_node = dict(
                              sources = [self.config["source_name"]],  # SOURCE
                              subjects = e[0], # SUBJECT
                              predicateobject = [dict(
                                  predicate = e[1], # PREDICATE
                                  objects = dict(
                                      value = e [2], # OBJECT
                                      datatype = e[3]))]))  # OBJECT'S TYPE

          triplet_map[str(BNode())] = triplet_map.pop("name_node") # rename name_mode using an unique name per node
          mapping_dict["mapping"].update(triplet_map) # append dict into dict
          
      self.main_dict.update(mapping_dict) # append mapping object into main

      # dump
      document = yaml.dump(self.main_dict)
      return document