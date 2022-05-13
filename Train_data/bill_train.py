import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.initializers as I
from chainer import training
from chainer.training import extensions


class MyChain(chainer.Chain):
    def __init__(self):
        super(MyChain, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(4, 10)
            self.l2 = L.Linear(10, 10)
            self.l3 = L.Linear(10, 4)

    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        y = self.l3(h2)
        return y


epoch = 1000
batchsize = 8

with open('train_data.txt', 'r') as f:
    lines = f.readlines()

data = []
for l in lines:
    d = l.strip().split(',')
    data.append(list(map(int, d)))

data = np.array(data, dtype=np.int32)
trainx, trainy = np.hsplit(data, [4])
trainy = trainy[:, 0]
trainx = np.array(trainx, dtype=np.float32)
trainy = np.array(trainy, dtype=np.int32)
train = chainer.datasets.TupleDataset(trainx, trainy)
test = chainer.datasets.TupleDataset(trainx, trainy)

model = L.Classifier(MyChain(), lossfun=F.softmax_cross_entropy)
optimizer = chainer.optimizers.Adam()
optimizer.setup(model)

train_iter = chainer.iterators.SerialIterator(train, batchsize)
test_iter = chainer.iterators.SerialIterator(
    test, batchsize, repeat=False, shuffle=False)

updater = training.StandardUpdater(train_iter, optimizer)

trainer = training.Trainer(updater, (epoch, 'epoch'))

trainer.extend(extensions.LogReport())
trainer.extend(extensions.Evaluator(test_iter, model))
trainer.extend(extensions.PrintReport(
    ['epoch', 'main/loss', 'validation/main/loss', 'main/accuracy', 'validation/main/accuracy', 'elapsed_time']))

trainer.run()

chainer.serializers.save_npz("./result/out.model", model)
