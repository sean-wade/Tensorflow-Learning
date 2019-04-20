# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 17:07:31 2019

@author: Sean
"""

#测试集正确率0.97
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


#载入数据集
mnist = input_data.read_data_sets("MNIST_data", one_hot=True)

#每个批次大小
batch_size = 128
#计算一共多少个批次
n_batch = mnist.train.num_examples // batch_size

#定义两个placeholder
x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])

keep_prob = tf.placeholder(tf.float32)

#创建一个简单的神经网络
#W1 = tf.Variable(tf.random.normal([784, 10]))
#truncated_normal: 切割正态分布，意思大概是取中间的
W1 = tf.Variable(0.01 * tf.truncated_normal([784, 250], mean=0.0, stddev=1.0))
b1 = tf.Variable(tf.zeros([250])+0.1)
L1 = tf.nn.relu(tf.matmul(x, W1) + b1)
L1_drop = tf.nn.dropout(L1, keep_prob)


W2 = tf.Variable(1 * tf.truncated_normal([250, 10], mean=0.0, stddev=1.0))
b2 = tf.Variable(tf.zeros([10])+0.1)
prediction = tf.nn.softmax(tf.matmul(L1_drop, W2) + b2) 


#二次代价函数
loss = tf.reduce_mean(tf.square(y - prediction))
#交叉熵代价函数
#loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=prediction))

#梯度下降法
#train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
train_step = tf.train.AdamOptimizer(0.0001).minimize(loss)

#初始化变量
init = tf.global_variables_initializer()

#结果存放于bool列表
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))

#求准确率，tf.cast是把bool转换成float32
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)
    #所有图片训练20次
    for epoch in range(51):
        #每100个图片训练一次
        for batch in range(n_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys, keep_prob:0.7})
        
        acc = sess.run(accuracy, feed_dict={x:mnist.test.images, y:mnist.test.labels, keep_prob:1.0})
        print("Iter: " + str(epoch) + ", Testing Accuracy: " + str(acc))
    #保存模型
    saver.save(sess, 'net/my_net.ckpt')
























