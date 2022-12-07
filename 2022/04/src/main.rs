#![allow(non_snake_case)]
#![allow(unused_parens)]

use regex::Regex;
use std::fs;

fn part1(text: &String) {
    // Regular expression to parse range of ids 1-2,3-4.
    let patternIds = Regex::new(r"^(?P<a1>\d+)-(?P<a2>\d+),(?P<b1>\d+)-(?P<b2>\d+)$").unwrap();
    let mut counter: i64 = 0;
    let mut counterOverlap: i64 = 0;
    for line in text.lines() {
        let m = patternIds.captures(line).unwrap();
        let (a1, a2, b1, b2) = (
            m.name("a1").unwrap().as_str().parse::<i64>().unwrap(),
            m.name("a2").unwrap().as_str().parse::<i64>().unwrap(),
            m.name("b1").unwrap().as_str().parse::<i64>().unwrap(),
            m.name("b2").unwrap().as_str().parse::<i64>().unwrap(),
        );
        //println!("{}-{},{}-{}", a1, a2, b1, b2);
        // Find ranges that one is all in other.
        if (a1 <= b1 && a2 >= b2) {
            counter += 1;
        } else if (b1 <= a1 && b2 >= a2) {
            counter += 1;
        }
        // One border is at same place as other border.
        else if (a2 == b1 || b2 == a1) {
            counterOverlap += 1;
        }
        // First overlap with second.
        else if (a1 < b1 && a2 > b1) {
            counterOverlap += 1;
        }
        // Second overlap with first.
        else if (b1 < a1 && b2 > a1) {
            counterOverlap += 1;
        }
    }
    println!("{}", counter);
    println!("{}", counter + counterOverlap);
}

fn part2(_text: &String) {}

fn main() {
    let text: String = fs::read_to_string("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
