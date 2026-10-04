import numpy as np

import matplotlib.pyplot as plt
import logging
logging.basicConfig(
    # filename="results.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
import matplotlib
font = {'weight' : 'normal',
        'size'   : 22}
matplotlib.rc('font', **font)


# GLOBAL PARAMETERS FOR STOCHASTIC GRADIENT DESCENT
np.random.seed(102)
step_size_arr = [0.03, 0.01, 0.003]
batch_size_arr = [200, 500, 1000]
max_epochs_arr = [500, 1000]

# GLOBAL PARAMETERS FOR NETWORK ARCHITECTURE
number_of_layers_arr = [5, 10]
width_of_layers_arr = [16]  # only matters if number of layers > 1
activation_arr = ["ReLU" if True else "Sigmoid" ]

# FINAL PARAMETERS
step_size_arr = [0.03]
batch_size_arr = [1000]
max_epochs_arr = [600]
number_of_layers_arr = [5]
activation_arr = ["ReLU" if True else "Sigmoid" ]

def main():
  # Load data and display an example
  X_train, Y_train, X_val, Y_val, X_test = loadData()
  # displayExample(X_train[np.random.randint(0,len(X_train))]) # UNCOMMENT THIS SAFOIA SDFOIHANC9U982 N8PN2982NP9N2NECPNP2  N3 n2 ncep2P3CE4P  2 NP3C  ppy9F SDFA OSDHFOA 98aye98yn98wy nr89pnya ye8npeR NYPYNE yP9 ynp9P9NPNpn pNPN PNYp9yp9n yap9fp9nap9f np9
  augment_data(X_train, Y_train)
  for step_size in step_size_arr:
    for batch_size in batch_size_arr:
      for max_epochs in max_epochs_arr:
        for number_of_layers in number_of_layers_arr:
          for width_of_layers in width_of_layers_arr:
            for activation in activation_arr:
              logging.info(f"step_size_{step_size}-batch_size_{batch_size}-max_epochs_{max_epochs}-number_of_layers_{number_of_layers}")

              # Build a network with input feature dimensions, output feature dimension,
              # hidden dimension, and number of layers as specified below
              net = FeedForwardNeuralNetwork(X_train.shape[1],10,width_of_layers,number_of_layers, activation=activation)

              # Some lists for book-keeping for plotting later
              losses = []
              val_losses = []
              accs = []
              val_accs = []


              # Loss function
              lossFunc = CrossEntropySoftmax()

              # Indicies we will use to shuffle data randomly
              inds = np.arange(len(X_train))
              for i in range(max_epochs):
                
                # Shuffled indicies so we go through data in new random batches
                np.random.shuffle(inds)

                # Go through all datapoints once (aka an epoch)
                j = 0
                acc_running = loss_running = 0
                while j < len(X_train):

                  # Select the members of this random batch
                  b = min(batch_size, len(X_train)-j)
                  X_batch = X_train[inds[j:j+b]]
                  Y_batch = Y_train[inds[j:j+b]].astype(int)
                
                  # Compute the scores for our 10 classes using our model
                  logits = net.forward(X_batch)
                  loss = lossFunc.forward(logits, Y_batch)
                  acc = np.mean( np.argmax(logits,axis=1)[:,np.newaxis] == Y_batch)
                  
                  # Compute gradient of Cross-Entropy Loss with respect to logits
                  loss_grad = lossFunc.backward()

                  # Pass gradient back through networks
                  net.backward(loss_grad)

                  # Take a step of gradient descent
                  net.step(step_size)

                  #Record losses and accuracy then move to next batch
                  losses.append(loss)
                  accs.append(acc)
                  loss_running += loss*b
                  acc_running += acc*b

                  j+=batch_size

                # Evaluate performance on validation. This function looks very similar to the training loop above, 
                vloss, vacc = evaluateValidation(net, X_val, Y_val, batch_size)
                val_losses.append(vloss)
                val_accs.append(vacc)
                
                # Print out the average stats over this epoch
                # if i > (max_epochs - 6):
                #   logging.info("[Epoch {:3}]   Loss:  {:8.4}     Train Acc:  {:8.4}%      Val Acc:  {:8.4}%".format(i,loss_running/len(X_train), acc_running / len(X_train)*100,vacc*100))
                logging.info("[Epoch {:3}]   Loss:  {:8.4}     Train Acc:  {:8.4}%      Val Acc:  {:8.4}%".format(i,loss_running/len(X_train), acc_running / len(X_train)*100,vacc*100))

                


              fig, ax1 = plt.subplots(figsize=(16,9))
              color = 'tab:red'
              ax1.plot(range(len(losses)), losses, c=color, alpha=0.25, label="Train Loss")
              ax1.plot([np.ceil((i+1)*len(X_train)/batch_size) for i in range(len(val_losses))], val_losses,c="red", label="Val. Loss")
              ax1.set_xlabel("Iterations")
              ax1.set_ylabel("Avg. Cross-Entropy Loss", c=color)
              ax1.tick_params(axis='y', labelcolor=color)
              ax1.set_ylim(-0.01,3)

              ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

              color = 'tab:blue'
              ax2.plot(range(len(losses)), accs, c=color, label="Train Acc.", alpha=0.25)
              ax2.plot([np.ceil((i+1)*len(X_train)/batch_size) for i in range(len(val_accs))], val_accs,c="blue", label="Val. Acc.")
              ax2.set_ylabel(" Accuracy", c=color)
              ax2.tick_params(axis='y', labelcolor=color)
              ax2.set_ylim(-0.01,1.01)

              fig.tight_layout()  # otherwise the right y-label is slightly clipped
              ax1.legend(loc="center")
              ax2.legend(loc="center right")
              # plt.savefig(f"step_size_{step_size}-batch_size_{batch_size}-max_epochs_{max_epochs}-number_of_layers_{number_of_layers}.png")
              # plt.close()
              plt.show()

  ################################
  # Q7 Evaluate on Test
  ################################
  logits = net.forward(X_test)
  print(f"logits: {logits}")
  print(f"logits.shape: {logits.shape}")
  probs = softmax(logits)
  print(f"probs: {probs}")
  print(f"probs.shape: {probs.shape}")
  labels = []
  for prob in probs:
    best_i = 0
    max = prob[best_i]
    for i, pred in enumerate(prob):
      if pred > max:
        best_i = i
        max = prob[i]
    labels.append([best_i])
  labels = np.array(labels)
  print(f"labels: {labels}")
  print(f"labels.shape: {labels.shape}")
  # add index and header then save to file
  print(f"np.array(range(len(X_test)),dtype=int): {np.array(range(len(X_test)),dtype=int)}")
  print(f"np.array(range(len(X_test)),dtype=int).shape: {np.array(range(len(X_test)),dtype=int).shape}")
  test_out = np.concatenate((np.expand_dims(np.array(range(len(X_test)),dtype=int), axis=1), labels), axis=1)
  header = np.array([["id", "digit"]])
  test_out = np.concatenate((header, test_out))
  np.savetxt('test_predicted.csv', test_out, fmt='%s', delimiter=',')

def augment_data():
  displayExample(X_train[np.random.randint(0,len(X_train))]) # UNCOMMENT THIS SAFOIA SDFOIHANC9U982 N8PN2982NP9N2NECPNP2  N3 n2 ncep2P3CE4P  2 NP3C  ppy9F SDFA OSDHFOA 98aye98yn98wy nr89pnya ye8npeR NYPYNE yP9 ynp9P9NPNpn pNPN PNYp9yp9n yap9fp9nap9f np9


class LinearLayer:

  # Initialize our layer with (input_dim, output_dim) weight matrix and a (1,output_dim) bias vector
  def __init__(self, input_dim, output_dim):
    self.weights = np.random.randn(input_dim, output_dim)* np.sqrt(2. / input_dim)
    self.bias = np.ones( (1,output_dim) )*0.5

  # During the forward pass, we simply compute Xw+b
  def forward(self, input):
    self.input = input #Storing X
    return  self.input@self.weights + self.bias

  #################################################
  # Q3 Implementing Backward Pass for Linear
  #################################################
  # Inputs :
  # grad dL/dZ -- For a batch size of n, grad is a (n x output_dim ) matrix where
  # the i’th row is the gradient of the loss of example i with respect
  # to z_i ( the output of this layer for example i)
  #
  # Computes and stores :
  # self . grad_weights dL/dW -- A ( input_dim x output_dim ) matrix storing the
  # gradient of the loss with respect to the weights of # this layer.
  #
  # self . grad_bias dL/db -- A (1 x output_dim ) matrix storing the gradient
  # of the loss with respect to the bias of this layer .
  #
  # Return Value :
  # grad_input dL/dX -- For a batch size of n, grad_input is a (n x input_dim )
  # matrix where the i’th row is the gradient of the loss of
  # example i with respect to x_i (the input of this # layer for example i)
  # ################################################
  def backward(self, grad):
    self.grad_weights = self.input.T@grad
    self.grad_bias = np.sum(grad, axis=0)
    return grad@self.weights.T
    
  def step(self, step_size):
    self.weights -= step_size*self.grad_weights
    self.bias -= step_size*self.grad_bias


###############################################
# Instructor code below. Worth understanding
# but don't need to modify for base assignment
###############################################



class FeedForwardNeuralNetwork:

  def __init__(self, input_dim, output_dim, hidden_dim, num_layers, activation="ReLU"):

    if num_layers == 1:
      self.layers = [LinearLayer(input_dim, output_dim)]
    else:
      self.layers = [LinearLayer(input_dim, hidden_dim)]
      self.layers.append(Sigmoid() if activation=="Sigmoid" else ReLU())
      for _ in range(num_layers-2):
        self.layers.append(LinearLayer(hidden_dim, hidden_dim))
        self.layers.append(Sigmoid() if activation=="Sigmoid" else ReLU())
      self.layers.append(LinearLayer(hidden_dim, output_dim))

  def forward(self, X):
    for layer in self.layers:
      X = layer.forward(X)
    return X

  def backward(self, grad):
    for layer in reversed(self.layers):
      grad = layer.backward(grad)

  def step(self, step_size=0.001):
    for layer in self.layers:
      layer.step(step_size)





# Sigmoid or Logistic Activation Function
class Sigmoid:

  # Given the input, apply the sigmoid function
  # store the output value for use in the backwards pass
  def forward(self, input):
    self.act = 1/(1+np.exp(-input))
    return self.act
  
  # Compute the gradient of the output with respect to the input
  # self.act*(1-self.act) and then multiply by the loss gradient with 
  # respect to the output to produce the loss gradient with respect to the input
  def backward(self, grad):
    return grad * self.act * (1-self.act)

  # The Sigmoid has no parameters so nothing to do during a gradient descent step
  def step(self,step_size):
    return

# Rectified Linear Unit Activation Function
class ReLU:

  # Forward pass is max(0,input)
  def forward(self, input):
    self.mask = (input > 0)
    return input * self.mask
  
  # Backward pass masks out same elements
  def backward(self, grad):
    return grad * self.mask

  # No parameters so nothing to do during a gradient descent step
  def step(self,step_size):
    return



#####################################################
# Utility Functions for Computing Loss / Val Metrics
#####################################################
def softmax(x):
  x -= np.max(x,axis=1)[:,np.newaxis]  # Numerical stability trick
  return np.exp(x) / (np.sum(np.exp(x),axis=1)[:,np.newaxis])


class CrossEntropySoftmax:

  def forward(self, logits, labels):
    self.probs = softmax(logits)
    self.labels = labels
    return -np.mean(np.log(self.probs[np.arange(len(self.probs))[:,np.newaxis],labels]+0.00001))

  def backward(self):
    grad = self.probs
    grad[np.arange(len(self.probs))[:,np.newaxis],self.labels] -=  1
    return  grad.astype(np.float64)/len(self.probs)


def evaluateValidation(model, X_val, Y_val, batch_size):
  val_loss_running = 0
  val_acc_running = 0
  j=0

  lossFunc = CrossEntropySoftmax()

  while j < len(X_val):
    b = min(batch_size, len(X_val)-j)
    X_batch = X_val[j:j+b]
    Y_batch = Y_val[j:j+b].astype(int)
   
    logits = model.forward(X_batch)
    loss = lossFunc.forward(logits, Y_batch)
    acc = np.mean( np.argmax(logits,axis=1)[:,np.newaxis] == Y_batch)

    val_loss_running += loss*b
    val_acc_running += acc*b
       
    j+=batch_size

  return val_loss_running/len(X_val), val_acc_running/len(X_val)







#####################################################
# Utility Functions for Loading and Displaying Data
#####################################################
def loadData(normalize = True):
  train = np.loadtxt("mnist_small_train.csv", delimiter=",", dtype=np.float64)
  val = np.loadtxt("mnist_small_val.csv", delimiter=",", dtype=np.float64)
  test = np.loadtxt("mnist_small_test.csv", delimiter=",", dtype=np.float64)

  # Normalize Our Data
  if normalize:
    X_train = train[:,:-1]/256-0.5
    X_val = val[:,:-1]/256-0.5
    X_test = test/256-0.5
  else:
    X_train = train[:,:-1]
    X_val = val[:,:-1]
    X_test = test

  Y_train = train[:,-1].astype(int)[:,np.newaxis]
  Y_val = val[:,-1].astype(int)[:,np.newaxis]

  logging.info("Loaded train: " + str(X_train.shape))
  logging.info("Loaded val: " + str(X_val.shape))
  logging.info("Loaded test: "+ str(X_test.shape)) 

  return X_train, Y_train, X_val, Y_val, X_test


def displayExample(x):
  plt.imshow(x.reshape(28,28),cmap="gray")
  plt.show()


if __name__=="__main__":
  main()