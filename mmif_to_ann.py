import argparse
import os
import sys

from mmif.serialize import Mmif
from mmif.vocabulary import DocumentTypes
from lapps.discriminators import Uri

#usage:
#python mmif_to_ann.py example-mmif.json out-ann.ann spacy_nlp

def mmif_to_ann(mmif_path, ann_path, ner_app):

    def view_is_created_by_ner_app(view, ner_app):
        #view_app = str(view.metadata.get_parameter(param_key = "app"))
        view_app = str(view.metadata.app)
        if (view_app == ner_app) or (os.path.basename(view_app) == ner_app):
            return True
        return False
    
    with open(mmif_path) as fh_in:
        mmif_serialized = fh_in.read()
    mmif = Mmif(mmif_serialized)
    ner_views = mmif.get_all_views_contain(at_types = Uri.NE)
    for view in reversed(ner_views):
        if(view_is_created_by_ner_app(view, ner_app)):
            annotations = view.get_annotations(at_type = Uri.NE)
            annotations_to_file(annotations, ann_path)
            return

def annotations_to_file(annotations, ann_path):

    index = 0
    def annotation_to_line(i, annotation):
        token = annotation.properties
        return ('T'+str(i+1)+"\t"+str(token['category'])+" "+str(token['start'])+ \
                " "+str(token['end'])+"\t"+token['text']+"\n")

    ann_lines = [annotation_to_line(i, annotation) for i, annotation in enumerate(annotations)]
    with open(ann_path, 'w') as fh_out:
        fh_out.writelines(ann_lines)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', help="input file")
    parser.add_argument('outfile', nargs='?', help="output file")
    parser.add_argument('app', nargs='?', help="the app that did the NER")
    args = parser.parse_args()

    mmif_to_ann(args.infile, args.outfile, args.app)
