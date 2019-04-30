import fp
import bp
import time
import ROC as R
import tensorflow as tf
import numpy as np
from sklearn import metrics

#网络参数
n_features =1378
n_classes = 2

regularizer = 0.01
TEST_INTERVAL_SECS = 5


def test(X,Y):
    with tf.Graph().as_default() as g:

        x  = tf.placeholder(tf.float32, shape=[None, n_features])
        y_ = tf.placeholder(tf.float32, shape=[None, n_classes])
        drop_rate = tf.placeholder(tf.float32)
        y = fp.forward(x, drop_rate, regularizer)


        saver = tf.train.Saver(tf.trainable_variables())


        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        y_score = tf.nn.softmax(logits=y)


        with tf.Session() as sess :
            ckpt = tf.train.get_checkpoint_state(bp.MODEL_SAVE_PATH)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess,ckpt.model_checkpoint_path)
                print("Model restored success.")

                acc, y_s = sess.run([accuracy, y_score], feed_dict={x: X, y_: Y, drop_rate: 0})
                auc = metrics.roc_auc_score(Y, y_s)
                R.plot_roc(np.transpose(Y)[0], np.transpose(y_s)[0])
                print("*****=====", "Testing accuracy: ", acc, " Testing auc: ", auc, "=====*****")

                return y_s

                # print("the result is:",tf.argmax(y_s,1))
                # print("the propabilty is：",y_s)

            else:
                print("NO checkpoint file found")
                return

            time.sleep(TEST_INTERVAL_SECS)






