use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

fn part1(text: &String) {
    let mut sum: i64 = 0;
    for line in text.lines() {
        // Get first number from beginning.
        for c in line.chars() {
            if (c.is_numeric()) {
                sum += c.to_digit(10).unwrap() as i64 * 10;
                break;
            }
        }
        // Get second number from end.
        for c in line.chars().rev() {
            if (c.is_numeric()) {
                sum += c.to_digit(10).unwrap() as i64;
                break;
            }
        }
    }
    println!("Result: {}", sum);
}

fn strToNumber(numberStr: &str) -> i64 {
    return match numberStr {
        "zero" => 0,
        "one" => 1,
        "two" => 2,
        "three" => 3,
        "four" => 4,
        "five" => 5,
        "six" => 6,
        "seven" => 7,
        "eight" => 8,
        "nine" => 9,
        "0" => 0,
        "1" => 1,
        "2" => 2,
        "3" => 3,
        "4" => 4,
        "5" => 5,
        "6" => 6,
        "7" => 7,
        "8" => 8,
        "9" => 9,
        _ => panic!("Error!"),
    };
}

fn part2(text: &String) {
    let mut sum: i64 = 0;
    for line in text.lines() {
        let numbersStr: Vec<&str> = [
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "1", "2", "3",
            "4", "5", "6", "7", "8", "9",
        ]
        .to_vec();

        // Get first number from beginning.
        let mut lowestIndex: usize = line.len();
        let mut firstNumber: i64 = 0;
        for nStr in numbersStr.iter() {
            let index = line.find(nStr);
            if (index.is_some() && index.unwrap() < lowestIndex) {
                lowestIndex = index.unwrap();
                firstNumber = strToNumber(nStr);
            }
        }

        // Get second number from end.
        let mut highestIndex = 0;
        let mut secondNumber: i64 = 0;
        for nStr in numbersStr.iter() {
            let index = line.rfind(nStr);
            if (index.is_some() && index.unwrap() >= highestIndex) {
                highestIndex = index.unwrap();
                secondNumber = strToNumber(nStr);
            }
        }

        sum += firstNumber * 10 + secondNumber;
    }
    println!("Result: {}", sum);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
