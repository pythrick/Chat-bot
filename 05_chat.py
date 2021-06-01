from gensim.models import Doc2Vec
import linecache

if __name__ == '__main__':
    doc2vec_model = Doc2Vec.load("models/doc2vec.model")
    while (m := input("> ")) not in ("q", "exit", "quit", "sair", "fim"):
        tokens = m.split()
        new_vector = doc2vec_model.infer_vector(tokens)
        index, acc = doc2vec_model.dv.most_similar([new_vector], topn=10)[0]
        print(index, acc)
        print(linecache.getline("train.to", index + 1))
