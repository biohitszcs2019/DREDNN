import tensorflow as tf
import numpy as np



E = 1
n_features = 1378
n_classes  = 2

n_hidden_1 = n_features
n_hidden_2 = 64
n_hidden_3 = 16
drop1 = False


file2 = './data/GEO1/example_adjacency.txt'
A = np.loadtxt(file2, dtype=int, delimiter=None)

def forward(x, drop_rate, regularizer):
    with tf.name_scope("network"):
        w1 = get_weight([n_features, n_hidden_1],regularizer)
        b1 = get_bias([n_hidden_1])

        w2 = get_weight([n_hidden_1, n_hidden_2],regularizer)
        b2 = get_bias([n_hidden_2])

        w3 = get_weight([n_hidden_2, n_hidden_3],regularizer)
        b3 = get_bias([n_hidden_3])

        wo = get_weight([n_hidden_3, n_classes],regularizer)
        bo = get_bias([n_classes])


        if E == 0 :
            y1 = tf.nn.elu(tf.matmul(x, w1) + b1)
        else:
            y1 = tf.nn.elu( tf.matmul(x, tf.multiply(w1, A) ) + b1 )


        if drop1:
            y1 = tf.nn.dropout(y1, rate =drop_rate)


        y2 = tf.nn.elu(tf.matmul(y1, w2) + b2)
        y2 = tf.nn.dropout(y2, rate=drop_rate)


        y3 = tf.nn.elu(tf.matmul(y2, w3) + b3)
        y3 = tf.nn.dropout(y3, rate=drop_rate)


        y = tf.matmul(y3,wo) + bo

        return y



def get_weight(shape,regularizer):
    with tf.name_scope("weights"):
        w = tf.Variable(tf.truncated_normal(shape=shape, stddev=0.1))

        if regularizer != None:
            tf.add_to_collection('losses',tf.contrib.layers.l2_regularizer(regularizer)(w))
        return w


def get_bias(shape):
    with tf.name_scope("bias"):
        b = tf.Variable(tf.zeros(shape))
        return b








