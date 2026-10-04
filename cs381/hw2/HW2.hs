--- name: Lyon Kee
--- date: 4/18/2023

module HW2  where
import HW2types


-- Q1.a) sizeTree; computes size by adding nodes
    -- Input: Tree
    -- Output: Int
sizeTree :: Tree -> Int
sizeTree Leaf = 0
sizeTree (Node n l r) = 1 + sizeTree l + sizeTree r


-- Q1.b) height; height(layer) of tree
    -- Input: Tree
    -- Output: Int
height :: Tree -> Int
height Leaf = -1
height (Node n l r) = 1 + maximum[height l, height r]


-- Q1.c) treeSum; Sum of all Nodes in a Tree
    -- Input: Tree
    -- Output: Int
treeSum :: Tree -> Int
treeSum Leaf = 0
treeSum (Node n l r) = n + treeSum l + treeSum r


-- Helper function to convert a tree to an array of node values
treeToArr :: Tree -> [Int]
treeToArr Leaf = []
treeToArr (Node n l r) = treeToArr l ++ [n] ++ treeToArr r


-- Q1.d) Overload Equivalence; Overload the equivalence to evaluate if two trees contain the same values
-- Two leafs are True
-- If it is a leaf and a tree, the wildcard equates it as False
    -- Input: Tree -> Tree
    -- Output: Bool
instance Eq Tree where
    (==) Leaf Leaf = True
    (==) (Node n1 l1 r1) (Node n2 l2 r2) = includes (treeToArr (Node n1 l1 r1)) (treeToArr (Node n2 l2 r2)) && includes (treeToArr (Node n2 l2 r2)) (treeToArr (Node n1 l1 r1))
        where
            includes [] a = True
            includes (x:xs) a = elem x a && includes xs a
    (==) _ _ = False


-- Helper function to adds a node to a tree in BST order where left <= n < right
insertBST :: Int -> Tree -> Tree
insertBST n Leaf = (Node n Leaf Leaf)
insertBST x (Node n l r)
    | x <= n = (Node n (insertBST x l) r)
    | otherwise = (Node n l (insertBST x r))
-- Q1.e) mergeTrees; merges two trees by adding another tree's value to a tree with insertBST function
-- Merging a Leaf and a tree, we return the tree
-- Merging two Leafs yield a Leaf
-- We use foldr to continuously apply the insertBST function to the t1 tree with values from t2 in an array form given by treeToArr
    -- Input: Tree -> Tree
    -- Output: Tree
mergeTrees :: Tree -> Tree -> Tree
mergeTrees Leaf Leaf = Leaf
mergeTrees t Leaf = t
mergeTrees Leaf t = t
mergeTrees t1 t2 = foldr insertBST t1 (treeToArr t2)


-- Q1.f) isBST; checks if l <= n <= r
-- Checks that the maximum value found on the entire left branch is <= to n and minimum found in the entire right branch is >= n
-- The same checking is recursively applied to the l and r branches
-- minVal fetches the smallest value in the tree
-- maxVal fetches the biggest value in the tree
    -- Input: Tree
    -- Output: Bool
isBST :: Tree -> Bool
isBST Leaf = True
isBST (Node n l r) = (maxVal l <= n) && (minVal r >= n) && isBST l && isBST r
    where
        minVal Leaf = maxBound :: Int
        minVal (Node m Leaf Leaf) = m
        minVal (Node m l r) = minimum([m, minVal l, minVal r])
        maxVal Leaf = minBound :: Int
        maxVal (Node m Leaf Leaf) = m
        maxVal (Node m l r) = maximum([m, maxVal l, maxVal r])


-- Q1.g) convertBST; converts a tree to a BST
-- Start with an empty tree and apply insertBST on the new tree until all nodes from the tree is applied
-- This is done through converting the initial tree to an array and using foldr to insert all values into the tree
    -- Input: Tree
    -- Output: Tree
convertBST :: Tree -> Tree
convertBST Leaf = Leaf
convertBST (Node n l r) = foldr insertBST (Node n Leaf Leaf) ((treeToArr l) ++ (treeToArr r))


-- Q2.a) numVE; returns the number of vertices and the number of edges
-- vertices is denoted by the count of unique values found in the graph after converting it to an array
-- Edges is denoted by the number of connection or the length of the graph in this graph data structure
    -- Input: Graph
    -- Output: [(Vertex, edges)]
numVE :: Graph -> (Vertex, Vertex)
numVE [] = (0,0)
numVE g = (length (unique (graphToArr g)), length g)
    where
        unique [] = []
        unique (x:xs)
            | elem x xs = unique xs
            | otherwise = x : unique xs
        graphToArr [] = []
        graphToArr ((x1,x2):xs) = x1 : x2 : graphToArr xs


-- Q2.b) removeLoops; returns a graph with removed self loops
-- Create a list from the given list such that no tuple include the same first and second values
    -- Input: Graph
    -- Output: Graph
removeLoops :: Graph -> Graph
removeLoops xs = [(x1, x2) | (x1, x2) <- xs, x1 /= x2]



-- Q2.c) removeVertex; returns a graph without a vertex
-- Create a list from the given list such that neither first or second value of the tuple contain the node to remove
    -- Input: Int -> Graph
    -- Output: [(Int, Int)]
removeVertex :: Int -> Graph -> Graph
removeVertex v xs = [(x1,x2) | (x1, x2) <- xs, x1 /= v && x2 /= v]

