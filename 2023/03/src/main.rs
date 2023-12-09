use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

struct Value {
    value: i64,
    coords: Vec<(usize, usize)>,
}

impl Value {
    fn new() -> Value {
        Value {
            value: 0,
            coords: Vec::new(),
        }
    }
}

fn getAllValues(text: &String) -> Vec<Value> {
    let mut allValues: Vec<Value> = Vec::new();
    for (y, line) in text.lines().enumerate() {
        let mut lastValueStr: String = String::new();
        let lineWidth: usize = line.chars().count();
        for (x, c) in line.chars().enumerate() {
            if (c.is_digit(10)) {
                lastValueStr.push(c);
            } else if (!lastValueStr.is_empty()) {
                // Value finished.
                let lastValue: i64 = lastValueStr.parse().unwrap();
                let mut newValue: Value = Value::new();
                newValue.value = lastValue;
                for i in 0..lastValueStr.len() {
                    newValue.coords.push((x - i - 1, y));
                }

                allValues.push(newValue);
                lastValueStr.clear();
            }
        }

        if (!lastValueStr.is_empty()) {
            // Value finished.
            let lastValue: i64 = lastValueStr.parse().unwrap();
            let mut newValue: Value = Value::new();
            newValue.value = lastValue;
            for i in 0..lastValueStr.len() {
                newValue.coords.push((lineWidth - i - 1, y));
            }

            allValues.push(newValue);
            lastValueStr.clear();
        }
    }
    return allValues;
}

fn checkCoordinates(value: &Value, x: usize, y: usize) -> i64 {
    for coord in &value.coords {
        if (coord.0.abs_diff(x) <= 1 && coord.1.abs_diff(y) <= 1) {
            return value.value;
        }
    }
    return 0;
}

fn part1(text: &String) {
    let mut sum: i64 = 0;
    let allValues: Vec<Value> = getAllValues(text);

    for (y, line) in text.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if (!c.is_digit(10) && c != '.') {
                // It is symbol. Found values around.
                for value in &allValues {
                    let valueFound: i64 = checkCoordinates(&value, x, y);
                    sum += valueFound;
                }
            }
        }
    }
    println!("Result: {}", sum);
}

fn part2(text: &String) {
    let mut sum: i64 = 0;
    let allValues: Vec<Value> = getAllValues(text);

    for (y, line) in text.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if (c == '*') {
                // This is gear. Check whether is has exactly 2 values around.
                let mut counter: i64 = 0;
                let mut gearRatio: i64 = 1;
                for value in &allValues {
                    let valueFound: i64 = checkCoordinates(&value, x, y);
                    if (valueFound != 0) {
                        gearRatio *= valueFound;
                        counter += 1;
                    }
                }

                if (counter == 2) {
                    sum += gearRatio;
                }
            }
        }
    }
    println!("Result: {}", sum);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
