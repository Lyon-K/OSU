-- Homework 3 template
module Sentence where

-- Grammar for the animal sentence language:
--
--   <sentence> ->  <noun> <verb> [<noun>]  
--               	|  <sentence> `and` <sentence>
--				 	
--   <noun> 	-> <adj> <noun> | <noun> `and` <noun>
--					| `cats` | `dogs` | `bears` | `goats`
--
--   <verb>		->  `chase` | `cuddle` | `hug` | `scare`
--   <adj>		->	`sad` | `small` | `big` | `happy`
 
data Sentence
   = NVN Noun Verb Noun -- finish noun verb noun sentence
   | NV Noun Verb -- finish noun verb sentence
   | And Sentence Sentence -- finish sentence and sentence
   | End
  deriving (Eq,Show)

data Adj = Sad | Small | Big | Happy -- finish adjectives
  deriving (Eq,Show)

-- data Noun =  -- finish
data Noun = NP Adj Noun  -- Noun phrase
    | NAnd Noun Noun  -- Finish noun and noun
	  | Cats | Dogs | Bears | Goats		  -- list of nouns
  deriving (Eq,Show)

data Verb = Chase | Cuddle | Hug | Scare -- finish

  deriving (Eq,Show)



ex1 :: Sentence
ex1 = NVN Cats Hug Dogs

ex2 :: Sentence
ex2 = NVN (NP Small Cats) Hug Dogs

ex3 :: Sentence
ex3 = NVN (NAnd Dogs Cats) Chase Goats

ex4 :: Sentence
ex4 = NVN (NAnd (NP Happy Dogs) Cats) Chase Goats


-- | Build a sentence from a noun verb noun.
-- | buildS2 Cats Hug Cats
-- | NVN Cats Hug Cats

buildS2 :: Noun -> Verb ->Noun-> Sentence
buildS2 n1 v n2 = NVN n1 v n2
-- finish

-- | Build a sentence from a noun verb 
-- | buildS1 Cats Hug 
-- | NV Cats Hug 

buildS1 :: Noun -> Verb ->Sentence
buildS1 n v = NV n v
-- finish


-- | Build a noun phrase from an adjective and noun
-- | buildNP Happy Dogs
-- | NP Happy Dogs

buildNP :: Adj -> Noun -> Noun
buildNP a n = NP a n
-- finish

-- | Build a noun conjunction from two nouns
-- | buildNAnd Dogs Cats
-- | NAnd Dogs Cats

buildNAnd :: Noun -> Noun -> Noun
buildNAnd n1 n2 = NAnd n1 n2
-- finish

-- | Build a sentence that is a conjunction of a list of other sentences.
-- | conjunction [ex1, ex2]
-- | And (NVN Cats Hug Dogs) (NVN (NP Small Cats) Hug Dogs)
-- | The End is used if no sentences are given
 
conjunction :: [Sentence] -> Sentence
-- And sentences 1 by 1 recursively until an array of length 1
conjunction (x : xs)  
  | xs == [] = x
  | otherwise = And x (conjunction xs)
-- finish

-- | Pretty print a sentence.
pretty :: Sentence -> String
pretty (NVN s v o) = prettyNoun s ++ " " ++ prettyVerb v ++ " " ++ prettyNoun o
pretty (And l r)   = pretty l ++ " and " ++ pretty r
pretty (NV s v)     = prettyNoun s ++ " " ++ prettyVerb v
pretty (End) = "."

-- | Pretty print a noun.
prettyNoun :: Noun -> String
prettyNoun Cats   = "cats"
prettyNoun Dogs   = "dogs"
prettyNoun Bears  = "bears"
prettyNoun Goats  = "goats"
-- finish


prettyNoun (NP a n) = prettyAdj a ++ " " ++ prettyNoun n
prettyNoun (NAnd m n) = prettyNoun m ++ " and " ++prettyNoun n

-- | Pretty print a verb.
prettyVerb :: Verb -> String
prettyVerb Chase  = "chase"
prettyVerb Cuddle  = "cuddle"
prettyVerb Hug  = "hug"
prettyVerb Scare  = "scare"
-- finish

-- | Pretty print an adjective.
prettyAdj :: Adj -> String
prettyAdj Sad  = "sad"
prettyAdj Small  = "small"
prettyAdj Big  = "big"
prettyAdj Happy  = "happy"
-- finish


-- | Does the sentence contain only chase and scare?
-- | isMean ex2 => False
-- | isMean ex3 => True
isMean :: Sentence -> Bool
-- Map boolean values of all verbs
isMean (NVN _ Chase _)  = True
isMean (NVN _ Scare _)  = True
isMean (NVN _ Cuddle _) = False
isMean (NVN _ Hug _) = False
isMean (NV _ Chase)  = True
isMean (NV _ Scare)  = True
isMean (NV _ Cuddle) = False
isMean (NV _ Hug) = False
-- True only if the sentence contains only mean words
isMean (And s1 s2) = isMean s1 && isMean s2

-- finish

-- |Count the number of words in a sentence
-- | wordCount ex4
--    6

-- Helper function used to count the number of words in Nouns
nounWordCount :: Noun -> Int
-- Add 1 for the terminating Adj
nounWordCount ( NP _ n ) = 1 + nounWordCount n
-- Add 1 for word "and"
nounWordCount ( NAnd n1 n2 ) = nounWordCount n1 + nounWordCount n2 + 1
-- terminating nouns
nounWordCount _ = 1

wordCount :: Sentence -> Int
-- Add 1 for the terminating verb
wordCount ( NVN n1 _ n2 ) = nounWordCount n1 + 1 + nounWordCount n2
-- Add 1 for the terminating verb
wordCount ( NV n _ )  = nounWordCount n + 1
-- Add 1 for the word "and"
wordCount ( And l r ) = wordCount l + wordCount r + 1
-- finish