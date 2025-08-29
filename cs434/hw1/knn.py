import numpy as np
import time

def main():

    #############################################################
    # These first bits are just to help you develop your code
    # and have expected ouputs given. All asserts should pass.
    ############################################################

    # I made up some random 3-dimensional data and some labels for us
    example_train_x = np.array([ [ 1, 0, 2], [3, -2, 4], [5, -2, 4],
                                 [ 4, 2, 1.5], [3.2, np.pi, 2], [-5, 0, 1]])
    example_train_y = np.array([[0], [1], [1], [1], [0], [1]])
  
    #########
    # Sanity Check 1: If I query with examples from the training set 
    # and k=1, each point should be its own nearest neighbor
    
    # for i in range(len(example_train_x)):
    #     assert([i] == get_nearest_neighbors(example_train_x, example_train_x[i], 1))
        
    # #########
    # # Sanity Check 2: See if neighbors are right for some examples (ignoring order)
    # nn_idx = get_nearest_neighbors(example_train_x, np.array( [ 1, 4, 2] ), 2)
    # assert(set(nn_idx).difference(set([4,3]))==set())

    # nn_idx = get_nearest_neighbors(example_train_x, np.array( [ 1, -4, 2] ), 3)
    # assert(set(nn_idx).difference(set([1,0,2]))==set())

    # nn_idx = get_nearest_neighbors(example_train_x, np.array( [ 10, 40, 20] ), 5)
    # assert(set(nn_idx).difference(set([4, 3, 0, 2, 1]))==set())

    # #########
    # # Sanity Check 3: Neighbors for increasing k should be subsets
    # query = np.array( [ 10, 40, 20] )
    # p_nn_idx = get_nearest_neighbors(example_train_x, query, 1)
    # for k in range(2,7):
    #   nn_idx = get_nearest_neighbors(example_train_x, query, k)
    #   assert(set(p_nn_idx).issubset(nn_idx))
    #   p_nn_idx = nn_idx
   
    # #########
    # # Test out our prediction code
    # queries = np.array( [[ 10, 40, 20], [-2, 0, 5], [0,0,0]] )
    # pred = predict(example_train_x, example_train_y, queries, 3)
    # assert( np.all(pred == np.array([[0],[1],[0]])))

    # #########
    # # Test our our accuracy code
    # true_y = np.array([[0],[1],[2],[1],[1],[0]])
    # pred_y = np.array([[5],[1],[0],[0],[1],[0]])                    
    # assert( compute_accuracy(true_y, pred_y) == 3/6)

    # pred_y = np.array([[5],[1],[2],[0],[1],[0]])                    
    # assert( compute_accuracy(true_y, pred_y) == 4/6)



    #######################################
    # Now on to the real data!
    #######################################

    # Load training and test data as numpy matrices 
    train_X, train_y, test_X = load_data()


    #######################################
    # Q9 Hyperparmeter Search
    #######################################

    # Search over possible settings of k
    print("Performing 4-fold cross validation")
    # for k in [70,80]:
    # # for k in [75]:
    #     t0 = time.time()

    #     #######################################
    #     # TODO Compute train accuracy using whole set
    #     #######################################
    #     # pred_train_y = []
    #     # for i in range(len(train_X)):
    #     #     pred_train_y.append([knn_classify_point(train_X, train_y, train_X[i], k)])
    #     # train_acc = compute_accuracy(train_y, pred_train_y)
    #     train_acc = 0
    #     #######################################
    #     # TODO Compute 4-fold cross validation accuracy
    #     #######################################
    #     num_folds = 4
    #     val_acc, val_acc_var = cross_validation(train_X, train_y, num_folds, k)
    #     t1 = time.time()
    #     print("k = {:5d} -- train acc = {:.2f}%  val acc = {:.2f}% ({:.4f})\t\t[exe_time = {:.2f}]".format(k, train_acc*100, val_acc*100, val_acc_var*100, t1-t0))
        
    
    #######################################


    #######################################
    # Q10 Kaggle Submission
    #######################################


    # TODO set your best k value and then run on the test set
    best_k = 70

    # Make predictions on test set
    pred_test_y = predict(train_X, train_y, test_X, best_k)    
    
    # add index and header then save to file
    test_out = np.concatenate((np.expand_dims(np.array(range(2000),dtype=np.int), axis=1), pred_test_y), axis=1)
    header = np.array([["id", "income"]])
    test_out = np.concatenate((header, test_out))
    np.savetxt('test_predicted.csv', test_out, fmt='%s', delimiter=',')

######################################################################
# Q7 get_nearest_neighbors 
######################################################################
# Finds and returns the index of the k examples nearest to
# the query point. Here, nearest is defined as having the 
# lowest Euclidean distance. This function does the bulk of the
# computation in kNN. As described in the homework, you'll want
# to use efficient computation to get this done. Check out 
# the documentaiton for np.linalg.norm (with axis=1) and broadcasting
# in numpy. 
#
# Input: 
#   example_set --  a n-by-d matrix of examples where each row
#                   corresponds to a single d-dimensional example
#
#   query --    a 1-by-d vector representing a single example
#
#   k --        the number of neighbors to return
#
# Output:
#   idx_of_nearest --   a k-by- list of indices for the nearest k
#                       neighbors of the query point
######################################################################

def get_nearest_neighbors(example_set, query, k):
    #TODO
    distance_index_pair = [ (np.linalg.norm(example - query), i) for i, example in enumerate(example_set) ]
    return sorted(distance_index_pair)[:k]

# as per function description:
#     distance_index_pair = [ (np.linalg.norm(example - query), i) for i, example in enumerate(example_set) ]
#     return [ i for (_, i) in sorted(distance_index_pair) ][:k]


######################################################################
# Q7 knn_classify_point 
######################################################################
# Runs a kNN classifier on the query point
#
# Input: 
#   examples_X --  a n-by-d matrix of examples where each row
#                   corresponds to a single d-dimensional example
#
#   examples_Y --  a n-by-1 vector of example class labels
#
#   query --    a 1-by-d vector representing a single example
#
#   k --        the number of neighbors to return
#
# Output:
#   predicted_label --   either 0 or 1 corresponding to the predicted
#                        class of the query based on the neighbors
######################################################################

def knn_classify_point(examples_X, examples_y, query, k):
    #TODO
    nearest_neighbors = get_nearest_neighbors(examples_X, query, k)
    if k == 1:
        return examples_y[nearest_neighbors[0][1]]
    neighbors_range = nearest_neighbors[-1][0] - nearest_neighbors[0][0]
    if neighbors_range == 0:
        predicted_score = sum((examples_y[idx]) for (dist, idx) in nearest_neighbors)
        return int(predicted_score > k/2)
    furthest_dist = nearest_neighbors[-1][0]
    total_weight = 0
    sum = 0
    for (dist, idx) in nearest_neighbors:
        weight = abs(dist - furthest_dist)/(float(neighbors_range))*0.1 + 0.9
        # print('weight: ', weight)
        total_weight += weight
        sum += examples_y[idx] * weight
    return int(sum > total_weight/2)
    # pred
# as per function description:
#     predicted_score = sum((examples_y[idx]) for idx in get_nearest_neighbors(examples_X, query, k))
#     return int(predicted_score > k/2)


######################################################################
# Q8 cross_validation 
######################################################################
# Runs K-fold cross validation on our training data.
#
# Input: 
#   train_X --  a n-by-d matrix of examples where each row
#                   corresponds to a single d-dimensional example
#
#   train_Y --  a n-by-1 vector of example class labels
#
# Output:
#   avg_val_acc --      the average validation accuracy across the folds
#   var_val_acc --      the variance of validation accuracy across the folds
######################################################################

def cross_validation(train_X, train_y, num_folds=4, k=1):
    #TODO
    k_folds_train_X = np.split(train_X, num_folds)
    k_folds_train_y = np.split(train_y, num_folds)
    accuracy_arr = []
    for i in range(num_folds):
        print("training fold: ", i)
        pred_train_y = []
        validate_data_X = k_folds_train_X[i]
        validate_data_y = k_folds_train_y[i]
        train_data_X = np.vstack(np.delete(k_folds_train_X, i, axis = 0))
        train_data_y = np.vstack(np.delete(k_folds_train_y, i, axis = 0))
        for x in validate_data_X:
            pred_train_y.append([knn_classify_point(train_data_X, train_data_y, x, k)])
        accuracy_arr.append(compute_accuracy(validate_data_y, pred_train_y))
    # print(f'TEMP: num_folds={num_folds} len(accuracy_arr) = {len(accuracy_arr)}')
    avg_val_acc = np.mean(accuracy_arr)
    varr_val_acc = np.var(accuracy_arr)

    return avg_val_acc, varr_val_acc



##################################################################
# Instructor Provided Code, Don't need to modify but should read
##################################################################


######################################################################
# compute_accuracy 
######################################################################
# Runs a kNN classifier on the query point
#
# Input: 
#   true_y --  a n-by-1 vector where each value corresponds to 
#              the true label of an example
#
#   predicted_y --  a n-by-1 vector where each value corresponds
#                to the predicted label of an example
#
# Output:
#   predicted_label --   the fraction of predicted labels that match 
#                        the true labels
######################################################################

def compute_accuracy(true_y, predicted_y):
    accuracy = np.mean(true_y == predicted_y)
    return accuracy

######################################################################
# Runs a kNN classifier on every query in a matrix of queries
#
# Input: 
#   examples_X --  a n-by-d matrix of examples where each row
#                   corresponds to a single d-dimensional example
#
#   examples_Y --  a n-by-1 vector of example class labels
#
#   queries_X --    a m-by-d matrix representing a set of queries 
#
#   k --        the number of neighbors to return
#
# Output:
#   predicted_y --   a m-by-1 vector of predicted class labels
######################################################################

def predict(examples_X, examples_y, queries_X, k): 
    # For each query, run a knn classifier
    predicted_y = [knn_classify_point(examples_X, examples_y, query, k) for query in queries_X]

    return np.array(predicted_y,dtype=np.int)[:,np.newaxis]

# Load data
def load_data():
    traindata = np.genfromtxt('train.csv', delimiter=',')[1:, 1:]
    train_X = traindata[:, :-1]
    train_y = traindata[:, -1]
    train_y = train_y[:,np.newaxis]
    
    test_X = np.genfromtxt('test_pub.csv', delimiter=',')[1:, 1:]

    return train_X, train_y, test_X


    
if __name__ == "__main__":
    main()