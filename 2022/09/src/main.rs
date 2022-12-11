#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashSet;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

struct Knot {
    x: i64,
    y: i64,
}

impl Knot {
    pub fn new() -> Self {
        Self { x: 0, y: 0 }
    }

    fn moveKnot(&mut self, dir: (i64, i64)) {
        self.x += dir.0;
        self.y += dir.1;
    }

    fn calculateDir(&self, head: &Knot) -> (i64, i64) {
        // Same place.
        if (self.x == head.x && self.y == head.y) {
            return (0, 0);
        }
        // Next to each other.
        if ((head.x - self.x).abs() <= 1 && (head.y - self.y).abs() <= 1) {
            return (0, 0);
        }
        return ((head.x - self.x).signum(), (head.y - self.y).signum());
    }
}

fn part1(text: &String) {
    let mut head: Knot = Knot::new();
    let mut tail: Knot = Knot::new();
    let mut visited: HashSet<(i64, i64)> = HashSet::new();
    visited.insert((tail.x, tail.y));

    for line in text.lines() {
        let split: Vec<&str> = line.split_whitespace().collect();
        let (direction, distance): (&str, i64) = (split[0], split[1].parse::<i64>().unwrap());
        let dir = match &direction {
            &"R" => (1, 0),
            &"L" => (-1, 0),
            &"U" => (0, -1),
            &"D" => (0, 1),
            _ => (0, 0),
        };
        for _ in 0..distance {
            head.moveKnot(dir);
            let tailDir = tail.calculateDir(&head);
            tail.moveKnot(tailDir);
            visited.insert((tail.x, tail.y));
        }
        //println!("{} {} ; {} {}", head.x, head.y, tail.x, tail.y);
    }
    println!("Visited: {}", visited.len());
}

fn part2(text: &String) {
    let mut knots: Vec<Knot> = Vec::new();
    for _ in 0..10 {
        knots.push(Knot::new());
    }
    let mut visited: HashSet<(i64, i64)> = HashSet::new();

    for line in text.lines() {
        let split: Vec<&str> = line.split_whitespace().collect();
        let (direction, distance): (&str, i64) = (split[0], split[1].parse::<i64>().unwrap());
        let dir = match &direction {
            &"R" => (1, 0),
            &"L" => (-1, 0),
            &"U" => (0, -1),
            &"D" => (0, 1),
            _ => (0, 0),
        };
        for _ in 0..distance {
            knots.first_mut().unwrap().moveKnot(dir);

            for i in 1..knots.len() {
                let tailDir = {
                    let tail = knots.get(i).unwrap();
                    tail.calculateDir(knots.get(i - 1).unwrap())
                };

                let tail: &mut Knot = knots.get_mut(i).unwrap();
                tail.moveKnot(tailDir);
            }

            visited.insert((knots.last().unwrap().x, knots.last().unwrap().y));
        }
        //println!("{} {} ; {} {}", head.x, head.y, tail.x, tail.y);
    }
    println!("Visited: {}", visited.len());
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
