use regex::Regex;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

fn getGameValues(results: &str) -> [i64; 3] {
    let mut maxValues: [i64; 3] = [0; 3];
    let reValue = Regex::new(r"(\d+) (\w+)").unwrap();
    for gameStr in results.split("; ").into_iter() {
        let values: Vec<&str> = gameStr.split(", ").collect::<Vec<&str>>();
        for value in values {
            let mValue = reValue.captures(value).unwrap();
            let items: i64 = mValue.get(1).unwrap().as_str().parse::<i64>().unwrap();
            let name: &str = mValue.get(2).unwrap().as_str();
            match name {
                "red" => maxValues[0] = std::cmp::max(maxValues[0], items),
                "green" => maxValues[1] = std::cmp::max(maxValues[1], items),
                "blue" => maxValues[2] = std::cmp::max(maxValues[2], items),
                _ => panic!("Unknown item: {}", name),
            }
        }
    }
    return maxValues;
}

fn part1(text: &String) {
    let mut sum: i64 = 0;
    for line in text.lines() {
        let reAll = Regex::new(r"Game (\d+): (.+)").unwrap();
        let m = reAll.captures(line).unwrap();
        let gameId: i64 = m.get(1).unwrap().as_str().parse::<i64>().unwrap();
        let results: &str = m.get(2).unwrap().as_str();

        let maxValues: [i64; 3] = getGameValues(results);

        // Check if game is possible. Max values must be at most 12 red cubes, 13 green cubes, and 14 blue cubes.
        if (maxValues[0] <= 12 && maxValues[1] <= 13 && maxValues[2] <= 14) {
            sum += gameId;
        }
    }
    println!("Result: {}", sum);
}

fn part2(text: &String) {
    let mut sum: i64 = 0;
    for line in text.lines() {
        let reAll = Regex::new(r"Game (\d+): (.+)").unwrap();
        let m = reAll.captures(line).unwrap();
        let results: &str = m.get(2).unwrap().as_str();

        let maxValues: [i64; 3] = getGameValues(results);

        // Get multiply of max values.
        let result: i64 = maxValues[0] * maxValues[1] * maxValues[2];
        sum += result;
    }
    println!("Result: {}", sum);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
