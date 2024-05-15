# Performance-Aware Programming

## Introduction

- Instructions --> CPU --> completed instructions
- If we want to talk about the performance, we're really just talking about how long, in total, the CPU takes to process that entire set of instructions
- There's really only two things we as programmers can do to change the performance of the program:
  - Reduce the number of instructions, or
  - Increase the speed the instructions move through the CPU.

## Waste

- Examples of x64 instructions for adding two integers in the CPU (usually held in registers or sometimes memory addresses):
  - `ADD` --> `A += B`
  - `LEA` (load effective address) --> `C = A + B`
- Running a simple program that adds `A` and `B` is much slower in Python than C
  - Python first turns the `A + B` into its own instruction stream (instructions meant to be read by the Python interpreter rather than the CPU)
  - When the program is ran, we have to run all the instructions for Python to decode and manage that Python instruction stream, which generates massive numbers of additional instructions
  - The few instructions we actually asked for are sandwiched in between hundreds of instructions we did not ask for and the CPU has to do them all
- As a result, if we want our Python code to run more quickly, we essentially have to look for ways of not using Python. This includes:
  - Using add-ons that that have ways of doing work in bulk (in precompiled C), so we only have to use a little bit of Python to kick off much faster work that can be done in compiled code
  - Finding a JIT that will turn some of our loops into actual streamlined code, so that the Python interpreter will not be involved

## Instructions Per Clock

- Ways to describe CPU performance:
  - **IPC (instructions per clock)** --> the average number of machine instructions the CPU executes on every clock cycle
  - **ILP (instruction-level parallelism)** --> more of a general term used to refer to the fact that a particular CPU is capable of doing some number of instructions at the same time

### Unrolling a Loop

```c
typedef unsigned int u32;
u32 Unroll2Scalar(u32 Count, u32 *Input)
{
	u32 Sum = 0;

  // Go two indices at a time and do two additions in the body of the loop
	for(u32 Index = 0; Index < Count; Index += 2)
	{
		Sum += Input[Index];
		Sum += Input[Index + 1];
	}

	return Sum;
}
```

### Serial Dependency Chains

- **Serial dependency chain** --> refers to code which is one huge chain of things that are all dependent on each other
- In the previous code example, every single add that we do in the entire summation is all dependent on its predecessor (all the way back to the first iteration of the loop)
  - We can improve the performance of this loop, but we must first break the serial dependency chain

```c
typedef unsigned int u32;
u32 DualScalar(u32 Count, u32 *Input)
{
	u32 SumA = 0;
	u32 SumB = 0;

  // Keep the unrolled loops, but sum into different accumulators. This will
  // allow for multiple dependency chains, which are independent of each other,
  // so the CPU will always have at more than one add it can do in parallel.
	for(u32 Index = 0; Index < Count; Index += 2)
	{
		SumA += Input[Index + 0];
		SumB += Input[Index + 1];
	}

	u32 Sum = SumA + SumB;
	return Sum;
}
```
