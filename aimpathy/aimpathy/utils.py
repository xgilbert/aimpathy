import json
import logging
import pickle

from sys import exit


def tsv_to_json(src, out):
    """Convert tsv files to dataturks json format

    Args:
        src (str): path to input data (tsv)
        out (str): path to output data (json)

    Returns:
        int: exit status
    """

    try:
        f = open(src, 'r')   # input
        fp = open(out, 'w')  # output

        data_dict = {}
        annotations = []
        label_dict = {}
        s = ''
        start = 0

        for line in f:
            if line[0:len(line)-1] != '.\tO':
                word, entity = line.split('\t')
                s += word + " "
                entity = entity[:len(entity)-1]

                # start and end positions of entities
                if len(entity) != 1:
                    d = {}
                    d['text'] = word
                    d['start'] = start
                    d['end'] = start + len(word) - 1

                    try:
                        label_dict[entity].append(d)
                    except:
                        label_dict[entity] = []
                        label_dict[entity].append(d)

                start += len(word)+1
            
            else:
                data_dict['content'] = s
                s = ''
                label_list = []

                for ents in list(label_dict.keys()):
                    for i in range(len(label_dict[ents])):
                        if(label_dict[ents][i]['text'] != ''):
                            l = [ents, label_dict[ents][i]]
                            for j in range(i+1, len(label_dict[ents])):
                                if(label_dict[ents][i]['text'] == label_dict[ents][j]['text']):
                                    di = {}
                                    di['start'] = label_dict[ents][j]['start']
                                    di['end'] = label_dict[ents][j]['end']
                                    di['text'] = label_dict[ents][i]['text']
                                    l.append(di)
                                    label_dict[ents][j]['text'] = ''
                            label_list.append(l)

                for entities in label_list:
                    label = {}
                    label['label'] = [entities[0]]
                    label['points'] = entities[1:]
                    annotations.append(label)

                data_dict['annotation'] = annotations
                annotations = []
                json.dump(data_dict, fp)
                fp.write('\n')
                data_dict = {}
                start = 0
                label_dict = {}

    except Exception as e:
        logging.exception(
            "Unable to process file" + "\n" + "error = " + str(e)
        )
        exit(1)


def json_to_spacy(src, out):
    """Parse json files to spacy traning data

    Args:
        src (str): path to input data (json)
        out (str): path to output data (pickle, spacy training data)

    Returns:
        int: exit status
    """

    try:
        data_train = []

        with open(src, 'r') as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)
            text = data['content']
            entities = []

            for annotation in data['annotation']:
                point = annotation['points'][0]
                labels = annotation['label']

                if not isinstance(labels, list):
                    labels = [labels]

                for label in labels:
                    entities.append((point['start'], point['end'] + 1, label))

            data_train.append((text, {"entities": entities}))

        with open(out, 'wb') as fout:
            pickle.dump(data_train, fout)

    except Exception as e:
        logging.exception(
            "Unable to process " + src + "\n" + "error = " + str(e)
        )
        exit(1)
