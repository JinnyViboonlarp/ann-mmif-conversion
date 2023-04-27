# ann-mmif-conversion

### converting .ann file to mmif (.mmif or .json)

```
python ann_to_mmif.py example-ann.ann out-mmif.mmif
```

to specify the text (where the NER is supposed to have worked on) in the document's property
```
python ann_to_mmif.py example-ann.ann out-mmif-with-text.mmif "Example text data"
```

to specify the location of the text (where the NER is supposed to have worked on) in the document's property
```
python ann_to_mmif.py -l example-ann.ann out-mmif-with-text-location.mmif "D:\path\to\text.txt"
```
per Mmif file's format restriction, the location here must be an absolute path

### converting mmif file to .ann

the name of the NER app (that has done the annotations to be exported to .ann) must be specified. In the following example, the app's name in the view's metadata is "https://apps.clams.ai/spacy_nlp". If there are many views with named-entity annotations from this app, only the last view's annotations are exported to .ann
```
python mmif_to_ann.py example-mmif.json out-ann.ann spacy_nlp
```
or, equivalently (in this case, the full name of the app must be used)
```
python mmif_to_ann.py example-mmif.json out-ann.ann https://apps.clams.ai/spacy_nlp
```
