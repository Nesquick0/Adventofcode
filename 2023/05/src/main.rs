use std::{collections::btree_map::Values, fs};

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

struct Converter {
    sourceStart: i64,
    sourceEnd: i64,
    oper: i64,
}

impl Converter {
    fn new() -> Converter {
        Converter {
            sourceStart: 0,
            sourceEnd: 0,
            oper: 0,
        }
    }
}

fn part1(text: &String) {
    let mut lowestLocation: i64 = i64::MAX;
    let mut lines = text.lines().into_iter();
    let mut converters: Vec<Vec<Converter>> = Vec::new();
    for _ in 0..7 {
        converters.push(Vec::new());
    }

    let seeds: Vec<i64> = lines
        .next()
        .unwrap()
        .split_whitespace()
        .into_iter()
        .skip(1)
        .map(|x| x.parse::<i64>().unwrap())
        .collect::<Vec<i64>>();
    lines.next();
    lines.next();
    let mut counter: i64 = 0;
    while let Some(line) = lines.next() {
        if (line.is_empty()) {
            counter += 1;
            lines.next();
            continue;
        }
        let mut rule: Converter = Converter::new();
        let values: Vec<i64> = line
            .split_whitespace()
            .into_iter()
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>();
        rule.sourceStart = values[1];
        rule.sourceEnd = values[1] + values[2] - 1;
        rule.oper = values[0] - values[1];

        converters[counter as usize].push(rule);
    }

    // Check every seed and it's target location.
    for seed in seeds {
        let mut currentNumber: i64 = seed;
        for category in &converters {
            for converter in category {
                if (currentNumber >= converter.sourceStart && currentNumber <= converter.sourceEnd)
                {
                    currentNumber += converter.oper;
                    break;
                }
            }
            // If not found, keep same number.
        }

        lowestLocation = std::cmp::min(lowestLocation, currentNumber);
    }

    println!("Result: {}", lowestLocation);
}

#[derive(Debug)]
struct ValuesRange {
    start: i64,
    end: i64,
}

impl ValuesRange {
    fn new() -> ValuesRange {
        ValuesRange { start: 0, end: 0 }
    }
}

fn part2(text: &String) {
    let mut lowestLocation: i64 = i64::MAX;
    let mut lines = text.lines().into_iter();
    let mut converters: Vec<Vec<Converter>> = Vec::new();
    for _ in 0..7 {
        converters.push(Vec::new());
    }

    let seeds: Vec<i64> = lines
        .next()
        .unwrap()
        .split_whitespace()
        .into_iter()
        .skip(1)
        .map(|x| x.parse::<i64>().unwrap())
        .collect::<Vec<i64>>();
    let seedsChunks: Vec<&[i64]> = seeds.chunks(2).collect();
    let mut seedRanges: Vec<ValuesRange> = Vec::new();
    for seed in seedsChunks {
        let mut range: ValuesRange = ValuesRange::new();
        range.start = seed[0];
        range.end = seed[0] + seed[1] - 1;
        seedRanges.push(range);
    }

    lines.next();
    lines.next();
    let mut counter: i64 = 0;
    while let Some(line) = lines.next() {
        if (line.is_empty()) {
            counter += 1;
            lines.next();
            continue;
        }
        let mut rule: Converter = Converter::new();
        let values: Vec<i64> = line
            .split_whitespace()
            .into_iter()
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>();
        rule.sourceStart = values[1];
        rule.sourceEnd = values[1] + values[2] - 1;
        rule.oper = values[0] - values[1];

        converters[counter as usize].push(rule);
    }

    // For every iteration of converters process all seeds and create new ranges of values.
    for category in &converters {
        let mut sourceLimits: Vec<i64> = Vec::new();
        for converter in category {
            sourceLimits.push(converter.sourceStart);
            sourceLimits.push(converter.sourceEnd);
        }
        sourceLimits.sort();
        // Now split each seed range and then convert to new values.
        let mut newSeedRanges: Vec<ValuesRange> = Vec::new();
        for seedRange in &seedRanges {
            let mut currentNumber: i64 = seedRange.start;
            for sourceLimit in &sourceLimits {
                if (currentNumber <= *sourceLimit && seedRange.end >= *sourceLimit) {
                    let mut newRange: ValuesRange = ValuesRange::new();
                    newRange.start = currentNumber;
                    newRange.end = *sourceLimit;
                    newSeedRanges.push(newRange);
                }
            }

            let mut newRange: ValuesRange = ValuesRange::new();
            let mut start: i64 = seedRange.start;
            let mut end: i64 = seedRange.end;
            for sourceRange in &sourceLimits {
                if (start <= *sourceRange && end >= *sourceRange) {
                    start += category[(sourceRange - sourceLimits[0]) as usize].oper;
                    end += category[(sourceRange - sourceLimits[0]) as usize].oper;
                }
            }
            newRange.start = start;
            newRange.end = end;
            newSeedRanges.push(newRange);
        }
    }
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    //part1(&text);
    part2(&text);
}
