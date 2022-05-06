# prefixes:
#   linkml: https://w3id.org/linkml/
# https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/types.yaml
# https://github.com/linkml/linkml-model/blob/main/linkml_model/model/schema/meta.yaml
# imports:
#   - linkml:types
#   - linkml:mappings
#   - linkml:extensions
#   - linkml:annotations
# https://w3id.org/linkml/types.yaml -> https://linkml.io/linkml-model/linkml_model/model/schema/types.yaml

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
import pandas as pd
import re

pd.set_option('display.max_columns', None)

meta_view = SchemaView("https://w3id.org/linkml/meta.yaml")
type_slots = meta_view.class_induced_slots("type_definition")
ts_names = [i.name for i in type_slots]
ts_dict = dict(zip(ts_names, type_slots))
ts_names.sort()

# why do I have to do this?
ts_names.remove("type_uri")
ts_names.append("uri")

type_view = SchemaView("https://w3id.org/linkml/types.yaml")
types = type_view.all_types()
type_names = list(types.keys())
type_names.sort()

type_lod = []
for current_tn in type_names:
    current_type = types[current_tn]
    current_type_dict = {}
    for current_tsn in ts_names:
        # why do I have to do this (for broad mappings vs broad_mappings)
        underscored = re.sub(r' +', '_', current_tsn)
        ctu = current_type[underscored]
        if ctu:
            # todo collapse lists
            # check against schema or just by object type?
            if isinstance(ctu, list):
                panda_friendly = "|".join(ctu)
            else:
                panda_friendly = ctu
            current_type_dict[underscored] = panda_friendly
    type_lod.append(current_type_dict)
type_df = pd.DataFrame(type_lod)

tdc = list(type_df.columns)
tdc.remove("name")
tdc = ["name"] + tdc

type_df = type_df[tdc]

# print(type_df)


type_df.to_csv("type_df.tsv", sep="\t", index=False)
