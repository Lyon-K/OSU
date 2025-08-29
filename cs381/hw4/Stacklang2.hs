module Stacklang2 where

type Prog = [Cmd]
type Stack = [Either Bool Int]
data Cmd
    = LDI Int
    | LDB Bool
    | LEQ
    | ADD
    | MULT
    | DUP
    | IFELSE Prog Prog
    deriving Show

run :: Prog -> Stack -> Maybe Stack
run [] s = Just s
run (c:cs) s = case semCmd c s of
    Nothing -> Nothing
    Just s' -> run cs s'

semCmd :: Cmd -> Stack -> Maybe Stack
-- Push a Right Int to the stack
semCmd (LDI n) s = Just ((Right n):s)
-- Push a Left Bool to the stack
semCmd (LDB n) s = Just ((Left n):s)
-- Remove 2 rights and push the sum to the stack as Right Int
semCmd ADD ((Right a):(Right b):s) = Just ((Right (a + b)):s)
-- Remove 2 rights and push the product to the stack as Right Int
semCmd MULT ((Right a):(Right b):s) = Just ((Right (a * b)):s)
-- Push the duplicated element and the removed element back to the stack
semCmd DUP (a:s) = Just (a:a:s)
-- Remove 2 Right Ints and push the value of `a<=b` to stack as Left Bool
semCmd LEQ ((Right a):(Right b):s) = Just((Left (a <= b)):s)
-- Remove the first element, x, assert x is Left Bool, then run p1 if x else p2
semCmd (IFELSE p1 p2) (x:s) = case x of
    Left x -> if x then run p1 s else run p2 s
-- Everything else not mentioned above is a `Nothing`
semCmd _ _ = Nothing