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

    // Part 1.
    let mut elvesCalories: Vec<i64> = Vec::new();
    elvesCalories.push(0);
    for line in text.lines() {
        if (line.is_empty()) {
            elvesCalories.push(0);
        } else {
            let calories: i64 = line.parse::<i64>().unwrap();
            *elvesCalories.last_mut().unwrap() += calories;
        }
    }
    let maxCalories: &i64 = elvesCalories.iter().max().unwrap();
    println!("Max: {}", maxCalories);

    // Part 2.
    elvesCalories.sort();
    elvesCalories.reverse();
    let max3Calories: i64 = elvesCalories[0] + elvesCalories[1] + elvesCalories[2];
    println!("Max 3: {}", max3Calories);
}
