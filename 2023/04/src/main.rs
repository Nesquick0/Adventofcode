use std::collections::HashSet;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

fn part1(text: &String) {
    let mut sum: i64 = 0;
    for line in text.lines() {
        let lineSplit = line.split(": ").collect::<Vec<&str>>()[1]
            .split(" | ")
            .collect::<Vec<&str>>();
        let winValues = lineSplit[0];
        let yourValues = lineSplit[1];

        let winValuesSet: HashSet<i64> = winValues
            .split_whitespace()
            .map(|x| x.parse::<i64>().unwrap())
            .collect();

        let mut points: i64 = 0;
        for yourValue in yourValues.split_whitespace() {
            let value = yourValue.parse::<i64>().unwrap();
            if (winValuesSet.contains(&value)) {
                if (points == 0) {
                    points = 1;
                } else {
                    points *= 2;
                }
            }
        }
        sum += points;
    }
    println!("Result: {}", sum);
}

fn part2(text: &String) {
    let mut sum: i64 = 0;
    let mut scratchCards: Vec<i64> = Vec::new();
    scratchCards.resize(text.lines().count(), 0);
    for (i, line) in text.lines().enumerate() {
        scratchCards[i] += 1;

        let lineSplit = line.split(": ").collect::<Vec<&str>>()[1]
            .split(" | ")
            .collect::<Vec<&str>>();
        let winValues = lineSplit[0];
        let yourValues = lineSplit[1];

        let winValuesSet: HashSet<i64> = winValues
            .split_whitespace()
            .map(|x| x.parse::<i64>().unwrap())
            .collect();

        let mut numFound: usize = 0;
        for yourValue in yourValues.split_whitespace() {
            let value = yourValue.parse::<i64>().unwrap();
            if (winValuesSet.contains(&value)) {
                numFound += 1;
            }
        }
        for v in 0..numFound {
            let target = i + v + 1;
            if (target < scratchCards.len()) {
                scratchCards[target] += scratchCards[i];
            }
        }
    }

    for num in scratchCards {
        sum += num;
    }
    println!("Result: {}", sum);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
