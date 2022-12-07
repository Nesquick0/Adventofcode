#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashSet;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

fn charToValue(oneChar: char) -> i64 {
    return match oneChar {
        'a'..='z' => oneChar as i64 - 'a' as i64 + 1,
        'A'..='Z' => oneChar as i64 - 'A' as i64 + 27,
        _ => 0,
    };
}

fn part1(text: &String) {
    // Part 1.
    let mut totalSum: i64 = 0;
    for line in text.lines() {
        let nItems = line.len();
        let nHalf = nItems / 2;

        let mut first: HashSet<char> = HashSet::new();
        let mut second: HashSet<char> = HashSet::new();
        let mut chars = line.chars();
        for _ in 0..nHalf {
            let oneChar: char = chars.next().unwrap();
            first.insert(oneChar);
        }
        for _ in nHalf..nItems {
            let oneChar: char = chars.next().unwrap();
            if (first.contains(&oneChar) && !second.contains(&oneChar)) {
                //println!("{}", oneChar);
                totalSum += charToValue(oneChar);
            }
            second.insert(oneChar);
        }
    }
    println!("{}", totalSum);
}

fn part2(text: &String) {
    // Part 2.
    let mut totalSum: i64 = 0;
    let mut counter = 0;
    let mut badges: HashSet<char> = HashSet::new();
    for line in text.lines() {
        if (counter == 0) {
            badges.clear();
            line.chars().for_each(|x| {
                badges.insert(x);
            });
        } else {
            let mut tempChars: HashSet<char> = HashSet::new();
            line.chars().for_each(|x| {
                tempChars.insert(x);
            });
            badges.retain(|x| tempChars.contains(x));
        }
        counter = (counter + 1) % 3;
        if (counter == 0) {
            assert!(badges.len() == 1);
            let oneChar: &char = badges.iter().next().unwrap();
            totalSum += charToValue(*oneChar);
        }
    }
    println!("{}", totalSum);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
