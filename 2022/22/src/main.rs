#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use regex::Regex;
use std::collections::HashMap;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

#[derive(PartialEq)]
enum MazePos {
    Empty,
    Wall,
}

fn part1(text: &String) {
    let mut maze: HashMap<(i64, i64), MazePos> = HashMap::new();

    for (y, line) in text.lines().enumerate() {
        if (line.is_empty()) {
            break;
        }

        for (x, c) in line.chars().enumerate() {
            match c {
                '.' => maze.insert((x as i64, y as i64), MazePos::Empty),
                '#' => maze.insert((x as i64, y as i64), MazePos::Wall),
                _ => Some(MazePos::Empty),
            };
        }
    }

    let mut instrStr = text.lines().nth_back(0).unwrap().to_string();
    let patternNum = Regex::new(r"^([\d]+)(.*)").unwrap();
    let patternDir = Regex::new(r"^([RL]+)(.*)").unwrap();
    let mut instructions: Vec<String> = Vec::new();
    while (!instrStr.is_empty()) {
        let m = patternNum.captures(&instrStr);
        if (m.is_some()) {
            let mNum = m.unwrap();
            instructions.push(mNum[1].to_string());
            instrStr = mNum[2].to_string();
        } else {
            let m = patternDir.captures(&instrStr);
            if (m.is_some()) {
                let mDir = m.unwrap();
                instructions.push(mDir[1].to_string());
                instrStr = mDir[2].to_string();
            }
        }
    }

    // Find start.
    let mut x: i64 = 0;
    let mut y: i64 = 0;
    let mut dir: i64 = 0;
    while (!maze.contains_key(&(x, y))) {
        x += 1;
    }

    for instr in instructions {
        if (instr == "R") {
            dir = (dir + 1).rem_euclid(4);
        } else if (instr == "L") {
            dir = (dir - 1).rem_euclid(4);
        } else {
            let value: i64 = instr.parse::<i64>().unwrap();

            let offset: (i64, i64) = match dir {
                0 => (1, 0),
                1 => (0, 1),
                2 => (-1, 0),
                3 => (0, -1),
                _ => panic!("Wrong dir!"),
            };

            for _ in 0..value {
                let mut newX = x + offset.0;
                let mut newY = y + offset.1;

                let mazePos = maze.get(&(newX, newY));
                if (mazePos.is_some()) {
                    if (mazePos.unwrap() == &MazePos::Wall) {
                        break;
                    } else {
                        x = newX;
                        y = newY;
                    }
                } else {
                    // Wrap around. Go in opposite direction and find last valid position.
                    loop {
                        newX -= offset.0;
                        newY -= offset.1;

                        let mazePosTest = maze.get(&(newX, newY));
                        if (mazePosTest.is_none()) {
                            newX += offset.0;
                            newY += offset.1;
                            break;
                        }
                    }

                    let mazePosTest = maze.get(&(newX, newY));
                    if (mazePosTest.unwrap() == &MazePos::Wall) {
                        break;
                    } else {
                        x = newX;
                        y = newY;
                    }
                }
            }
        }
    }

    println!("{} {} {}", x, y, dir);
    println!("Result: {}", (y + 1) * 1000 + (x + 1) * 4 + dir);
}

fn getSideNumberExample(x: i64, y: i64) -> i64 {
    match y {
        0..=3 => return 1,
        4..=7 => match x {
            0..=3 => return 2,
            4..=7 => return 3,
            8..=11 => return 5,
            _ => return 0,
        },
        8..=11 => match x {
            8..=11 => return 6,
            12..=15 => return 4,
            _ => return 0,
        },
        _ => return 0,
    }
}

fn getSideNumber(x: i64, y: i64) -> i64 {
    match y {
        0..=49 => match x {
            50..=99 => return 1,
            100..=149 => return 2,
            _ => panic!("Wrong!"),
        },
        50..=99 => return 3,
        100..=149 => match x {
            0..=49 => return 5,
            50..=99 => return 6,
            _ => panic!("Wrong!"),
        },
        150..=199 => return 4,
        _ => panic!("Wrong!"),
    }
}

fn getWrapExample(x: i64, y: i64, dirX: i64, dirY: i64) -> (i64, i64, i64, i64) {
    let from: i64 = getSideNumberExample(x, y);
    if (from == 1) {
        if (dirY == -1) {
            // up to 2.
            return (11 - x, 4, 0, 1);
        } else if (dirX == 1) {
            // right to 4.
            return (15, 11 - y, -1, 0);
        } else if (dirX == -1) {
            // left to 3.
            return (y + 4, 4, 0, 1);
        }
    } else if (from == 2) {
        if (dirY == -1) {
            // up to 1.
            return (11 - x, 0, 0, 1);
        } else if (dirY == 1) {
            // down to 6.
            return (11 - x, 11, 0, -1);
        } else if (dirX == -1) {
            // left to 4.
            return (15 - y + 4, 11, 0, -1);
        }
    } else if (from == 3) {
        if (dirY == -1) {
            // up to 1.
            return (8, x - 4, 1, 0);
        } else if (dirY == 1) {
            // down to 6.
            return (11 - x, 11, 1, 0);
        }
    } else if (from == 4) {
        if (dirY == -1) {
            // up to 5.
            return (11, 7 - x + 12, -1, 0);
        } else if (dirY == 1) {
            // down to 2.
            return (0, 7 - x + 12, 1, 0);
        } else if (dirX == 1) {
            // right to 1.
            return (11, 11 - y, -1, 0);
        }
    } else if (from == 5) {
        if (dirX == 1) {
            // right to 4.
            return (7 - y + 12, 8, 0, 1);
        }
    } else if (from == 6) {
        if (dirY == 1) {
            // down to 2.
            return (11 - x, 7, 0, -1);
        } else if (dirX == -1) {
            // left to 3.
            return (11 - y + 4, 7, 0, -1);
        }
    }
    panic!("Wrong!");
}

fn getWrap(x: i64, y: i64, dirX: i64, dirY: i64) -> (i64, i64, i64, i64) {
    let from: i64 = getSideNumber(x, y);
    let lx = x % 50;
    let ly = y % 50;
    if (from == 1) {
        if (dirY == -1) {
            // up to 4.
            return (0, 150 + lx, 1, 0);
        } else if (dirX == -1) {
            // left to 5.
            return (0, 149 - ly, 1, 0);
        }
    } else if (from == 2) {
        if (dirY == -1) {
            // up to 4.
            return (lx, 199, 0, -1);
        } else if (dirY == 1) {
            // down to 3.
            return (99, 50 + lx, -1, 0);
        } else if (dirX == 1) {
            // right to 6.
            return (99, 149 - ly, -1, 0);
        }
    } else if (from == 3) {
        if (dirX == -1) {
            // left to 5.
            return (ly, 100, 0, 1);
        } else if (dirX == 1) {
            // right to 2.
            return (100 + ly, 49, 0, -1);
        }
    } else if (from == 4) {
        if (dirY == 1) {
            // down to 2.
            return (100 + lx, 0, 0, 1);
        } else if (dirX == -1) {
            // left to 1.
            return (50 + ly, 0, 0, 1);
        } else if (dirX == 1) {
            // right to 6.
            return (50 + ly, 149, 0, -1);
        }
    } else if (from == 5) {
        if (dirY == -1) {
            // up to 3.
            return (50, 50 + lx, 1, 0);
        } else if (dirX == -1) {
            // left to 1.
            return (50, 49 - ly, 1, 0);
        }
    } else if (from == 6) {
        if (dirY == 1) {
            // down to 4.
            return (49, 150 + lx, -1, 0);
        } else if (dirX == 1) {
            // right to 2.
            return (149, 49 - ly, -1, 0);
        }
    }
    panic!("Wrong!");
}

fn part2(text: &String) {
    let mut maze: HashMap<(i64, i64), MazePos> = HashMap::new();

    for (y, line) in text.lines().enumerate() {
        if (line.is_empty()) {
            break;
        }

        for (x, c) in line.chars().enumerate() {
            match c {
                '.' => maze.insert((x as i64, y as i64), MazePos::Empty),
                '#' => maze.insert((x as i64, y as i64), MazePos::Wall),
                _ => Some(MazePos::Empty),
            };
        }
    }

    let mut instrStr = text.lines().nth_back(0).unwrap().to_string();
    let patternNum = Regex::new(r"^([\d]+)(.*)").unwrap();
    let patternDir = Regex::new(r"^([RL]+)(.*)").unwrap();
    let mut instructions: Vec<String> = Vec::new();
    while (!instrStr.is_empty()) {
        let m = patternNum.captures(&instrStr);
        if (m.is_some()) {
            let mNum = m.unwrap();
            instructions.push(mNum[1].to_string());
            instrStr = mNum[2].to_string();
        } else {
            let m = patternDir.captures(&instrStr);
            if (m.is_some()) {
                let mDir = m.unwrap();
                instructions.push(mDir[1].to_string());
                instrStr = mDir[2].to_string();
            }
        }
    }

    // Find start.
    let mut x: i64 = 0;
    let mut y: i64 = 0;
    let mut dir: i64 = 0;
    while (!maze.contains_key(&(x, y))) {
        x += 1;
    }

    for instr in instructions {
        if (instr == "R") {
            dir = (dir + 1).rem_euclid(4);
        } else if (instr == "L") {
            dir = (dir - 1).rem_euclid(4);
        } else {
            let value: i64 = instr.parse::<i64>().unwrap();

            let mut offset: (i64, i64) = match dir {
                0 => (1, 0),
                1 => (0, 1),
                2 => (-1, 0),
                3 => (0, -1),
                _ => panic!("Wrong dir!"),
            };

            for _ in 0..value {
                let mut newX = x + offset.0;
                let mut newY = y + offset.1;

                let mazePos = maze.get(&(newX, newY));
                if (mazePos.is_some()) {
                    if (mazePos.unwrap() == &MazePos::Wall) {
                        break;
                    } else {
                        x = newX;
                        y = newY;
                    }
                } else {
                    // Wrap around. Get new position on cube.
                    let result = getWrap(x, y, offset.0, offset.1);
                    newX = result.0;
                    newY = result.1;
                    offset.0 = result.2;
                    offset.1 = result.3;

                    let mazePosTest = maze.get(&(newX, newY));
                    if (mazePosTest.unwrap() == &MazePos::Wall) {
                        break;
                    } else {
                        x = newX;
                        y = newY;
                        dir = match offset {
                            (1, 0) => 0,
                            (0, 1) => 1,
                            (-1, 0) => 2,
                            (0, -1) => 3,
                            _ => panic!("Wrong!"),
                        }
                    }
                }
            }
        }
    }

    println!("{} {} {}", x, y, dir);
    println!("Result: {}", (y + 1) * 1000 + (x + 1) * 4 + dir);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    //part1(&text);
    part2(&text);
}
