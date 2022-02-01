import yaml
import sys
from pyperseo.functions import milisec


class EMB():
    def __init__(self, config):
      self.config = config

    def transform(self,prefixes,triplets):
      self.prefixes = prefixes
      self.triplets = triplets
      self.main_dict = dict()

      # prefixes object:
      if self.config["configuration"] == "ejp":
        prefixes_dict = dict(prefixes=self.prefixes) # create prefixes object
        prefixes_dict["prefixes"]["this"] = str("|||BASE|||")
        self.main_dict.update(prefixes_dict) # append prefixes object into main
      elif self.config["configuration"] == "csv":
        prefixes_dict = dict(prefixes=self.prefixes) # create prefixes object
        self.main_dict.update(prefixes_dict) # append prefixes object into main
      else:
        sys.exit('You must provide a configuration parameter: use "ejp" for using this template for EJP-RDs workflow, or "csv" for defining CSV data source')
    

      # sources object:
      if self.config["configuration"] == "ejp":
        sources_dict = dict(sources= dict(
                              source_prov=dict(
                                access = str("|||DATA|||"),
                                referenceFormulation= str("|||FORMULATION|||"),
                                iterator = str("$"))))
        sources_dict["sources"][self.config["source_name"]] = sources_dict["sources"].pop("source_prov") # rename source_name using an unique name from config
        self.main_dict.update(sources_dict)
      elif self.config["configuration"] == "csv":
        if "csv_name" in self.config:
          sources_dict = dict(sources= dict(
                                source_prov=dict(
                                  access = self.config["csv_name"]+ ".csv",
                                  referenceFormulation= "csv",
                                  iterator = str("$"))))
          sources_dict["sources"][self.config["source_name"]] = sources_dict["sources"].pop("source_prov") # rename source_name using an unique name from config
          self.main_dict.update(sources_dict)
        else:
          sys.exit('You must provide a csv_name parameter for defining the name of your CSV data source')

      else:
        sys.exit('You must provide a configuration parameter: use "ejp" for using this template for EJP-RDs workflow, or "csv" for defining CSV data source')
    
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

          stamp = milisec() + "_" + self.config["source_name"] # Creating a unique name for each object using timestamp and source_name 
          if e[3] == "iri":
            triplet_map["name_node"]["predicateobject"][0]["objects"]["type"] = triplet_map["name_node"]["predicateobject"][0]["objects"].pop("datatype") # rename name_mode using an unique name per node

          triplet_map[stamp] = triplet_map.pop("name_node") # rename name_mode using an unique name per node
          mapping_dict["mapping"].update(triplet_map) # append dict into dict
          
      self.main_dict.update(mapping_dict) # append mapping object into main

      # dump
      document = yaml.dump(self.main_dict)
      return document