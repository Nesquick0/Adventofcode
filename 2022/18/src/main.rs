#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use std::collections::{HashMap, VecDeque};
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

fn part1(text: &String) {
    let mut cubes: HashMap<(i64, i64, i64), i64> = HashMap::new();
    for line in text.lines() {
        let pos: Vec<i64> = line
            .split(",")
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>();
        let mut posIter = pos.iter();
        let (x, y, z) = (
            posIter.next().unwrap(),
            posIter.next().unwrap(),
            posIter.next().unwrap(),
        );
        cubes.insert((*x, *y, *z), 1);
    }

    let mut sides: i64 = 0;
    for ((x, y, z), _) in &cubes {
        for dir in [
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
        ] {
            if (!cubes.contains_key(&(x + dir.0, y + dir.1, z + dir.2))) {
                sides += 1;
            }
        }
    }
    println!("{}", sides);
}

fn part2(text: &String) {
    let mut cubes: HashMap<(i64, i64, i64), i64> = HashMap::new();
    for line in text.lines() {
        let pos: Vec<i64> = line
            .split(",")
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>();
        let mut posIter = pos.iter();
        let (x, y, z) = (
            posIter.next().unwrap(),
            posIter.next().unwrap(),
            posIter.next().unwrap(),
        );
        cubes.insert((*x, *y, *z), 1);
    }

    let mut limitsMin: (i64, i64, i64) = (0, 0, 0);
    let mut limitsMax: (i64, i64, i64) = (0, 0, 0);
    let mut initLimits = true;
    for ((x, y, z), _) in &cubes {
        if (initLimits) {
            initLimits = false;
            limitsMin = (*x, *y, *z);
            limitsMax = (*x, *y, *z);
        }
        limitsMin.0 = std::cmp::min(limitsMin.0, *x);
        limitsMin.1 = std::cmp::min(limitsMin.1, *y);
        limitsMin.2 = std::cmp::min(limitsMin.2, *z);

        limitsMax.0 = std::cmp::max(limitsMax.0, *x);
        limitsMax.1 = std::cmp::max(limitsMax.1, *y);
        limitsMax.2 = std::cmp::max(limitsMax.2, *z);
    }
    limitsMin = (limitsMin.0 - 1, limitsMin.1 - 1, limitsMin.2 - 1);
    limitsMax = (limitsMax.0 + 1, limitsMax.1 + 1, limitsMax.2 + 1);
    println!("{:?} {:?}", limitsMin, limitsMax);

    // Expand "smoke" from border.
    let mut smokes: HashMap<(i64, i64, i64), i64> = HashMap::new();
    smokes.insert(limitsMin, 1);
    let mut queue: VecDeque<(i64, i64, i64)> = VecDeque::new();
    queue.push_back(limitsMin);

    while (!queue.is_empty()) {
        let pos = queue.pop_front().unwrap();

        for dir in [
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
        ] {
            let newPos = (pos.0 + dir.0, pos.1 + dir.1, pos.2 + dir.2);
            if (newPos.0 >= limitsMin.0
                && newPos.0 <= limitsMax.0
                && newPos.1 >= limitsMin.1
                && newPos.1 <= limitsMax.1
                && newPos.2 >= limitsMin.2
                && newPos.2 <= limitsMax.2)
            {
                if (!cubes.contains_key(&newPos) && !smokes.contains_key(&newPos)) {
                    queue.push_back(newPos);
                    smokes.insert(newPos, 1);
                }
            }
        }
    }

    let mut sides: i64 = 0;
    for ((x, y, z), _) in &cubes {
        for dir in [
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
        ] {
            let pos = (x + dir.0, y + dir.1, z + dir.2);
            if (!cubes.contains_key(&pos) && smokes.contains_key(&pos)) {
                sides += 1;
            }
        }
    }
    println!("{}", sides);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
