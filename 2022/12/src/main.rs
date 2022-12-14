#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::{HashSet, VecDeque};
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

struct World {
    pos: Vec<i64>,
    w: i64,
    h: i64,
}

impl World {
    pub fn new() -> Self {
        Self {
            pos: Vec::new(),
            w: 0,
            h: 0,
        }
    }

    fn getNeighbours(&self, index: i64) -> Vec<i64> {
        let x = index % self.w;
        let y = index / self.w;

        let mut neightbours = Vec::new();
        if (x > 0) {
            neightbours.push(index - 1);
        }
        if (x < self.w - 1) {
            neightbours.push(index + 1);
        }
        if (y > 0) {
            neightbours.push(index - self.w);
        }
        if (y < self.h - 1) {
            neightbours.push(index + self.w);
        }
        return neightbours;
    }

    fn getNeighboursUp(&self, index: i64) -> Vec<i64> {
        // Find neighbours that are only at most 1 step higher.
        let height = self.pos.get(index as usize).unwrap();
        let mut neighbours = self.getNeighbours(index);
        neighbours.retain(|newIndex| self.pos.get(*newIndex as usize).unwrap() <= &(height + 1));
        return neighbours;
    }

    fn getNeighboursOpposite(&self, index: i64) -> Vec<i64> {
        // Checking path from opposite direction so check neighbours that are at least 1 lower.
        let height = self.pos.get(index as usize).unwrap();
        let mut neighbours = self.getNeighbours(index);
        neighbours.retain(|newIndex| self.pos.get(*newIndex as usize).unwrap() >= &(height - 1));
        return neighbours;
    }

    fn findPath(&self, from: i64, to: i64) -> i64 {
        let mut queue: VecDeque<(i64, Vec<i64>)> = VecDeque::new();
        queue.push_back((from, vec![from]));
        let mut visited: HashSet<i64> = HashSet::new();
        visited.insert(from);
        let mut shortestPath: Vec<i64> = Vec::new();

        while (!queue.is_empty()) {
            //println!("{:?}", queue);
            let (index, path): (i64, Vec<i64>) = queue.pop_front().unwrap();
            if (index == to) {
                shortestPath = path;
                break;
            }

            let neighbours = self.getNeighboursUp(index);
            for n in neighbours {
                if (visited.contains(&n)) {
                    continue;
                }
                visited.insert(n);
                let mut newPath = path.clone();
                newPath.push(n);
                queue.push_back((n, newPath));
            }
        }
        //println!("{}", visited.len());
        return shortestPath.len() as i64 - 1;
    }

    fn findNearestBottom(&self, from: i64) -> i64 {
        let mut queue: VecDeque<(i64, Vec<i64>)> = VecDeque::new();
        queue.push_back((from, vec![from]));
        let mut visited: HashSet<i64> = HashSet::new();
        visited.insert(from);
        let mut shortestPath: Vec<i64> = Vec::new();

        while (!queue.is_empty()) {
            let (index, path): (i64, Vec<i64>) = queue.pop_front().unwrap();
            // Run until found first 0 height.
            if (self.pos.get(index as usize).unwrap() == &0) {
                shortestPath = path;
                break;
            }

            let neighbours = self.getNeighboursOpposite(index);
            for n in neighbours {
                if (visited.contains(&n)) {
                    continue;
                }
                visited.insert(n);
                let mut newPath = path.clone();
                newPath.push(n);
                queue.push_back((n, newPath));
            }
        }
        return shortestPath.len() as i64 - 1;
    }
}

fn part1(text: &String) {
    let mut world: World = World::new();
    let mut start: i64 = -1;
    let mut end: i64 = -1;

    for line in text.lines() {
        for oneChar in line.chars() {
            let value: i64 = match (oneChar) {
                'S' => {
                    start = world.pos.len() as i64;
                    0
                }
                'E' => {
                    end = world.pos.len() as i64;
                    'z' as i64 - 'a' as i64
                }
                'a'..='z' => oneChar as i64 - 'a' as i64,
                _ => panic!("Test"),
            };
            world.pos.push(value);
        }
        world.w = line.len() as i64;
        world.h += 1;
    }

    let steps: i64 = world.findPath(start, end);
    println!("{}", steps);

    let steps: i64 = world.findNearestBottom(end);
    println!("{}", steps);
}

fn part2(_text: &String) {}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
