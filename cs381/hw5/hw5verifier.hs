import HW5sol
import HW5types

import Text.Printf (printf)

-- test programs
p1 = [LDI 3, DUP, ADD, LDI 5, SWAP] 
p2 = [LDI 8, POP 1, LDI 3, DUP, POP 2, LDI 4] 
p3 = [LDI 3, LDI 4, LDI 5, MULT, ADD] 
p4 = [DUP] 
p5 = [POP 4] 
p6 = [LDB True, IFELSE [ADD] [LDI 7], ADD ]
p7 = [LDB True, LDI 1, LDI 10, LDI 5, IFELSE [ADD] [LDI 7], ADD ]
p8 = [LDI 20, LDI 1, LDI 10, LDI 5, LEQ, IFELSE [ADD] [LDI 7], DUP ]
p9 = [LDB True, LDB False, MULT]
p10 = [LDI 10, DEC, DUP, DUP, DUP, POP 2]
p11 = [LDI 10, LDI 20, LEQ, DEC]
p12 = [LDI 10, LDI 5, LDB True, IFELSE [LDB True, IFELSE [ADD, DUP] [MULT]] [LDI 7] ]
p13 = [LDI 10, LDI 5, LDB True, IFELSE [LDB False, IFELSE [ADD, DUP] [MULT]] [LDI 7] ]
p14 = [LDI 10, LDI 5, LDB False, IFELSE [LDB True, IFELSE [ADD, DUP] [MULT]] [LDI 7] ]
p15 = [LDI 10, LDI 5, LDB False, IFELSE [LDB True, IFELSE [ADD, ADD] [MULT]] [LDI 7] ]
pList = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15]

-- test stacks
s1 = [B True]
s2 = [I 2]
s3 = [I 1, I 3]
s4 = [B False, I 4, I 7]
s5 = [I 1, I 4, I 6]
s6 = [I 10]
s7 = [I 100, I 6]
s8 = [I 10, I 20, I 1]
s9 = [I 3, I 8]
s10 = [I 1, I 4, I 6]
s11 = [I 10]
s12 = [I 100, I 6]
s13 = [I 10, I 20, I 1]
s14 = [I 3, I 8]
s15 = [I 3, I 8]
sList = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15]
eList = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]


-- empty `rank` results
rankE1 = Just 2
rankE2 = Just 1
rankE3 = Just 1
rankE4 = Nothing
rankE5 = Nothing
rankE6 = Nothing
rankE7 = Just 1
rankE8 = Just 2
rankE9 = Just 1
rankE10 = Just 2
rankE11 = Just 1
rankE12 = Just 1
rankE13 = Just 1
rankE14 = Just 1
rankE15 = Nothing
rankEs = [rankE1, rankE2, rankE3, rankE4, rankE5, rankE6, rankE7, rankE8, rankE9, rankE10, rankE11, rankE12, rankE13, rankE14, rankE15]


-- expected `rank` results
rank1 = Just 3
rank2 = Just 2
rank3 = Just 3
rank4 = Just 4
rank5 = Nothing
rank6 = Nothing
rank7 = Just 3
rank8 = Just 5
rank9 = Just 3
rank10 = Just 5
rank11 = Just 2
rank12 = Just 3
rank13 = Just 4
rank14 = Just 3
rank15 = Just 2
ranks = [rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9, rank10, rank11, rank12, rank13, rank14, rank15]


-- empty `run` results
runE1 = A [I 6, I 5]
runE2 = A [I 4]
runE3 = A [I 23]
runE4 = RankError
runE5 = RankError
runE6 = RankError
runE7 = TypeError
runE8 = A [I 21, I 21]
runE9 = TypeError
runE10 = A [I 9, I 9]
runE11 = TypeError
runE12 = A [I 15, I 15]
runE13 = A [I 50]
runE14 = A [I 7, I 5, I 10]
runE15 = RankError
runEs = [runE1, runE2, runE3, runE4, runE5, runE6, runE7, runE8, runE9, runE10, runE11, runE12, runE13, runE14, runE15]


-- expected `run` results
run1 = A [I 6, I 5, B True]
run2 = A [I 4, I 2]
run3 = A [I 23, I 1, I 3]
run4 = A [B False, B False, I 4, I 7]
run5 = RankError
run6 = RankError
run7 = TypeError
run8 = A [I 21, I 21, I 10, I 20, I 1]
run9 = TypeError
run10 = A [I 9, I 9, I 1, I 4, I 6]
run11 = TypeError
run12 = A [I 15, I 15, I 100, I 6]
run13 = A [I 50, I 10, I 20, I 1]
run14 = A [I 7, I 5, I 10, I 3, I 8]
run15 = A [I 7, I 5, I 10, I 3, I 8]
runs = [run1, run2, run3, run4, run5, run6, run7, run8, run9, run10, run11, run12, run13, run14, run15]


test :: (Show a, Show b, Show c, Eq c) => String -> (a -> b -> c) -> a -> b -> c -> IO () 
test fname f x y expected = do
    let result = f x y
    printf "%s %s %s -> %s " fname (show x) (show y) (show result)
    if result == expected then
        putStrLn "\ESC[1;32m[SUCCESS]\ESC[0m"
    else
        printf "\ESC[1;31m[FAILURE]\ESC[0m Expected %s\n" $ show expected


testBatch :: (Show a, Show b, Show c, Eq c) => String -> String -> (a -> b -> c) -> [a] -> [b] -> [c] -> IO ()
testBatch msg fname f xs ys expects = do
    printf "\ESC[3;34m%s\ESC[0m\n" msg
    sequence_ $ zipWith3 (test fname f) xs ys expects
    putChar '\n'


rankTests :: String -> [Stack] -> [Maybe Rank] -> IO ()
rankTests msg = testBatch msg "rankP" rankP pList . map length


runTests :: String -> [Stack] -> [Result] -> IO ()
runTests msg = testBatch msg "run" run pList


main = do
    rankTests "Empty stack rank tests" eList rankEs
    rankTests "Rank tests" sList ranks
    runTests "Empty runs" eList runEs
    runTests "Runs" sList runs