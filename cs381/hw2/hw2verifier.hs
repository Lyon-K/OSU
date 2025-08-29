--- Code provided by Evan Hock on Piazza
--- This is similar to a verifier used to test your code when grading
--- To use  ghci hw2verifier.hs   and then main in the interrepter
--- OR
--- ghc hw2verifier.hs  and then run the executable hw2verifier

module Main where 
import HW2types
import HW2

import Control.Applicative (liftA2)
import Control.Monad (join)


graph2 = zip [1, 2, 3, 1, 1] [2, 3, 4, 1, 3]
graph3 = [(1, 1)]
graph4 = [(1, 2), (2, 1)]
graph5 = zip [1, 3, 2, 3, 4, 6, 5, 1, 6] [3, 2, 6, 4, 6, 5, 1, 1, 6]
graph6 = zip [1, 2, 2, 3, 3, 4, 5, 6] [5, 3, 6, 4, 6, 5, 6, 6]


-- trees
ts = [Leaf, tree1, tree2, tree3, tree4, tree5, tree6]


-- tree answers
test1 = [0, 1, 5, 5, 4, 4, 5]
test2 = [-1, 0, 2, 2, 3, 2, 3]
test3 = [0, 5, 26, 32, 10, 23, 34]
test4 = [x == y | let xs = [1..length ts], x <- xs, y <- xs]
test5 = [True, True, False, True, True, False, False]
test6 = replicate 6 True
test7 = [ Node 5 Leaf Leaf
        , Node 5 Leaf Leaf
        , Node 5 
            (Node 2
                Leaf
                (Node 3 Leaf Leaf)) 
            (Node 8
                (Node 6
                    Leaf
                    (Node 7 Leaf Leaf))
                Leaf)
        , Node 5
            (Node 2
                Leaf
                (Node 3 Leaf Leaf))
            (Node 8
                Leaf
                (Node 10
                    (Node 9 Leaf Leaf)
                    Leaf))
        , Node 5
            (Node 4
                (Node 3
                    (Node 2
                        (Node 1 Leaf Leaf)
                        Leaf)
                    Leaf)
                Leaf)
            Leaf
        , Node 5
            (Node 4
                (Node 3 Leaf Leaf)
                Leaf)
            (Node 6
                Leaf
                (Node 10 Leaf Leaf)
            )
        , Node 5
            (Node 4
                (Node 2 Leaf Leaf)
                Leaf)
            (Node 10
                (Node 7 Leaf Leaf)
                (Node 11 Leaf Leaf))
        ]


-- graphs
gs = [graph1, graph2, graph3, graph4, graph5, graph6]


-- graph answers
test8 = zip [6, 4, 1, 2, 6, 6] [7, 5, 1, 2, 9, 8]
test9 = [ zip [1, 2, 4, 5, 6] [2, 4, 3, 6, 5]
        , zip [1, 2, 3, 1] [2, 3, 4, 3]
        , []
        , [(1, 2), (2, 1)]
        , zip [1, 3, 2, 3, 4, 6, 5] [3, 2, 6, 4, 6, 5, 1]
        , zip [1, 2, 2, 3, 3, 4, 5] [5, 3, 6, 4, 6, 5, 6]
        ]
test10 = [ zip [2, 2, 4, 3, 5, 6] [2, 4, 3, 3, 6, 5]
        , zip [4, 3, 5, 6] [3, 3, 6, 5]
        , graph1
        , []
        , []
        ]


successFailure :: Bool -> String -> IO ()
successFailure True = (putStr "\ESC[1;32m[Success]\ESC[0m ">>) . putStrLn
successFailure False = (putStr "\ESC[1;31m[Failure]\ESC[0m ">>) . putStrLn


validate :: (Eq b, Show b) => (a -> b) -> a -> b -> IO ()
validate f x y =
    let
        result = f x
    in
        successFailure (result == y) $ "Actual: " ++ show result ++ " Expected: " ++ show y


test :: (Eq b, Show b) => [a] -> (a -> b) -> [b] -> IO ()
test xs f ys = do
    sequence_ $ zipWith (validate f) xs ys
    putChar '\n'


treeTest :: (Eq a, Show a) => (Tree -> a) -> [a] -> IO ()
treeTest = test ts


graphTest :: (Eq a, Show a) => (Graph -> a) -> [a] -> IO ()
graphTest = test gs

main = do
    putStrLn "Part 1: TREES\n"

    putStrLn "Test 1: sizeTree"
    treeTest sizeTree test1

    putStrLn "Test 2: height"
    treeTest height test2

    putStrLn "Test 3: treeSum"
    treeTest treeSum test3

    putStrLn "Test 4: Eq instance"
    test (join (liftA2 (==)) ts) id test4

    putStrLn "Test 5: isBST"
    treeTest isBST test5

    putStrLn "CAUTION! The results here depend on your isBST definition being correct!"
    putStrLn "Test 6: convertBST"
    test (map convertBST ts) isBST test6

    putStrLn "CAUTION! The results here depend on your Eq instance being correct!"
    putStrLn "Test 7: mergeTrees"
    treeTest (mergeTrees tree1) test7

    putStrLn "Part 2: GRAPHS\n"
    putStrLn "Test 8: numVE"
    graphTest numVE test8


    putStrLn "Test 9: removeLoops"
    graphTest removeLoops test9

    putStrLn "Test 10: removeVertex"
    test (zipWith removeVertex [1, 2, 8, 1, 1] $ replicate 3 graph1 ++ [[], graph3]) id test10
