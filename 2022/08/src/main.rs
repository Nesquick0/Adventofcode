#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

struct World {
    trees: Vec<i64>,
    w: usize,
    h: usize,
}

impl World {
    pub fn new() -> Self {
        Self {
            trees: Vec::new(),
            w: 0,
            h: 0,
        }
    }

    fn load(&mut self, text: &String) {
        let lines: Vec<&str> = text.lines().collect();
        self.w = lines[0].len();
        self.h = lines.len();

        for line in lines.iter() {
            for oneChar in line.chars() {
                self.trees.push(oneChar.to_string().parse::<i64>().unwrap());
            }
        }
    }

    fn isVisible(&self, i: usize) -> bool {
        let x: i64 = (i % self.w) as i64;
        let y: i64 = (i / self.w) as i64;

        // Border is visible.
        if (x == 0 || x == self.w as i64 - 1 || y == 0 || y == self.h as i64 - 1) {
            return true;
        }

        let height = self.trees[i];
        // Check each direction.
        let mut treeVisible: bool = false;
        let dirs: [(i64, i64); 4] = [(0, -1), (1, 0), (0, 1), (-1, 0)];
        for dir in dirs {
            let mut visible: bool = true;
            let mut curX = x + dir.0;
            let mut curY = y + dir.1;
            while (visible
                && curX >= 0
                && curX < self.w as i64
                && curY >= 0
                && curY < self.h as i64)
            {
                if (self.trees[curX as usize + curY as usize * self.w] >= height) {
                    visible = false;
                    break;
                }
                curX += dir.0;
                curY += dir.1;
            }
            if (visible) {
                treeVisible = true;
                break;
            }
        }
        return treeVisible;
    }

    fn scenicScore(&self, i: usize) -> i64 {
        let x: i64 = (i % self.w) as i64;
        let y: i64 = (i / self.w) as i64;

        let height = self.trees[i];

        // Check each direction.
        let mut score: i64 = 1;
        let dirs: [(i64, i64); 4] = [(0, -1), (1, 0), (0, 1), (-1, 0)];
        for dir in dirs {
            let mut dirScore: i64 = 0;
            let mut curX = x + dir.0;
            let mut curY = y + dir.1;
            while (curX >= 0 && curX < self.w as i64 && curY >= 0 && curY < self.h as i64) {
                dirScore += 1;
                if (self.trees[curX as usize + curY as usize * self.w] >= height) {
                    break;
                }
                curX += dir.0;
                curY += dir.1;
            }
            score *= dirScore;
        }
        return score;
    }
}

fn part1(world: &World) {
    let mut count: i64 = 0;
    for i in 0..world.trees.len() {
        if (world.isVisible(i)) {
            count += 1;
        }
    }
    println!("{}", count);
}

fn part2(world: &World) {
    let mut maxScore: i64 = 0;
    for i in 0..world.trees.len() {
        let score = world.scenicScore(i);
        maxScore = std::cmp::max(maxScore, score);
    }
    println!("{}", maxScore);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");
    let mut world = World::new();
    world.load(&text);

    part1(&world);
    part2(&world);
}
