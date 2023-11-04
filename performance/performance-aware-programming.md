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
  - `LEA` (learn effective address) --> `C = A + B`
- Running a simple program that adds `A` and `B` is much slower in Python than C
  - Python first turns the `A + B` into its own instruction stream (instructions meant to be read by the Python interpreter rather than the CPU)
  - When the program is ran, we have to run all the instructions for Python to decode and manage that Python instruction stream, which generates massive numbers of additional instructions
  - The few instructions we actually asked for are sandwiched in between hundreds of instructions we did not ask for and the CPU has to do them all
- As a result, if we want our Python code to run more quickly, we essentially have to look for ways of not using Python. This includes:
  - Using add-ons that that have ways of doing work in bulk (in precompiled C), so we only have to use a little bit of Python to kick off much faster work that can be done in compiled code
  - Finding a JIT that will turn some of our loops into actual streamlined code, so that the Python interpreter will not be involved
