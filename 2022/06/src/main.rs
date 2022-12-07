#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashSet;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

fn part1(text: &String, nTarget: usize) {
    let chars: Vec<char> = text.chars().collect();
    let mut count: usize = nTarget;
    for x in chars.windows(count) {
        //println!("{:?}", x);
        let set: HashSet<&char> = HashSet::from_iter(x.iter());
        if (set.len() == x.len()) {
            break;
        }
        count += 1;
    }
    println!("{}", count);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text, 4);
    part1(&text, 14);
}
