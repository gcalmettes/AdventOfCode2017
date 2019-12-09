"""
https://adventofcode.com/2019/day/5
"""

from typing import List, Tuple
from enum import Enum

class Opcode(Enum):
    ADD: int = 1
    MULTIPLY: int = 2
    INPUT: int = 3
    OUTPUT: int = 4
    JUMP_IF_TRUE: int = 5 
    JUMP_IF_FALSE: int = 6
    LESS_THAN: int = 7
    EQUALS: int = 8
    HALT: int = 99

class ParameterMode:
    POSITION: int = 0
    IMMEDIATE: int = 1

Modes = List[int]
Program = List[int] 

def parse_opcode(opcode: int, n_modes: int = 3) -> Tuple[Opcode, Modes]:
    opcode_part = opcode % 100

    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(n_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10

    return Opcode(opcode_part), modes

def get_value(program: Program, pos: int, mode: int) -> int:
    if mode == ParameterMode.POSITION:
        return program[program[pos]]
    elif mode == ParameterMode.IMMEDIATE:
        return program[pos]





def run_intcode(program: Program, inputs=[1]) -> int:
    program = program[:]

    #
    cursor = 0
    output = []
    inputs.reverse()

    while True:
        opcode, modes = parse_opcode(program[cursor])
        # print(opcode)

        if opcode == Opcode.ADD:
            p1 = get_value(program, cursor+1, modes[0])
            p2 = get_value(program, cursor+2, modes[1])
            program[program[cursor+3]] = p1 + p2
            cursor += 4
        elif opcode == Opcode.MULTIPLY:
            p1 = get_value(program, cursor+1, modes[0])
            p2 = get_value(program, cursor+2, modes[1])
            program[program[cursor+3]] = p1 * p2
            cursor += 4
        elif opcode == Opcode.INPUT:
            in_value = inputs.pop()
            program[program[cursor+1]] = in_value
            cursor += 2
        elif opcode == Opcode.OUTPUT:
            p1 = get_value(program, cursor+1, modes[0])
            output += [p1]
            cursor += 2
        elif opcode == Opcode.JUMP_IF_TRUE:
            p1 = get_value(program, cursor+1, modes[0])
            p2 = get_value(program, cursor+2, modes[1])
            if p1 != 0:
                cursor = p2
            else:
                cursor += 3
        elif opcode == Opcode.JUMP_IF_FALSE:
            p1 = get_value(program, cursor+1, modes[0])
            p2 = get_value(program, cursor+2, modes[1])
            if p1 == 0:
                cursor = p2
            else:
                cursor += 3
        elif opcode == Opcode.LESS_THAN:
            p1 = get_value(program, cursor+1, modes[0])
            p2 = get_value(program, cursor+2, modes[1])
            # p3 = get_value(program, cursor+3, modes[2])
            if p1 < p2:
                program[program[cursor+3]] = 1
            else:
                program[program[cursor+3]] = 0
            cursor += 4
        elif opcode == Opcode.EQUALS:
            p1 = get_value(program, cursor+1, modes[0])
            p2 = get_value(program, cursor+2, modes[1])
            # p3 = get_value(program, cursor+3, modes[2])
            if p1 == p2:
                program[program[cursor+3]] = 1
            else:
                program[program[cursor+3]] = 0
            cursor += 4
        elif opcode == Opcode.HALT:
            break
        else:
            raise ValueError(f'Incorrect opcode {opcode}')


    return program[0], output



with open('day05_input.txt', 'r') as f:
    data = list(map(int, f.readline().split(',')))


part1 = run_intcode(data, inputs=[1])[1][-1]
print(f'part1: {part1}')

part2 = run_intcode(data, inputs=[5])[1][-1]
print(f'part2: {part2}')