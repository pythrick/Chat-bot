from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
import multiprocessing
import os
from dataclasses import dataclass


@dataclass
class MyTexts:
    train_file: str

    def __iter__(self):
        with open(self.train_file) as train_file:
            for i, row in enumerate(train_file):
                yield TaggedDocument(words=simple_preprocess(row), tags=[i])


if __name__ == '__main__':
    print("Doing cool math stuff...")
    cores = multiprocessing.cpu_count()

    texts = MyTexts("train.from")
    doc2vec_model = Doc2Vec(vector_size=200, workers=cores)
    doc2vec_model.build_vocab(texts)
    doc2vec_model.train(texts, total_examples=doc2vec_model.corpus_count, epochs=15)

    if not os.path.exists("models"):
        os.makedirs("models")

    doc2vec_model.save("models/doc2vec.model")
    print("And we did it!")
