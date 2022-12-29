#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use std::collections::HashMap;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

fn draw(elves: &HashMap<(i64, i64), i64>) {
    let minX = elves.keys().min_by_key(|a| a.0).unwrap().0;
    let minY = elves.keys().min_by_key(|a| a.1).unwrap().1;
    let maxX = elves.keys().max_by_key(|a| a.0).unwrap().0;
    let maxY = elves.keys().max_by_key(|a| a.1).unwrap().1;

    for y in minY..=maxY {
        for x in minX..=maxX {
            if (elves.contains_key(&(x, y))) {
                print!("#");
            } else {
                print!(".");
            }
        }
        println!();
    }
    println!();
}

fn score(elves: &HashMap<(i64, i64), i64>) -> i64 {
    let minX = elves.keys().min_by_key(|a| a.0).unwrap().0;
    let minY = elves.keys().min_by_key(|a| a.1).unwrap().1;
    let maxX = elves.keys().max_by_key(|a| a.0).unwrap().0;
    let maxY = elves.keys().max_by_key(|a| a.1).unwrap().1;

    return ((maxX - minX + 1) * (maxY - minY + 1)) - elves.len() as i64;
}

#[derive(PartialEq)]
enum Directions {
    North,
    South,
    West,
    East,
}

fn part1(text: &String) {
    let mut elves: HashMap<(i64, i64), i64> = HashMap::new();
    for (y, line) in text.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if (c == '#') {
                elves.insert((x as i64, y as i64), 1);
            }
        }
    }
    //draw(&elves);

    // Simulate.
    let mut round = 0;
    loop {
        let mut proposed: HashMap<(i64, i64), Vec<(i64, i64)>> = HashMap::new(); // (proposed position)

        // For every elf check positions and propose movement.
        for elf in &elves {
            let pos = elf.0;
            let mut neighbourds: [i64; 8] = [0; 8];
            for (i, offset) in [
                (-1, -1),
                (0, -1),
                (1, -1),
                (-1, 0),
                (1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
            ]
            .iter()
            .enumerate()
            {
                if (elves.contains_key(&(pos.0 + offset.0, pos.1 + offset.1))) {
                    neighbourds[i] = 1;
                } else {
                    neighbourds[i] = 0;
                }
            }

            if (neighbourds.iter().sum::<i64>() == 0) {
                // Do nothing.
                continue;
            }

            for dir in 0..4 {
                let testDir: Directions = match ((round + dir) % 4) {
                    0 => Directions::North,
                    1 => Directions::South,
                    2 => Directions::West,
                    3 => Directions::East,
                    _ => panic!("Wrong enum!"),
                };

                if (testDir == Directions::North) {
                    if (neighbourds[0] == 0 && neighbourds[1] == 0 && neighbourds[2] == 0) {
                        proposed
                            .entry((pos.0, pos.1 - 1))
                            .or_insert(Vec::new())
                            .push(*pos);
                        break;
                    }
                } else if (testDir == Directions::South) {
                    if (neighbourds[5] == 0 && neighbourds[6] == 0 && neighbourds[7] == 0) {
                        proposed
                            .entry((pos.0, pos.1 + 1))
                            .or_insert(Vec::new())
                            .push(*pos);
                        break;
                    }
                } else if (testDir == Directions::West) {
                    if (neighbourds[0] == 0 && neighbourds[3] == 0 && neighbourds[5] == 0) {
                        proposed
                            .entry((pos.0 - 1, pos.1))
                            .or_insert(Vec::new())
                            .push(*pos);
                        break;
                    }
                } else if (testDir == Directions::East) {
                    if (neighbourds[2] == 0 && neighbourds[4] == 0 && neighbourds[7] == 0) {
                        proposed
                            .entry((pos.0 + 1, pos.1))
                            .or_insert(Vec::new())
                            .push(*pos);
                        break;
                    }
                }
            }
        }

        if (proposed.is_empty()) {
            println!("Final round: {}", round + 1);
            break;
        }

        // Only move those which are only one to that position.
        for prop in &proposed {
            if (prop.1.len() == 1) {
                elves.remove(prop.1.get(0).unwrap());
                elves.insert(*prop.0, 1);
            }
        }

        // draw(&elves);
        round += 1;
        if (round == 10) {
            println!("Empty: {}", score(&elves));
        }
    }
}

fn part2(text: &String) {}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
