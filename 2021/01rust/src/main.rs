#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::io::Read;

fn readToString(filename: &str) -> std::io::Result<String> {
    let mut file = std::fs::File::open(&filename)?;
    let mut text = String::new();
    file.read_to_string(&mut text)?;
    Ok(text)
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    let numbers: Vec<i64> = text.lines().map(|x| x.parse::<i64>().unwrap()).collect();

    // Part one.
    let mut count: i64 = 0;
    for i in (1..numbers.len()) {
        if (numbers[i] > numbers[i - 1]) {
            count += 1;
        }
    }
    println!("{}", count);

    // Part two.
    let mut slidingNumbers: Vec<i64> = Vec::new();
    for i in (0..numbers.len() - 2) {
        slidingNumbers.push(numbers[i..i + 3].iter().sum::<i64>());
    }

    let mut count2: i64 = 0;
    for i in (1..slidingNumbers.len()) {
        if (slidingNumbers[i] > slidingNumbers[i - 1]) {
            count2 += 1;
        }
    }
    println!("{}", count2);
}
