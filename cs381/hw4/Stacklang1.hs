module Stacklang1 where

type Prog = [Cmd]
data Cmd 
    = LD Int
    | ADD
    | MULT
    | DUP
    deriving Show
type Stack = [Int]

run :: Prog -> Stack -> Maybe Stack
run [] s = Just s
run (c:cs) s = case semCmd c s of
    Nothing -> Nothing
    Just s' -> run cs s'

semCmd :: Cmd -> Stack -> Maybe Stack
-- Push n to the stack
semCmd (LD n) s = Just (n:s)
-- Remove first 2 and push the sum to the stack
semCmd ADD (a:b:s) = Just ((a + b):s)
-- Remove first 2 and push the product to the stack
semCmd MULT (a:b:s) = Just ((a * b):s)
-- Push the duplicated element and the removed element back to the stack
semCmd DUP (a:s) = Just (a:a:s)
-- Everything else not mentioned above is a `Nothing`
semCmd _ _ = Nothing
