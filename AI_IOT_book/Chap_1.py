'''
Created on 18 Jun 2020

@author: AbdulMannanRauf
'''
#import tensor flow as tf gives an error thatswhy its replaced by import tensorflow.compat.v1 as tf
from astunparse import __main__

class Chap1(object):
     # default constructor 
    def __init__(self): 
        self.name = "Chap1"
    
    def code_1(self):
        import tensorflow.compat.v1 as tf
        tf.disable_v2_behavior()
        import numpy as np
        # Data
        # A random matrix of size [3,5]
        mat1 = np.random.rand(3,5)  
        print(mat1)
        # A random matrix of size [5,2]
        mat2 = np.random.rand(5,2) 
        print(mat2)
        A = tf.placeholder(tf.float32, None, name='A')
        B = tf.placeholder(tf.float32, None, name='B')
        C = tf.matmul(A,B)
        #Execution Graph
        with tf.Session() as sess:
            result = sess.run(C, feed_dict={A: mat1, B:mat2})
            print(result)
        
    def code_2(self):
        
        import keras.backend as K
        import numpy as np
        A = np.random.rand(20,500)
        B = np.random.rand(500,3000)
        
        x = K.variable(value=A)
        y = K.variable(value=B)
        
        z = K.dot(x,y)

        print(K.eval(z))
        
        




if __name__ == '__main__':
    obj = Chap1()
    print(obj.name)
    obj.code_1()
    obj.code_2()
