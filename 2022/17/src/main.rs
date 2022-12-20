#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use std::collections::HashSet;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

#[derive(Debug, PartialEq)]
enum WindDir {
    L,
    R,
}

#[derive(Debug, Clone)]
struct Rock {
    points: Vec<(i64, i64)>,
    height: i64,
    width: i64,
}

impl Rock {
    pub fn new(points: Vec<(i64, i64)>) -> Self {
        let height: i64 = points.iter().max_by_key(|x| &x.1).unwrap().1 + 1;
        let width: i64 = points.iter().max_by_key(|x| &x.0).unwrap().0 + 1;
        Self {
            points: points,
            height: height,
            width: width,
        }
    }

    fn createRocks() -> Vec<Rock> {
        let mut rocks: Vec<Rock> = Vec::new();

        rocks.push(Rock::new(vec![(0, 0), (1, 0), (2, 0), (3, 0)]));
        rocks.push(Rock::new(vec![(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]));
        rocks.push(Rock::new(vec![(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)]));
        rocks.push(Rock::new(vec![(0, 0), (0, 1), (0, 2), (0, 3)]));
        rocks.push(Rock::new(vec![(0, 0), (1, 0), (0, 1), (1, 1)]));

        return rocks;
    }

    fn collide(&self, rockPoints: &HashSet<(i64, i64)>, rockPos: &(i64, i64)) -> bool {
        for point in &self.points {
            if (rockPoints.contains(&(point.0 + rockPos.0, point.1 + rockPos.1))) {
                return true;
            }
        }
        return false;
    }
}

fn _drawRocks(width: i64, maxHeight: i64, rockPoints: &HashSet<(i64, i64)>) {
    for y in maxHeight..=0 {
        for x in 0..width {
            if (rockPoints.contains(&(x, y))) {
                print!("#");
            } else {
                print!(".");
            }
        }
        println!();
    }
    println!("");
}

fn part1(text: &String) {
    let winds: Vec<WindDir> = text
        .lines()
        .next()
        .unwrap()
        .chars()
        .map(|OneChar| match OneChar {
            '>' => WindDir::R,
            '<' => WindDir::L,
            _ => panic!("Wrong char"),
        })
        .collect::<Vec<WindDir>>();

    let mut maxHeight: i64 = 0;
    let mut rockPoints: HashSet<(i64, i64)> = HashSet::new();
    let rockPool: Vec<Rock> = Rock::createRocks();
    let width: i64 = 7;

    // Try to find pattern.
    let loopLength = (winds.len() * rockPool.len());
    let mut linesBits: Vec<u8> = Vec::new();

    let mut w: usize = 0;
    for i in 0..2022 {
        let rockIndex: usize = i % rockPool.len();

        // Create new rock.
        let rock: &Rock = rockPool.get(rockIndex).unwrap();
        let mut rockPos: (i64, i64) = (2, maxHeight - 3 + 1 - rock.height);
        // Simulate fall
        loop {
            let windDir: &WindDir = winds.get(w % winds.len()).unwrap();
            w += 1;
            let mut newPos: (i64, i64) = (rockPos.0, rockPos.1);
            // Move with wind.
            if (windDir == &WindDir::L) {
                if (newPos.0 > 0) {
                    newPos.0 -= 1;
                }
            } else {
                if (newPos.0 + rock.width < width) {
                    newPos.0 += 1;
                }
            }
            // Check collision. Revert position.
            if (rock.collide(&rockPoints, &newPos)) {
                newPos = (rockPos.0, rockPos.1);
            }

            // Try to fall.
            if ((newPos.1 + rock.height - 1) >= 0
                || rock.collide(&rockPoints, &(newPos.0, newPos.1 + 1)))
            {
                for point in &rock.points {
                    let newPoint: (i64, i64) = (point.0 + newPos.0, point.1 + newPos.1);
                    rockPoints.insert(newPoint);

                    while ((-newPoint.1) as usize >= linesBits.len()) {
                        linesBits.push(0);
                    }
                    *linesBits.get_mut((-newPoint.1 as usize)).unwrap() |= (1 << newPoint.0);
                }
                maxHeight = std::cmp::min(newPos.1 - 1, maxHeight);
                break;
            }
            // Set new position.
            rockPos = (newPos.0, newPos.1 + 1);
        }
        //drawRocks(width, maxHeight, &rockPoints);
    }
    println!("Height: {}", -maxHeight);
}

fn part2(text: &String) {}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    //part2(&text); // I give up.
}
