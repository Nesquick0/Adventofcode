#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::fs;

fn part1(commands: &Vec<(usize, usize, usize)>, stacks: &mut Vec<Vec<char>>) {
    for command in commands.iter() {
        let count: usize = command.0;
        let from: usize = command.1;
        let to: usize = command.2;

        //println!("{} {} {}", count, from, to);
        for _ in 0..count {
            let oneChar: char = stacks.get_mut(from).unwrap().pop().unwrap();
            stacks.get_mut(to).unwrap().push(oneChar);
        }
    }
    for stack in stacks.iter() {
        println!("{:?}", stack);
    }
    for stack in stacks.iter() {
        print!("{}", stack.last().unwrap());
    }
    println!();
}

fn part2(commands: &Vec<(usize, usize, usize)>, stacks: &mut Vec<Vec<char>>) {
    for command in commands.iter() {
        let count: usize = command.0;
        let from: usize = command.1;
        let to: usize = command.2;

        //println!("{} {} {}", count, from, to);
        let nKeep = stacks.get(from).unwrap().len();
        let chars = stacks.get_mut(from).unwrap().split_off(nKeep - count);
        for oneChar in chars {
            stacks.get_mut(to).unwrap().push(oneChar);
        }
    }
    for stack in stacks.iter() {
        println!("{:?}", stack);
    }
    for stack in stacks.iter() {
        print!("{}", stack.last().unwrap());
    }
    println!();
}

fn main() {
    let text: String = fs::read_to_string("input.txt").expect("Bad file!");

    let mut stacks: Vec<Vec<char>> = Vec::new();
    let mut lines = text.lines();
    let nStacks = text.lines().nth(0).unwrap().len() / 4 + 1;
    for _ in 0..nStacks {
        stacks.push(Vec::new());
    }

    loop {
        let line = lines.next().unwrap();
        if (line.is_empty()) {
            break;
        }

        for j in (0..nStacks) {
            let oneChar = line.chars().nth(j * 4 + 1).unwrap();
            if (oneChar != ' ') {
                stacks.get_mut(j).unwrap().push(oneChar);
            }
        }
    }
    for stack in &mut stacks {
        stack.pop();
        stack.reverse();
    }

    let mut commands: Vec<(usize, usize, usize)> = Vec::new();
    for line in lines {
        let mut split = line.split(" ");
        let count: usize = split.nth(1).unwrap().parse::<usize>().unwrap();
        let from: usize = split.nth(1).unwrap().parse::<usize>().unwrap() - 1;
        let to: usize = split.nth(1).unwrap().parse::<usize>().unwrap() - 1;

        commands.push((count, from, to));
    }

    let mut stackCopy = stacks.clone();
    part1(&commands, &mut stackCopy);
    let mut stackCopy2 = stacks.clone();
    part2(&commands, &mut stackCopy2);
}
