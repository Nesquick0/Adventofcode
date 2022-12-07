#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::io::Read;

fn readToString(filename: &str) -> std::io::Result<String> {
    let mut file = std::fs::File::open(&filename)?;
    let mut text = String::new();
    file.read_to_string(&mut text)?;
    Ok(text)
}

fn part1(text: &String) {
    // Part 1.
    let mut totalScore: i64 = 0;
    for line in text.lines() {
        let mut split = line.split(" ");
        let (aT, bT) = (split.next().unwrap(), split.next().unwrap());
        let a: i64 = aT.chars().next().unwrap() as i64 - 'A' as i64;
        let b: i64 = bT.chars().next().unwrap() as i64 - 'X' as i64;

        let mut score: i64 = b + 1;
        let mut diff: i64 = (b - a);
        if (diff < 0) {
            diff += 3;
        }
        score += match (diff) {
            0 => 3,
            1 => 6,
            2 => 0,
            _ => 0,
        };

        totalScore += score;
    }
    println!("Score: {}", totalScore);
}

fn part2(text: &String) {
    // Part 2.
    let mut totalScore: i64 = 0;
    for line in text.lines() {
        let mut split = line.split(" ");
        let (aT, bT) = (split.next().unwrap(), split.next().unwrap());
        let a: i64 = aT.chars().next().unwrap() as i64 - 'A' as i64;
        let b: i64 = bT.chars().next().unwrap() as i64 - 'X' as i64;

        let mut score: i64 = b * 3;
        score += match (b) {
            0 => (a - 1).rem_euclid(3),
            1 => a,
            2 => (a + 1).rem_euclid(3),
            _ => 0,
        } + 1;

        totalScore += score;
    }
    println!("Score: {}", totalScore);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
