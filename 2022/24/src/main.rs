#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use std::collections::{HashMap, HashSet, VecDeque};
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

enum Direction {
    Up,
    Right,
    Down,
    Left,
}

fn calculateBlizzPos(
    time: i64,
    initialPos: &(i64, i64),
    dir: &Direction,
    minMax: &[i64; 4],
) -> (i64, i64) {
    let newPos = match dir {
        Direction::Up => (
            initialPos.0,
            (initialPos.1 - time - 1).rem_euclid(minMax[3] - 2) + 1,
        ),
        Direction::Right => (
            (initialPos.0 + time - 1).rem_euclid(minMax[2] - 2) + 1,
            initialPos.1,
        ),
        Direction::Down => (
            initialPos.0,
            (initialPos.1 + time - 1).rem_euclid(minMax[3] - 2) + 1,
        ),
        Direction::Left => (
            (initialPos.0 - time - 1).rem_euclid(minMax[2] - 2) + 1,
            initialPos.1,
        ),
    };
    return newPos;
}

fn _draw(blizzards: &HashMap<(i64, i64), Direction>, minMax: &[i64; 4], state: (i64, (i64, i64))) {
    let minX = minMax[0];
    let minY = minMax[1];
    let maxX = minMax[2];
    let maxY = minMax[3];

    let mut curBlizzards: HashSet<(i64, i64)> = HashSet::new();
    for blizz in blizzards {
        let curPos = calculateBlizzPos(state.0, blizz.0, blizz.1, minMax);
        curBlizzards.insert(curPos);
    }

    for y in minY..maxY {
        print!("#");
        for x in minX + 1..maxX - 1 {
            if (y == minY || y == maxY - 1) {
                print!("#")
            } else if (curBlizzards.contains(&(x, y))) {
                print!("o");
            } else if (state.1 .0 == x && state.1 .1 == y) {
                print!("E");
            } else {
                print!(".");
            }
        }
        println!("#");
    }
    println!();
}

fn part1(text: &String) {
    let mut blizzards: HashMap<(i64, i64), Direction> = HashMap::new();
    let mut minMax: [i64; 4] = [0; 4];

    for (y, line) in text.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            match c {
                '#' => None,
                '^' => blizzards.insert((x as i64, y as i64), Direction::Up),
                '>' => blizzards.insert((x as i64, y as i64), Direction::Right),
                'v' => blizzards.insert((x as i64, y as i64), Direction::Down),
                '<' => blizzards.insert((x as i64, y as i64), Direction::Left),
                _ => None,
            };
        }
    }
    minMax[2] = text.lines().next().unwrap().chars().count() as i64;
    minMax[3] = text.lines().count() as i64;

    //draw(&blizzards, &minMax, (0, (1, 0)));

    // Find path.
    let targetPos = (minMax[2] - 2, minMax[3] - 1);
    let mut cachedBlizzards: HashSet<(i64, i64)> = HashSet::new();
    let mut cachedTime: i64 = 0;

    let mut queue: VecDeque<(i64, (i64, i64))> = VecDeque::new(); // Time, Position.
    queue.push_front((0, (1, 0)));
    let mut visited: HashSet<(i64, (i64, i64))> = HashSet::new();
    visited.insert((0, (1, 0)));
    while (!queue.is_empty()) {
        let (oldTime, pos) = queue.pop_front().unwrap();
        let time = oldTime + 1;

        if (time != cachedTime) {
            //println!("Recalculate... {} {}", cachedTime, time);
            cachedTime = time;
            cachedBlizzards = HashSet::new();
            for blizz in &blizzards {
                let curPos = calculateBlizzPos(time, blizz.0, blizz.1, &minMax);
                cachedBlizzards.insert(curPos);
            }
        }

        //draw(&blizzards, &minMax, (oldTime, pos));

        for offset in [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)] {
            let newPos = (pos.0 + offset.0, pos.1 + offset.1);
            if (newPos.0 == targetPos.0 && newPos.1 == targetPos.1) {
                println!("Time: {}", time);
                return;
            } else if ((offset.0 != 0 || offset.1 != 0)
                && (newPos.0 <= minMax[0]
                    || newPos.1 <= minMax[1]
                    || newPos.0 >= minMax[2] - 1
                    || newPos.1 >= minMax[3] - 1))
            {
                // Skip, wrong place.
            } else if (!cachedBlizzards.contains(&newPos)) {
                if (!visited.contains(&(time, newPos))) {
                    queue.push_back((time, newPos));
                    visited.insert((time, newPos));
                }
            }
        }
    }
}

fn part2(text: &String) {
    let mut blizzards: HashMap<(i64, i64), Direction> = HashMap::new();
    let mut minMax: [i64; 4] = [0; 4];

    for (y, line) in text.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            match c {
                '#' => None,
                '^' => blizzards.insert((x as i64, y as i64), Direction::Up),
                '>' => blizzards.insert((x as i64, y as i64), Direction::Right),
                'v' => blizzards.insert((x as i64, y as i64), Direction::Down),
                '<' => blizzards.insert((x as i64, y as i64), Direction::Left),
                _ => None,
            };
        }
    }
    minMax[2] = text.lines().next().unwrap().chars().count() as i64;
    minMax[3] = text.lines().count() as i64;

    // Find path.
    let targetPos: [(i64, i64); 3] = [
        (minMax[2] - 2, minMax[3] - 1),
        (1, 0),
        (minMax[2] - 2, minMax[3] - 1),
    ];
    let mut wayIndex: usize = 0;
    let mut cachedBlizzards: HashSet<(i64, i64)> = HashSet::new();
    let mut cachedTime: i64 = 0;

    let mut queue: VecDeque<(i64, (i64, i64))> = VecDeque::new(); // Time, Position.
    queue.push_front((0, (1, 0)));
    let mut visited: HashSet<(i64, (i64, i64))> = HashSet::new();
    visited.insert((0, (1, 0)));
    while (!queue.is_empty()) {
        let (oldTime, pos) = queue.pop_front().unwrap();
        let time = oldTime + 1;

        if (time != cachedTime) {
            cachedTime = time;
            cachedBlizzards = HashSet::new();
            for blizz in &blizzards {
                let curPos = calculateBlizzPos(time, blizz.0, blizz.1, &minMax);
                cachedBlizzards.insert(curPos);
            }
        }

        for offset in [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)] {
            let newPos = (pos.0 + offset.0, pos.1 + offset.1);
            if (newPos.0 == targetPos[wayIndex].0 && newPos.1 == targetPos[wayIndex].1) {
                println!("Time: {}", time);
                if (wayIndex < 2) {
                    wayIndex += 1;
                    queue.clear();
                    queue.push_back((time, newPos));
                    visited.insert((time, newPos));
                    break;
                } else {
                    return;
                }
            } else if ((offset.0 != 0 || offset.1 != 0)
                && (newPos.0 <= minMax[0]
                    || newPos.1 <= minMax[1]
                    || newPos.0 >= minMax[2] - 1
                    || newPos.1 >= minMax[3] - 1))
            {
                // Skip, wrong place.
            } else if (!cachedBlizzards.contains(&newPos)) {
                if (!visited.contains(&(time, newPos))) {
                    queue.push_back((time, newPos));
                    visited.insert((time, newPos));
                }
            }
        }
    }
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
