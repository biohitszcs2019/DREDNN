import tensorflow as tf
import fp
import os
import numpy as np
from sklearn import metrics
from sklearn.utils import shuffle
import ROC as R

MODEL_SAVE_PATH = ".\model"
MODEL_NAME = "dnn_model"

#网络参数
n_features =1378
n_classes = 2
regularizer = 0.01
dp_rate = 0.1

#训练参数
learn_rate = 0.00001
training_epochs = 100
batch_size = 1
display_step = 1


#训练记录
loss_rec = np.zeros([training_epochs, 1])          #记录每一步迭代的损失
training_eval = np.zeros([training_epochs, 2])     #记录每一次迭代的acc和auc
testfile = False

def backward(X,Y,X_test,Y_test):
    x  = tf.placeholder(tf.float32, shape = [None, n_features])
    y_ = tf.placeholder(tf.float32, shape = [None, n_classes])
    drop_rate = tf.placeholder(tf.float32)

    # 前向传播计算（模型含参表达式）
    y = fp.forward(x, drop_rate, regularizer)

    # 损失定义
    with tf.name_scope("loss_fuction"):
        cost = tf.nn.sparse_softmax_cross_entropy_with_logits(logits = y, labels = tf.argmax(y_,1))
        loss = tf.reduce_mean(cost + tf.add_n(tf.get_collection('losses')))


    # 反向传播（单步梯度下降，训练中迭代更新参数）
    with tf.name_scope("train"):
        train_step = tf.train.AdamOptimizer(learning_rate = learn_rate).minimize(loss)


    # 模型评估正确率Evaluation （训练后利用新参数计算）
    with tf.name_scope("eval"):
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # 模型预测概率归一值（训练后利用新参数计算）
    y_score = tf.nn.softmax(logits = y )

    # 模型初始化
    init = tf.global_variables_initializer()


    # 模型保存
    saver = tf.train.Saver(max_to_keep=1)


    # 会话执行
    with tf.Session() as sess:
        sess.run(init)
        total_batch = int(X.shape[0]/ batch_size)

        #迭代训练（关键）
        for epoch in range(training_epochs):
            avg_cost = 0.
            x_tmp, y_tmp = shuffle(X, Y)

            for i in range(total_batch-1):
                # 取batch子集
                batch_x, batch_y = x_tmp[i*batch_size : i*batch_size+batch_size],y_tmp[i*batch_size : i*batch_size+batch_size]

                # 梯度下降train_step  并计算损失loss_total
                _, c = sess.run([train_step, loss],feed_dict={x: batch_x, y_: batch_y, drop_rate: dp_rate })

                # 计算batch平均损失
                avg_cost += c / total_batch

            del x_tmp
            del y_tmp

            #显示每次迭代训练的详细记录（次要）
            if epoch % display_step == 0:
                loss_rec[epoch] = avg_cost
                acc, y_s = sess.run([accuracy, y_score], feed_dict={x: X, y_: Y, drop_rate: 0} )
                auc = metrics.roc_auc_score(Y, y_s)
                training_eval[epoch] = [acc, auc]
                print ("Epoch:", '%d' % (epoch+1), "cost =", "{:.9f}".format(avg_cost),"Training accuracy:", round(acc,3), " Training auc:", round(auc,3))

             #早停止（次要）
            if avg_cost <= 0.1:
                print("Early stopping.")
                break

        if testfile == False:
            acc, y_s2 = sess.run([accuracy, y_score], feed_dict={x: X_test, y_: Y_test, drop_rate: 0})
            auc = metrics.roc_auc_score(Y_test, y_s2)
            R.plot_roc(np.transpose(Y_test)[0], np.transpose(y_s2)[0])
            print("*****=====", "Testing accuracy: ", acc, " Testing auc: ", auc, "=====*****")

            # 保存成文件“dnn_model-trainingepochs.meta”
            saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=training_epochs)
            print("Model restored successfully." + "  File Name：" + MODEL_NAME + "-" + str(training_epochs) + ".meta")

            return auc,y_s2

        #保存成文件“dnn_model-trainingepochs.meta”
        saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step = training_epochs)
        print("Model restored successfully."+"  File Name："+MODEL_NAME + "-" + str(training_epochs) + ".meta")

