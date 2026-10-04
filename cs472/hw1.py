#Q1.1
a1 = 32 * 0 + 3 * 0.05 + 2 * 0.05 + 1 * 0.7 + 2 * 0.2
print("Q1:", a1)

#Q1.2
a2 = 32 * 0.05 + 3 * 0.25 + 2 * 0.25 + 1 * 0.15 + 2 * 0.3
print("Q2:", a2)

#Q1.3
a3 = 0.05/0.25
print("Q3: ", a3)

#Q1.4
# pA_InstructionCount = 150 / 1.35 / 1
pA_InstructionCount = 150 / a1 / 1
# pB_InstructionCount = pA_InstructionCount * 0.2
pB_InstructionCount = pA_InstructionCount * a3
# pBCPUTime = pB_InstructionCount * 3.6 * 1.2
pBCPUTime = pB_InstructionCount * a2 * 1.2
print("Q4: ", pBCPUTime)

#Q7
loop2 = 7
loop1 = 5
((loop2 * 6) + loop1) * 6

#Q3.1
IMem = 550
control = 100
mux = 10
regs = 225
signExtend = 50
alu = 270
DMem = 650
print("Q3.1: ", IMem + max(control + mux, regs, signExtend) + mux + alu + DMem + mux + regs)