import yaml
import sys
from pyperseo.functions import milisec


class EMB():
    def __init__(self, config, prefixes, triplets):
        self.config = config
        self.prefixes = prefixes
        self.triplets = triplets
        self.main_dict = dict()
        self.tree = dict()

        # Check all objects are fine:
        if not isinstance(config and prefixes, dict):
            sys.exit("Both configuration and prefixes objects must be a dictionary. Please, check your input objects")
        if not isinstance(triplets, list):
            sys.exit("Triplets objects must be a list. Please, check your input objects")
        for i in self.triplets:
            if not len(i) == 4:
                sys.exit("Triplet object must be formed by four string based list [subject, predicate, object, datatype]. Please, check your input objects")

    
    def structured_quads(self, data):
        """
        Input: List of lists of quadruplets: [[s p o d], [s p o d], ...]
        Transform your input into tree-based triplets organized by common Subject. For example: s[pod],[pod]
        Output: self.tree() with your new structured quadruplets
        """
        if type(data) is not list:
            sys.exit("You must provide a list of lists with your quadruplets inside: [[s p o d], [s p o d], ...]")
        else:
            for quad in data:
                s, p, o ,d = quad
                if not s in self.tree.keys():
                    map = dict()
                    map.update({s:[[p,o,d]]}) 
                    self.tree.update(map)
                else:
                    po = [p,o,d] 
                    self.tree[s].append(po)
            return self.tree

    def transform_YARRRML(self):
        """
        Transform your input triplets, prefixes into YARRRML based on your configuration input dictionary.
        """
        self.tree = dict() # Reset tree object

        # prefixes object:
        if self.config["configuration"] == "ejp":
            prefixes_dict = dict(prefixes=self.prefixes) # create prefixes object
            prefixes_dict["prefixes"]["this"] = str("|||BASE|||")
            self.main_dict.update(prefixes_dict) # append prefixes object into main
        elif self.config["configuration"] == "default":
            prefixes_dict = dict(prefixes=self.prefixes) # create prefixes object
            self.main_dict.update(prefixes_dict) # append prefixes object into main
        else:
            sys.exit('You must provide a configuration parameter: use "ejp" for using this template for EJP-RDs workflow, or "default" for defining CSV data source')

        # sources object:
        if self.config["configuration"] == "ejp":
            sources_dict = dict(sources= dict(
                                    source_prov=dict(
                                    access = str("|||DATA|||"),
                                    referenceFormulation= str("|||FORMULATION|||"),
                                    iterator = str("$"))))
            sources_dict["sources"][self.config["source_name"]] = sources_dict["sources"].pop("source_prov") # rename source_name using an unique name from config
            self.main_dict.update(sources_dict)
        elif self.config["configuration"] == "default":
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
            sys.exit('You must provide a configuration parameter: use "ejp" for using this template for EJP-RDs workflow, or "default" for defining CSV data source')

        # mapping object:
        self.tree = self.structured_quads(self.triplets)

        mapping_dict = dict(mapping = dict())
        for t in self.tree.items():
            s_mapp = dict(name_node = dict(
                            sources = [self.config["source_name"]], # SOURCE
                            subjects = t[0], # SUBJECT
                            predicateobject = []))
            for l in t[1]:
                if l[2] == "iri":
                    pod_map = dict(
                                predicate = l[0], # PREDICATE
                                objects = dict(
                                    value = l[1], # OBJECT
                                    type = l[2])) # DATATYPE
                else:
                    pod_map = dict(
                                predicate = l[0], # PREDICATE
                                objects = dict(
                                    value = l[1], # OBJECT
                                    datatype = l[2])) # DATATYPE

                s_mapp["name_node"]["predicateobject"].append(pod_map)
                
            stamp = milisec() + "_" + self.config["source_name"] # Creating a unique name for each object using timestamp and source_name 
            s_mapp[stamp] = s_mapp.pop("name_node") # rename name_mode using an unique name per node
            mapping_dict["mapping"].update(s_mapp)
        self.main_dict.update(mapping_dict) # append mapping object into main

        document = yaml.dump(self.main_dict)
        return document

    def extract_information(self, term):
        if term.startswith("$("): term = term.replace("$(","").replace(")","") # If the term is a data reference, remove the symbols
        end_of_term = term.split("}")[-1] # split the term (normally URI) in case in contain any {} reference
        end_of_term = end_of_term.split(")")[-1] # split the term (normally URI) in case in contain any $() reference
        end_of_term_list = end_of_term.split('_') # Create a list with all word from the URI
        if "" in end_of_term_list: end_of_term_list.remove("") # Remove empty words
        if len(end_of_term_list) == 0 : end_of_term_list[0] = "UndeterminedName" # In case of none, create a provisional name
        return end_of_term_list

    def transform_ShEx(self):
        """
        Transform your input triplets and prefixes into Shape Expression (ShEx) based on your configuration input dictionary.
        """
        self.triplets_curated = list()
        self.tree = dict() # Reset tree object
        self.result_ShEx = ""
        if not self.config["basicURI"]: sys.exit("basicURI parameter must to be provided at configuration input")

        # prefixes addtion:
        for k,v in self.prefixes.items():
            if not k == self.config["basicURI"]:
                prefix = "PREFIX " + k + ": <" + v + ">"
            else:
                prefix = "PREFIX " + ": <" + v + ">"

            self.result_ShEx = self.result_ShEx + prefix + "\n"

        # triplets curation:
        for quad in self.triplets:
            s,p,o,d = quad

            # SUBJECT
            if s.startswith(self.config["basicURI"] + ":" ) or s.startswith(":") or s.startswith("$("):
                # Select shape's name removing the rest of the IRI:
                s_list = self.extract_information(s)
                # Using standard to name the shape properly:
                statement = ":"
                if len(s_list) >= 2:
                    statement = statement + s_list[0].lower()
                    for sl in s_list[1:]:
                        statement = statement + sl[0].upper() + sl[1:].lower()
                    statement = statement + "Shape"
                else:
                    statement =  statement + s_list[-1].lower() + "Shape"
                s_curated = statement

            elif s.startswith("http"): # Right syntax in case of IRI
                s_curated = "<" + s + ">"
            else:
                s_curated = s

            # PREDICATE
            if p == "rdf:type": # Turn rdf:type into "a" statement
                p_curated = "a"
            else:
                p_curated = p

            # OBJECT
            if not str(d) == "iri": # At non-IRI objects, all you need is the datatype
                o_curated = d
            else:
                if o.startswith(self.config["basicURI"] + ":" ) or o.startswith("$("):
                    # Select shape's name removing the rest of the IRI:
                    o_list = self.extract_information(o)

                    # Using standard to name the shape properly:
                    statement = "@:"
                    if len(o_list) >= 2:
                        statement = statement + o_list[0].lower()
                        for ol in o_list[1:]:
                            statement = statement + ol[0].upper() + ol[1:].lower()
                        statement = statement + "Shape"
                    else:
                        statement =  statement + o_list[-1].lower() + "Shape"
                    o_curated = statement

                elif "$(" in o and d == "iri": # For those non-static domain-specific ontological classes like HPO, Orphanet, etc
                    o_curated = "IRI"

                elif o.startswith("http"):
                    o_curated = "IRI"
                else:
                    o_curated = o

            # optional labels
            if p_curated == "rdfs:label" and d == "xsd:string" and self.config["configuration"] == "ejp":
                o_curated = "xsd:string?"
            
            triplet = [s_curated,p_curated,o_curated,d]
            self.triplets_curated.append(triplet) # Append curated triplets

        # individual triplets transformation into structured quads:
        self.tree = self.structured_quads(self.triplets_curated) # Transform your data into a subject-sorted dictionary

        # triplets into ShEx:
        for s in self.tree.items():
            subj= "\n" + s[0] + " IRI {"
            self.result_ShEx = self.result_ShEx + subj
            # for p,o in self.tree.items():
            for l in s[1]:
                if l[1].startswith("@") or l[1].startswith("xsd") or l[1] == "IRI":
                    pred_obj = "\n" + "\t" + l[0] + " " + l[1] + " ;"
                else:
                    pred_obj = "\n" + "\t" + l[0] + " [" + l[1] + "]" + " ;"
                self.result_ShEx = self.result_ShEx + pred_obj
            self.result_ShEx = self.result_ShEx[:-1]
            end = "\n" + "}" + "\n"
            self.result_ShEx = self.result_ShEx + end
        return self.result_ShEx


    def transform_OBDA(self):
        """
        Transform your triplets and prefixes inputs into OBDA (Ontology-Based Database Access).
        """
        self.result_OBDA = ""
        self.tree = dict() # Reset tree object
        self.triplets_curated = list()

        # Prefixes:
        self.result_OBDA = self.result_OBDA + "[PrefixDeclaration]" + "\n"
        for k,v in self.prefixes.items():
            prefix = k + ":" + "\t" + v
            self.result_OBDA = self.result_OBDA + prefix + "\n"

        # Triplets preproccesing:
        for quad in self.triplets:
            s,p,o,d = quad

            # SUBJECT:
            if '$(' in s:   # Change reference syntax to OBDA
                s_curated = s.replace('$(', '{')
                s_curated = s_curated.replace(")" , "}")
            else:
                s_curated = s

            # PREDICATE:
            if p == "rdf:type": # Turn rdf:type into "a" statement
                p_curated = "a"
            else:
                p_curated = p

            # OBJECT:
            if '$(' in o:   # Change reference syntax to OBDA
                o_curated = o.replace('$(', '{')
                o_curated = o_curated.replace(")" , "}")
                if o.startswith("$(") and d == "iri":
                    o_curated = "<" + o_curated + ">"
            else:
                o_curated = o

            triplet = [s_curated,p_curated,o_curated,d]
            self.triplets_curated.append(triplet) # Append curated triplets

        # individual triplets transformation into structured quads
        self.tree = self.structured_quads(self.triplets_curated)

        # OBDA build
        self.result_OBDA = self.result_OBDA + "\n" + "[MappingDeclaration] @collection [[" + "\n"
        for t in self.tree.items():
            self.result_OBDA = self.result_OBDA + "mappingId"	+ "\t" + self.config["source_name"] + milisec() + "\n" # milisec for unique mappingId objects
            self.result_OBDA = self.result_OBDA + "target" + "\t" + t[0]

            for l in t[1]:
                if not l[2] == "iri":
                    self.result_OBDA = self.result_OBDA +  " " + l[0] + " " + '"' + l[1]+ '"' + "^^" + l[2] + " ;"
                else:
                    self.result_OBDA = self.result_OBDA +  " " + l[0] + " " + l[1] + " ;"

            self.result_OBDA = self.result_OBDA + " ."
            self.result_OBDA = self.result_OBDA + "\n" + "source" + "\t" "SELECT * FROM mytable #ADD your QUERY HERE" + "\n" + "\n"

        self.result_OBDA = self.result_OBDA + "]]" + "\n"
        self.result_OBDA = self.result_OBDA.replace( "; .", ".")
        return self.result_OBDA


    def transform_SPARQL(self):
        
        if not self.config["basicURI"]: sys.exit("basicURI parameter must to be provided at configuration input")
        self.result_SPARQL = ""
        # Prefixes:
        for k,v in self.prefixes.items():
            self.result_SPARQL = self.result_SPARQL + "PREFIX " + k + ": " + "<" + v + ">" + "\n"

        self.result_SPARQL = self.result_SPARQL + "SELECT DISTINCT *" + "\n" + "WHERE {" + "\n"

        # Triplets preproccesing:
        for quad in self.triplets:
            s,p,o,d = quad

            # For subject:
            if s.startswith(self.config["basicURI"] + ":") or s.startswith("$("):
                # Select shape's name removing the rest of the IRI:
                s_list = self.extract_information(s)

                # Using standard to name the query properly:
                statement = "?"
                for sl in s_list:
                    statement = statement + sl.lower()
                s_curated = statement

            elif s.startswith("http"):
                s_curated = "<" + s + ">"
            else:
                s_curated = s 
            
            # For predicate:
            if p == "rdf:type": # Turn rdf:type into "a" statement
                p_curated = "a"
            else:
                p_curated = p

            # For object and datatype:
            if not str(d) == "iri": # At non-IRI objects, all you need is the datatype
                o_curated = d
            else:
                if o.startswith(self.config["basicURI"] + ":") or o.startswith("$("): # If subject is a data input reference:
                    # Select shape's name removing the rest of the IRI:
                    o_list = self.extract_information(o)

                    # Using standard to name the query properly:
                    statement = "?"
                    for ol in o_list:
                        statement = statement + ol.lower()
                    o_curated = statement 
                    
                elif o.startswith("http"):
                    o_curated = "<" + o + ">"
                else:
                    o_curated = o 
            
            self.result_SPARQL = self.result_SPARQL + "\t" +  s_curated + " " + p_curated + " " + o_curated + " ." + "\n"
        self.result_SPARQL = self.result_SPARQL + "}" + "\n"
        return self.result_SPARQL