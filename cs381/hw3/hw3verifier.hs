import Sentence


main:: IO()
main = do
	let s1 = buildS2 Cats Hug Goats
	let s2 = buildS1 Cats Cuddle
	let s3 = buildNP Sad Bears
	let s4 = buildNAnd Dogs Cats
	let s5 = conjunction [s2, s1]
	let s6 = buildS2 s3 Chase s4	
	let s7 = buildS1 Dogs Scare
	let s8 = conjunction [s1, s2, s7]
	let s9 = buildNP Big s3
	let s10 = buildS2 s9 Cuddle Cats
	let s11 = conjunction[s1, s1]
	let s12 = conjunction[s6, s7]
	let s13 = buildS2 Cats Scare Dogs

-- pretty print
	putStrLn "P5) b. Pretty print"
	print(pretty(s1))
	if ((pretty(s1)) == "cats hug goats") then print ("Pass s1")
	else print ("Fail s1")
	
	print(pretty(s2))	
	if ((pretty(s2)) == "cats cuddle") then print ("Pass s2")
	else print ("Fail s2")
	
	print(pretty(s5))
	if ((pretty(s5)) == "cats cuddle and cats hug goats") then print ("Pass s5")
	else print ("Fail s5")

	print(pretty(s6))	
	if ((pretty(s6)) == "sad bears chase dogs and cats") then print ("Pass s6")
	else print ("Fail s6")

	print(pretty(s7))
	if ((pretty(s7)) == "dogs scare") then print ("Pass s7")
	else print ("Fail s7")
	
	print(pretty(s8))
	if ((pretty(s8)) == "cats hug goats and cats cuddle and dogs scare") then print ("Pass s8")
	else print ("Fail s8")
	
-- build a sentence
	putStrLn " "
	putStrLn "P5) c. Build a sentence"
	print(pretty(s1))
	if ((s1) == NVN Cats Hug Goats) then print ("Pass s1")
	else print ("Fail s1")
		
	if ((s2) == NV Cats Cuddle) then print ("Pass s2")
	else print ("Fail s2")
	
	if ((s3) == NP Sad Bears) then print ("Pass s3")
	else print ("Fail s3")
	
	if ((s4) == NAnd Dogs Cats) then print ("Pass s4")
	else print ("Fail s4")
	
	if ((s10) == NVN (NP Big (NP Sad Bears)) Cuddle Cats) then print ("Pass s10")
	else print ("Fail s10")
	
-- isMean
	putStrLn " "
	putStrLn "P5) d. isMean "
	print(pretty(s1))
	if ((isMean s1)== False) then print ("Pass s1 - Not mean")
	else print ("Fail s1")
	
	print(pretty(s5))
	if ((isMean s5) == False) then print ("Pass s5 - Not mean")
	else print ("Fail s5")
	
	print(pretty(s6))
	if ((isMean s6) == True) then print ("Pass s6 - mean")
	else print ("Fail s6")
	
	print(pretty(s8))
	if ((isMean s8) == False) then print ("Pass s8 - not mean")
	else print ("Fail s8")
	
	print(pretty(s12))	
	if ((isMean s12) == True) then print ("Pass s12 - mean")
	else print ("Fail s12")
	
	print(pretty(s13))	
	if ((isMean s13) == True) then print ("Pass s13 - mean")
	else print ("Fail s13")
	
-- conjunction
	putStrLn " "
	putStrLn "P5) e. conjunction "	
	if ((s5) == And (NV Cats Cuddle) (NVN Cats Hug Goats)) then print ("Pass s5")
	else print ("Fail s5")
	
	if ((s8) == And (NVN Cats Hug Goats) (And (NV Cats Cuddle) (NV Dogs Scare))) then print ("Pass s8")
	else print ("Fail s8")	
	
	if ((s11) == And (NVN Cats Hug Goats) (NVN Cats Hug Goats)) then print ("Pass s11") 
	else print ("Fail s11")
	
	if (conjunction[NV Cats Hug] == (NV Cats Hug)) then print ("Pass Cat test")
	else print("Fail Cat test")

-- word count
	putStrLn " "
	putStrLn "P5) f. wordCount "	
	if ((wordCount s1) == 3) then print ("Pass s1")
	else print ("Fail s1")
		
	if ((wordCount s2) == 2) then print ("Pass s2")
	else print ("Fail s2")
	
	if ((wordCount s5)  == 6) then print ("Pass s5")
	else print ("Fail s5")
	
	if ((wordCount s6) == 6) then print ("Pass s6")
	else print ("Fail s6")
	
	if ((wordCount s8) == 9) then print ("Pass s8")
	else print ("Fail s8")
	
	if ((wordCount s10) == 5) then print ("Pass s10")
	else print ("Fail s10")
