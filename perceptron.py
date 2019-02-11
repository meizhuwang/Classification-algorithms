#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

NUM_FEATURES = 124 #features are 1 through 123 (123 only in test set), +1 for the bias
DATA_PATH = "/Users/Pro/Desktop/spring semester/machien learning folder/perceptron"

#returns the label and feature value vector for one datapoint (represented as a line (string) from the data file)
def parse_line(line):
    tokens = line.split()
    x = np.zeros(NUM_FEATURES)
    y = int(tokens[0])
    for t in tokens[1:]:
        parts = t.split(':')
        feature = int(parts[0])
        value = int(parts[1])
        x[feature-1] = value
    x[-1] = 1 #bias
    return y, x

#return labels and feature vectors for all datapoints in the given file
def parse_data(filename):
    with open(filename, 'r') as f:
        vals = [parse_line(line) for line in f]
        (ys, xs) = ([v[0] for v in vals],[v[1] for v in vals])
        return np.asarray(ys), np.asarray(xs) #returns a tuple, first is an array of labels, second is an array of feature vectors

def perceptron(train_ys, train_xs, dev_ys, dev_xs, args):
    weights = np.zeros(NUM_FEATURES)
    iter=0
    test_acc=[]
    traintest_acc=[]
    while iter < args.iterations:
        index=0
        while index < train_xs.shape[0]:
            # print("type of weights",type(weights),"weights",weights,"size of weights",weights.shape)
            # print("type of one traindata",type(train_xs[index]),"weights",train_xs[index],"size of one traindata",train_xs[index].shape)
            if np.dot(weights, train_xs[index]) * train_ys[index] <= 0:
                weights+=args.lr*train_xs[index]*train_ys[index]
            index+=1
        traintest_acc.append(test_accuracy(weights,train_ys,train_xs))
        if not args.nodev:
            test_acc.append(test_accuracy(weights,dev_ys,dev_xs))
        iter+=1
    # plt.scatter([i for i in range(len(test_acc))],test_acc,label="dev")
    # plt.scatter([i for i in range(len(traintest_acc))],traintest_acc,label="train")
    # plt.show()
    return weights


def test_accuracy(weights, test_ys, test_xs):
    accuracy = 0.0
    rightentry=0
    # print("weights",weights)
    for i in range(test_ys.size):
        if test_ys[i]*np.dot(weights, test_xs[i])>0:
            rightentry+=1
    accuracy=rightentry/test_ys.size
    return accuracy

def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Basic perceptron algorithm.')
    parser.add_argument('--nodev', action='store_true', default=False, help='If provided, no dev data will be used.')
    parser.add_argument('--iterations', type=int, default=50, help='Number of iterations through the full training data to perform.')
    parser.add_argument('--lr', type=float, default=1.0, help='Learning rate to use for update in training loop.')
    parser.add_argument('--train_file', type=str, default=os.path.join(DATA_PATH,'a7a.train'), help='Training data file.')
    parser.add_argument('--dev_file', type=str, default=os.path.join(DATA_PATH,'a7a.dev'), help='Dev data file.')
    parser.add_argument('--test_file', type=str, default=os.path.join(DATA_PATH,'a7a.test'), help='Test data file.')
    args = parser.parse_args()

    """
    At this point, args has the following fields:

    args.nodev: boolean; if True, you should not use dev data; if False, you can (and should) use dev data.
    args.iterations: int; number of iterations through the training data.
    args.lr: float; learning rate to use for training update.
    args.train_file: str; file name for training data.
    args.dev_file: str; file name for development data.
    args.test_file: str; file name for test data.
    """
    train_ys, train_xs = parse_data(args.train_file)
    dev_ys = None
    dev_xs = None
    if not args.nodev:
        dev_ys, dev_xs= parse_data(args.dev_file)
    test_ys, test_xs = parse_data(args.test_file)
    weights = perceptron(train_ys, train_xs, dev_ys, dev_xs, args)
    accuracy = test_accuracy(weights, test_ys, test_xs)
    print('Test accuracy: {}'.format(accuracy))
    print('Feature weights (bias last): {}'.format(' '.join(map(str,weights))))

if __name__ == '__main__':
    main()
