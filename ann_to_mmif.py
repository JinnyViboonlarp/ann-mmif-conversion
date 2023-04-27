import argparse
import os
import sys

from mmif.serialize import Mmif
from mmif.serialize.annotation import Document
from mmif.vocabulary import DocumentTypes
from lapps.discriminators import Uri

MMIF_VERSION = '0.4.0'
identifier = ('https://mmif.clams.ai/'+MMIF_VERSION)

#usage:
#python ann_to_mmif.py example-ann.ann out-mmif.mmif
#python ann_to_mmif.py example-ann.ann out-mmif-with-text.mmif "Hello, this is Jim Lehrer with the NewsHour on PBS. In the nineteen eighties, barking dogs have increasingly become a problem in urban areas."
#python ann_to_mmif.py -l example-ann.ann out-mmif-with-text-location.mmif "D:\clams\ann-mmif-conversion\example-text.txt"

def ann_to_mmif(ann_path, mmif_path, text=None, is_location=False):

    doc_id = "m1"
    document = {"@type": str(DocumentTypes.TextDocument),
                "properties": {"id": doc_id}}
    if(text != None):
        if(is_location):
            document["properties"]["location"] = text
        else:
            document["properties"]["text"] = {"@value": text}
    mmif = Mmif({"metadata": {"mmif": identifier},
                 "documents": [document],
                 "views":[]})
    view = mmif.new_view()
    view.metadata.app = "ann-to-mmif-conversion"
    view.new_contain(Uri.NE, document=doc_id)
    add_annotations(ann_path, view)
    mmif_json = mmif.serialize(pretty=True)
    with open(mmif_path, 'w') as fh_out:
        fh_out.write(mmif_json)

def add_annotations(ann_path, view):
    with open(ann_path, 'r') as fh_in:
        lines = fh_in.readlines()
    for index, line in enumerate(lines, start=1):
        ent = line.split()
        # ent[i]: 0=index, 1=type, 2=start_char, 3=end_char, 4+=name
        add_annotation( view, ("ne"+str(index)),
                    { "start": int(ent[2]), "end": int(ent[3]), "text": (" ".join(ent[4:])),
                      "category": ent[1] })

def add_annotation(view, identifier, properties):
    """Utility method to add an annotation to a view."""
    a = view.new_annotation(Uri.NE, identifier)
    for prop, val in properties.items():
        a.add_property(prop, val)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', help="input file")
    parser.add_argument('outfile', nargs='?', help="output file")
    parser.add_argument('-l', '--location',  action='store_true', help="indicate that the text file's\
                        location would be given (instead of the text's content)")
    parser.add_argument('text', nargs='?', help="original text file that the NER is done on")
    args = parser.parse_args()

    if(args.text != None):
        ann_to_mmif(args.infile, args.outfile, args.text, args.location)
    else:
        ann_to_mmif(args.infile, args.outfile)
