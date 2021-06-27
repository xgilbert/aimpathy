import os
import pickle
import random

import spacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example

from aimpathy.utils import tsv_to_json, json_to_spacy


def train(DATA_PATH, MODEL_PATH, n_iter=10):
    """Train model

    Args:
        DATA_PATH (str): Base PATH for training data.
        MODEL_PATH (str): Base PATH for trained model.
        n_iter (int, optional): [description]. Defaults to 20.
    """

    tsv_to_json(
        f"{DATA_PATH}/training.txt",
        f"{DATA_PATH}/training.json",
    )

    json_to_spacy(
        f"{DATA_PATH}/training.json",
        f"{DATA_PATH}/training.pickle",
    )

    nlp = spacy.load("en_core_web_sm")

    with open (f"{DATA_PATH}/training.pickle", 'rb') as f:
        TRAIN_DATA = pickle.load(f)

    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))

        for batch in batches:
            for text, annotations in batch:
                # create Example object
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                # update model
                nlp.update([example], losses=losses, drop=0.3)
        # print(losses) # @DEBUG

    nlp.to_disk(f"{MODEL_PATH}/model.pickle")