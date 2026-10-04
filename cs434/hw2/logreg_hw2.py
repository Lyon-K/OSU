import numpy as np
np.random.seed(42)
import matplotlib.pyplot as plt
import logging
logging.basicConfig(
    filename="results.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


# GLOBAL PARAMETERS FOR STOCHASTIC GRADIENT DESCENT
step_size=0.0001
max_iters=2000

# HYPERPARAMETERS
# step_size_hyperparameter = np.hstack((np.arange(0.05, 0.51, 0.01), np.arange(0.0001, 0.001, 0.0001)))
# step_size_hyperparameter = [0.47, 0.36, 0.27, 0.0005, 0.42, 0.32, 0.26, 0.24, 0.21, 0.17]
# step_size_hyperparameter = np.linspace(0.005,0.00005, 100)
k_fold_cross_hyperparameter = [5, 10]
best_n_step_size = 10

def main():

  # Load the training data
  logging.info("Loading data")
  X_train, y_train, X_test = loadData()

  logging.info("\n---------------------------------------------------------------------------\n")

  # Fit a logistic regression model on train and plot its losses
  step_size_acc_arr = []
  X_train_bias = dummyAugment(X_train)
  # for i, step_size in enumerate(step_size_hyperparameter):
  #   logging.info("Training logistic regression model (No Bias Term; step_size={})".format(step_size))
  #   w, losses = trainLogistic(X_train,y_train, step_size=step_size)
  #   y_pred_train = X_train@w >= 0
    
  #   logging.info("Learned weight vector: {}".format([np.round(a,4)[0] for a in w]))
  #   logging.info("Train accuracy: {:.4}%".format(np.mean(y_pred_train == y_train)*100))
    
  #   logging.info("\n---------------------------------------------------------------------------\n")

  
  #   # Fit a logistic regression model on train and plot its losses
  #   logging.info("Training logistic regression model (Added Bias Term; step_size={})".format(step_size))
  #   w, bias_losses = trainLogistic(X_train_bias,y_train, step_size=step_size)
  #   y_pred_train = X_train_bias@w >= 0
    
  #   train_accuracy = np.mean(y_pred_train == y_train)*100
  #   logging.info("Learned weight vector: {}".format([np.round(a,4)[0] for a in w]))
  #   logging.info("Train accuracy: {:.4}%".format(train_accuracy))
  #   step_size_acc_arr.append((train_accuracy, step_size))

  #   plt.figure(figsize=(16,9))
  #   # plt.plot(range(len(losses)), losses, label="No Bias Term Added")
  #   plt.plot(range(len(bias_losses)), bias_losses, label="Bias Term Added")
  #   plt.title(f"Logistic Regression Training Curve(step_size={step_size})")
  #   plt.xlabel("Epoch")
  #   plt.ylabel("Negative Log Likelihood")
  #   plt.legend()
  #   plt.savefig(f"plot_{i}")
  #   plt.close()
  #   plt.show()

  #   logging.info("\n----------------------------------------------------------------------------------------------------\n")
  # # step_size_acc_arr = sorted(step_size_acc_arr, reverse=True)
  # # logging.info("step_size_acc_arr: {}".format(step_size_acc_arr))
  # # step_size_acc_arr = step_size_acc_arr[:best_n_step_size]
  # # logging.info("best {} step sizes: {}".format(best_n_step_size, step_size_acc_arr))
  # # logging.info("\n----------------------------------------------------------------------------------------------------\n")
  # # logging.info("Running cross-fold validation for bias case:")

  # # Perform k-fold cross
  # best_k_acc = -1
  # # best_w = w
  # # best_k = -1
  # best_LL = -1
  # # for _, step_size in step_size_acc_arr:
  # for step_size in step_size_hyperparameter:
  #   for k in k_fold_cross_hyperparameter:
  #     cv_acc, cv_std, w = kFoldCrossVal(X_train_bias, y_train, k, step_size=step_size)
  #     logging.info("{}-fold Cross Val Accuracy(LL={}) -- Mean (stdev): {:.4}% ({:.4}%)".format(k,step_size, cv_acc*100, cv_std*100))
  #     if cv_acc > best_k_acc:
  #       best_k_acc = cv_acc
  #       # best_w = w
  #       # best_k = k
  #       best_LL = step_size

  ####################################################
  # Write the code to make your test submission here
  ####################################################
  best_LL = 0.0029
  logging.info("\n----------------------------------------------------------------------------------------------------\n")
  logging.info(f"Creating Prediction on step_size={best_LL}")
  logging.info("\n----------------------------------------------------------------------------------------------------\n")
  best_w, _ = trainLogistic(X_train_bias,y_train, step_size=best_LL)
  pred_test_y = dummyAugment(X_test)@best_w >= 0
    
  # add index and header then save to file
  test_out = np.concatenate((np.expand_dims(np.array(range(len(X_test)),dtype=int), axis=1), pred_test_y), axis=1)
  header = np.array([["id", "type"]])
  test_out = np.concatenate((header, test_out))
  np.savetxt('test_predicted.csv', test_out, fmt='%s', delimiter=',')

  # raise Exception('Student error: You haven\'t implemented the code in main() to make test predictions.')


######################################################################
# Q3.1 logistic 
######################################################################
# Given an input vector z, return a vector of the outputs of a logistic
# function applied to each input value
#
# Input: 
#   z --   a n-by-1 vector
#
# Output:
#   logit_z --  a n-by-1 vector where logit_z[i] is the result of 
#               applying the logistic function to z[i]
######################################################################
def logistic(z):
  return np.reciprocal(1 + np.exp(-z))


######################################################################
# Q3.2 calculateNegativeLogLikelihood 
######################################################################
# Given an input data matrix X, label vector y, and weight vector w
# compute the negative log likelihood of a logistic regression model
# using w on the data defined by X and y
#
# Input: 
#   X --   a n-by-d matrix of examples where each row
#                   corresponds to a single d-dimensional example
#
#   y --    a n-by-1 vector representing the labels of the examples in X
#
#   w --    a d-by-1 weight bector
#
# Output:
#   nll --  the value of the negative log-likelihood
######################################################################
def calculateNegativeLogLikelihood(X,y,w):
  # nll = 0
  # for x_i, y_i in zip(X, y):
  #   sigmoid = logistic(w.T @ x_i)
  #   nll -= y_i * np.log(sigmoid + 0.000001) + (1 - y_i) * np.log(1 - sigmoid + 0.000001)
  # return nll

  nll = 0
  for x_i, y_i in zip(X, y):
    z = w.T @ x_i
    if z > 0:
      log_logistic = -np.logaddexp(0, -z)
    else:
      log_logistic = -np.log(np.exp(z)+1) + z
    nll -= y_i * log_logistic + (1 - y_i) * np.log(1 - logistic(z) + 0.00000001)
  return nll
  # raise Exception('Student error: You haven\'t implemented the negative log likelihood calculation yet.')

"""
z=1000000
sigmoid(z) = 0 overflow

z = -100000
sigmoid(z) = 1

log
"""


######################################################################
# Q4 trainLogistic
######################################################################
# Given an input data matrix X, label vector y, maximum number of 
# iterations max_iters, and step size step_size -- run max_iters of 
# gradient descent with a step size of step_size to optimize a weight
# vector that minimizies negative log-likelihood on the data defined
# by X and y
#
# Input: 
#   X --   a n-by-d matrix of examples where each row
#                   corresponds to a single d-dimensional example
#
#   y --    a n-by-1 vector representing the labels of the examples in X
# 
#   max_iters --   the maximum number of gradient descent iterations
#
#   step_size -- the step size (or learning rate) for gradient descent
#
# Output:
#   w --  the d-by-1 weight vector at the end of training
#
#   losses -- a list of negative log-likelihood values for each iteration
######################################################################
def trainLogistic(X,y, max_iters=max_iters, step_size=step_size):

    # Initialize our weights with zeros
    w = np.zeros( (X.shape[1],1) )
    
    # Keep track of losses for plotting
    losses = [calculateNegativeLogLikelihood(X,y,w)]
    
    # Take up to max_iters steps of gradient descent
    for _ in range(max_iters):
    
               
        # Todo: Compute the gradient over the dataset and store in w_grad
        # . 
        # . Implement equation 9.
        # . 
        w_grad = X.T @ (logistic(X @ w) - y)
        # raise Exception('Student error: You haven\'t implemented the gradient calculation for trainLogistic yet.')

        # This is here to make sure your gradient is the right shape
        assert(w_grad.shape == (X.shape[1],1))

        # Take the update step in gradient descent
        w = w - step_size*w_grad
        
        # Calculate the negative log-likelihood with the 
        # new weight vector and store it for plotting later
        losses.append(calculateNegativeLogLikelihood(X,y,w))
        
    return w, losses


######################################################################
# Q5 dummyAugment
######################################################################
# Given an input data matrix X, add a column of ones to the left-hand
# side
#
# Input: 
#   X --   a n-by-d matrix of examples where each row
#                   corresponds to a single d-dimensional example
#
# Output:
#   aug_X --  a n-by-(d+1) matrix of examples where each row
#                   corresponds to a single d-dimensional example
#                   where the the first column is all ones
#
######################################################################
def dummyAugment(X):
  return np.column_stack((np.ones(len(X)), X))
  # raise Exception('Student error: You haven\'t implemented dummyAugment yet.')





##################################################################
# Instructor Provided Code, Don't need to modify but should read
##################################################################

# Given a matrix X (n x d) and y (n x 1), perform k fold cross val.
def kFoldCrossVal(X, y, k, step_size=step_size):
  fold_size = int(np.ceil(len(X)/k))
  
  rand_inds = np.random.permutation(len(X))
  X = X[rand_inds]
  y = y[rand_inds]

  acc = []
  inds = np.arange(len(X))
  for j in range(k):
    
    start = min(len(X),fold_size*j)
    end = min(len(X),fold_size*(j+1))
    test_idx = np.arange(start, end)
    train_idx = np.concatenate( [np.arange(0,start), np.arange(end, len(X))] )
    if len(test_idx) < 2:
      break

    X_fold_test = X[test_idx]
    y_fold_test = y[test_idx]
    
    X_fold_train = X[train_idx]
    y_fold_train = y[train_idx]

    w, losses = trainLogistic(X_fold_train, y_fold_train, step_size=step_size)

    acc.append(np.mean((X_fold_test@w >= 0) == y_fold_test))

  return np.mean(acc), np.std(acc), w


# Loads the train and test splits, passes back x/y for train and just x for test
def loadData():
  train = np.loadtxt("train_cancer.csv", delimiter=",")
  test = np.loadtxt("test_cancer_pub.csv", delimiter=",")
  
  X_train = train[:, 0:-1]
  y_train = train[:, -1]
  X_test = test
  
  return X_train, y_train[:, np.newaxis], X_test   # The np.newaxis trick changes it from a (n,) matrix to a (n,1) matrix.


main()
