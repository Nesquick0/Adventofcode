#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

struct Cpu {
    cycle: i64,
    x: i64,
}

impl Cpu {
    pub fn new() -> Self {
        Self { cycle: 1, x: 1 }
    }

    fn checkSignalStrenght(&self) -> i64 {
        if ((self.cycle - 20) % 40 == 0) {
            return self.cycle * self.x;
        }
        return 0;
    }

    fn run(&mut self, cmd: &str) -> i64 {
        let mut signal: i64 = 0;
        if ("noop" == cmd) {
            signal += self.checkSignalStrenght();
            self.cycle += 1;
        } else if (cmd.starts_with("addx ")) {
            signal += self.checkSignalStrenght();
            self.cycle += 1;
            signal += self.checkSignalStrenght();
            self.cycle += 1;
            let value: i64 = cmd
                .split_whitespace()
                .nth(1)
                .unwrap()
                .parse::<i64>()
                .unwrap();
            self.x += value;
        }
        return signal;
    }
}

struct CpuScreen {
    cycle: i64,
    x: i64,
}

impl CpuScreen {
    pub fn new() -> Self {
        Self { cycle: 1, x: 1 }
    }

    fn renderPixel(&self) {
        if (self.cycle % 40 == 1) {
            println!();
        }
        let testCycle = (self.cycle - 1) % 40;
        if (testCycle >= self.x - 1 && testCycle <= self.x + 1) {
            print!("#")
        } else {
            print!(".");
        }
    }

    fn run(&mut self, cmd: &str) {
        if ("noop" == cmd) {
            self.renderPixel();
            self.cycle += 1;
        } else if (cmd.starts_with("addx ")) {
            self.renderPixel();
            self.cycle += 1;
            self.renderPixel();
            self.cycle += 1;
            let value: i64 = cmd
                .split_whitespace()
                .nth(1)
                .unwrap()
                .parse::<i64>()
                .unwrap();
            self.x += value;
        }
    }
}

fn part1(text: &String) {
    let mut cpu: Cpu = Cpu::new();
    let mut totalSignalStrength: i64 = 0;
    for line in text.lines() {
        totalSignalStrength += cpu.run(line);
    }
    println!("{}", totalSignalStrength);
}

fn part2(text: &String) {
    let mut cpu: CpuScreen = CpuScreen::new();
    for line in text.lines() {
        cpu.run(line);
    }
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
