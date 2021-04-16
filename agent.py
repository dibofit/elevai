import tensorflow as tf

class agent:

    def __init__(self,input_shape,output_size,optimizer=None):
        inputs = tf.keras.Input(shape=input_shape)
        l1 = tf.keras.layers.Dense(64, activation = tf.nn.relu)(inputs)
        l2 = tf.keras.layers.Dense(32, activation = tf.nn.relu)(l1)
        outputs = tf.keras.layers.Dense(output_size, activation = tf.nn.softmax)(l2)
        self.model = tf.keras.Model(inputs = inputs, outputs = outputs)
        
        self.opt = 0
        if not optimizer = None:
            self.opt = optimizer
        else
            self.opt = tf.keras.optimizers.Adam()


    def calc_loss(self,y_hat,y):
        #need to fix here later potentially simple y_hat, y might not work

        return 0

    def learn(self,dataX,dataY):
        #dataX and dataY are iterable 
        for x,y in zip(dataX, dataY):
            with tf.GradientTape() as tape:
                y_hat = self.model(x,training = True)
                loss = self.calc_loss(y_hat,y)

            gradients = tape.gradient(loss,model.trainable_variables)
            self.opt.apply_gradients(zip(gradients, self.model.trainable_variables))



    

