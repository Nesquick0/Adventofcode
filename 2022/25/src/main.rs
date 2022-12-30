#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

fn snafuToDec(from: &str) -> i64 {
    let mut result: i64 = 0;
    for (i, c) in from.chars().rev().enumerate() {
        let v: i64 = match c {
            '2' => 2,
            '1' => 1,
            '0' => 0,
            '-' => -1,
            '=' => -2,
            _ => panic!("Wrong character!"),
        };
        result += (5 as i64).pow(i as u32) * v;
    }
    return result;
}

fn decToSnafu(from: i64) -> String {
    let mut digits: Vec<i64> = Vec::new();
    let mut decValue = from;
    while (decValue > 0) {
        decValue += 2;
        digits.push(decValue % 5);
        decValue /= 5;
    }
    digits.reverse();
    digits = digits.iter_mut().map(|v| *v - 2).collect::<Vec<i64>>();
    let mut result: String = String::new();
    for v in &digits {
        result.push(match v {
            2 => '2',
            1 => '1',
            0 => '0',
            -1 => '-',
            -2 => '=',
            _ => panic!("Wrong character!"),
        });
    }
    return result;
}

fn part1(text: &String) {
    let mut sumDecimal: i64 = 0;
    for line in text.lines() {
        let value = snafuToDec(line);
        //println!("{} {}", line, value);
        sumDecimal += value;
    }
    println!("Sum decimal: {}", sumDecimal);
    println!("Sum snafu: {}", decToSnafu(sumDecimal));
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
}
