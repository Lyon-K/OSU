module HW5sol where
import HW5types

-- This runs the rank checker, if it passes, runs runCmd to process TypeError during execution
run :: Prog -> Stack -> Result
run [] s = A s
run cs s = case rankP cs (length s) of
    Nothing -> RankError
    Just _ -> runCmd cs s

-- this will run until we encounter a Nothing which indicates a run time error/TypeError
runCmd :: Prog -> Stack -> Result
runCmd [] s = A s
runCmd (c:cs) s = case semCmd c s of
    Nothing -> TypeError
    Just s' -> runCmd cs s'

semCmd :: Cmd -> Stack -> Maybe Stack
-- Push a Int to the stack
semCmd (LDI n) s = Just ((I n):s)
-- Push a Bool to the stack
semCmd (LDB n) s = Just ((B n):s)
-- Remove 2 rights and push the sum to the stack as Int
semCmd ADD ((I a):(I b):s) = Just ((I (a + b)):s)
-- Remove 2 rights and push the product to the stack as Int
semCmd MULT ((I a):(I b):s) = Just ((I (a * b)):s)
-- Push the duplicated element and the removed element back to the stack
semCmd DUP (a:s) = Just (a:a:s)
-- Remove 2 Ints and push the value of `a<=b` to stack as Bool
semCmd LEQ ((I a):(I b):s) = Just((B (a <= b)):s)
-- Remove the first element, x, assert x is Bool, then run p1 if x else p2
semCmd (IFELSE p1 p2) (x:s) = case x of
    B x -> if x then runCase p1 else runCase p2
    _ -> Nothing
    where
        runCase p = case runCmd p s of
            A s -> Just s
            _ -> Nothing
-- Decrements the topmost element on the stack
semCmd DEC (a:s) = case a of
    I a -> Just ((I (a-1)) : s)
    _ -> Nothing
-- Swaps the two topmost elements on the stack
semCmd SWAP (a:b:s) =  Just (b:a:s)
-- Pops the first k elementnts off the stack by dropping them
semCmd (POP k) s = Just(drop k s)
-- semCmd (POP _) [] = Just([])
-- Everything else not mentioned above is a `Nothing`
semCmd _ _ = Nothing

-- maps each command to the stack element poped and pushed
rankC :: Cmd -> CmdRank
rankC c = case c of
    -- LDI pops 0 elements from the stack and pushes 1 elements to it
    LDI _ -> (0, 1)
    -- ADD pops 2 elements from the stack and pushes 1 elements to it
    ADD -> (2, 1)
    -- MULT pops 2 elements from the stack and pushes 1 elements to it
    MULT -> (2, 1)
    -- DUP pops 1 elements from the stack and pushes 2 elements to it
    DUP -> (1, 2)
    -- DEC pops 1 elements from the stack and pushes 1 elements to it
    DEC -> (1, 1)
    -- SWAP pops 2 elements from the stack and pushes 2 elements to it
    SWAP -> (2, 2)
    -- POP pops k elements from the stack and pushes 0 elements to it
    POP k -> (k, 0)
    -- IFELSE pops 1 elements from the stack and pushes 0 elements to it
    IFELSE p1 p2-> (1, 0)
    -- LDB pops 0 elements from the stack and pushes 1 elements to it
    LDB _-> (0, 1)
    -- LEQ pops 2 elements from the stack and pushes 1 elements to it
    LEQ -> (2, 1)

rankP :: Prog -> Rank -> Maybe Rank
-- handles IFELSE by subtracting 1 from rank because IFELSE pops 1 element from the stack to determine direction
rankP ((IFELSE (c1: p1) (c2: p2)):cs) r
    -- Return rankP cs of the minimum rank between p1 and p2
    | fst rank1 <= r && fst rank2 <= r = let minRank = (min (rankP p1 (r-1 - fst rank1 + snd rank1)) (rankP p2 (r-1 - fst rank2 + snd rank2))) in
        case minRank of
            -- If either p1 or p2 results in error, return Nothing
            Nothing -> Nothing
            Just minRank -> rankP cs minRank
    -- if rank is lesser than either p1 or p2's popped elements, return Nothing
    | otherwise = Nothing
        where
            rank1 = rankC c1
            rank2 = rankC c2
-- depending on the command, stack will be poped `fst rank` elements and pushed `snd rank` elements
rankP (c: cs) r
    | fst rank <= r = rankP cs (r - fst rank + snd rank)
    -- if rank is lesser than the number of popped elements, return Nothing
    | otherwise = Nothing
        where rank = rankC c
-- no commannds will return the rank number
rankP [] r = Just r
