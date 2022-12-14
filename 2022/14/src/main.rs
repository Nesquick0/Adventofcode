#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use std::collections::HashMap;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

struct World {
    //blocks: Vec<(i64, i64)>,
    blocks: HashMap<(i64, i64), i64>,
    snadStart: (i64, i64),
    abyssHeight: i64,
}

impl World {
    pub fn new() -> Self {
        Self {
            blocks: HashMap::new(),
            snadStart: (500, 0),
            abyssHeight: 0,
        }
    }

    fn simulateSand(&mut self) -> bool {
        let mut sand: (i64, i64) = self.snadStart;

        while (sand.1 <= self.abyssHeight) {
            if (!self.blocks.contains_key(&(sand.0, sand.1 + 1))) {
                sand.1 += 1;
            } else if (!self.blocks.contains_key(&(sand.0 - 1, sand.1 + 1))) {
                sand.0 -= 1;
                sand.1 += 1;
            } else if (!self.blocks.contains_key(&(sand.0 + 1, sand.1 + 1))) {
                sand.0 += 1;
                sand.1 += 1;
            } else {
                // All positions blocked. Finish.
                self.blocks.insert(sand, 2);
                return true;
            }
        }
        // Snad haven't stopped. Falling to abyss.
        return false;
    }

    fn simulateSandWithFloor(&mut self) -> bool {
        let mut sand: (i64, i64) = self.snadStart;
        if (self.blocks.contains_key(&sand)) {
            return false;
        }

        loop {
            if (sand.1 == self.abyssHeight + 1) {
                // Just above bottom floor. Stop.
                self.blocks.insert(sand, 2);
                return true;
            } else if (!self.blocks.contains_key(&(sand.0, sand.1 + 1))) {
                sand.1 += 1;
            } else if (!self.blocks.contains_key(&(sand.0 - 1, sand.1 + 1))) {
                sand.0 -= 1;
                sand.1 += 1;
            } else if (!self.blocks.contains_key(&(sand.0 + 1, sand.1 + 1))) {
                sand.0 += 1;
                sand.1 += 1;
            } else {
                // All positions blocked. Finish.
                self.blocks.insert(sand, 2);
                return true;
            }
        }
    }
}

fn part1(text: &String) {
    let mut world: World = World::new();

    for line in text.lines() {
        let split = line.split(" -> ");
        let mut positions: Vec<(i64, i64)> = Vec::new();
        for pos in split {
            let mut posSplit = pos.split(",");
            let x = posSplit.next().unwrap().parse::<i64>().unwrap();
            let y = posSplit.next().unwrap().parse::<i64>().unwrap();
            positions.push((x, y));
            world.abyssHeight = std::cmp::max(world.abyssHeight, y);
        }

        for window in positions.windows(2) {
            let pos1 = window.get(0).unwrap();
            let pos2 = window.get(1).unwrap();
            let step: (i64, i64) = ((pos2.0 - pos1.0).signum(), (pos2.1 - pos1.1).signum());
            let distance = std::cmp::max((pos2.0 - pos1.0).abs(), (pos2.1 - pos1.1).abs());

            for i in 0..=distance {
                let block: (i64, i64) = (pos1.0 + step.0 * i, pos1.1 + step.1 * i);
                world.blocks.insert(block, 1);
            }
        }
    }

    let stones = world.blocks.len();
    loop {
        let result = world.simulateSand();
        if (!result) {
            break;
        }
    }
    let allSand = world.blocks.len() - stones;
    println!("Sand: {}", allSand);
}

fn part2(text: &String) {
    let mut world: World = World::new();

    for line in text.lines() {
        let split = line.split(" -> ");
        let mut positions: Vec<(i64, i64)> = Vec::new();
        for pos in split {
            let mut posSplit = pos.split(",");
            let x = posSplit.next().unwrap().parse::<i64>().unwrap();
            let y = posSplit.next().unwrap().parse::<i64>().unwrap();
            positions.push((x, y));
            world.abyssHeight = std::cmp::max(world.abyssHeight, y);
        }

        for window in positions.windows(2) {
            let pos1 = window.get(0).unwrap();
            let pos2 = window.get(1).unwrap();
            let step: (i64, i64) = ((pos2.0 - pos1.0).signum(), (pos2.1 - pos1.1).signum());
            let distance = std::cmp::max((pos2.0 - pos1.0).abs(), (pos2.1 - pos1.1).abs());

            for i in 0..=distance {
                let block: (i64, i64) = (pos1.0 + step.0 * i, pos1.1 + step.1 * i);
                world.blocks.insert(block, 1);
            }
        }
    }

    let stones = world.blocks.len();
    loop {
        let result = world.simulateSandWithFloor();
        if (!result) {
            break;
        }
    }
    let allSand = world.blocks.len() - stones;
    println!("Sand: {}", allSand);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
