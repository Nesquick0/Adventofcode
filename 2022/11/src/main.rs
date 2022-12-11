#![allow(non_snake_case)]
#![allow(unused_parens)]

use regex::Regex;
use std::cell::RefCell;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

struct Monkey {
    id: i64,
    items: Vec<i64>,
    operation: Box<dyn Fn(i64, Option<i64>) -> i64>,
    operationValue: Option<i64>,
    devisible: i64,
    targetTrue: i64,
    targetFalse: i64,
    countInspections: i64,
}

impl Monkey {
    pub fn new(
        id: i64,
        items: Vec<i64>,
        operation: Box<dyn Fn(i64, Option<i64>) -> i64>,
        operationValue: Option<i64>,
        devisible: i64,
        targetTrue: i64,
        targetFalse: i64,
    ) -> Self {
        Self {
            id,
            items,
            operation,
            operationValue,
            devisible,
            targetTrue,
            targetFalse,
            countInspections: 0,
        }
    }
}

fn parseOperation(operationStr: &String) -> (Box<dyn Fn(i64, Option<i64>) -> i64>, Option<i64>) {
    let operationSplit = operationStr.split_whitespace().collect::<Vec<&str>>();
    let operFirst = operationSplit.get(0).unwrap();
    let operSecond = operationSplit.get(1).unwrap();
    if (operFirst == &"+") {
        if (operSecond == &"old") {
            return (Box::new(|x, _| x + x), None);
        } else {
            let valueSecond: i64 = operSecond.parse::<i64>().unwrap();
            return (Box::new(|x, y| x + y.unwrap()), Some(valueSecond));
        }
    } else {
        if (operSecond == &"old") {
            return (Box::new(|x, _| x * x), None);
        } else {
            let valueSecond: i64 = operSecond.parse::<i64>().unwrap();
            return (Box::new(|x, y| x * y.unwrap()), Some(valueSecond));
        }
    }
}

fn part1(text: &String) {
    let lines: Vec<&str> = text.lines().collect();
    let patternMonkey = Regex::new(r"^Monkey (\d+):$").unwrap();
    let mut Monkeys: Vec<RefCell<Monkey>> = Vec::new();

    for chunk in lines.chunks(7) {
        // Parse simple values.
        let id = patternMonkey
            .captures(chunk[0])
            .unwrap()
            .get(1)
            .unwrap()
            .as_str()
            .parse::<i64>()
            .unwrap();
        let items: Vec<i64> = chunk[1]
            .replace("  Starting items: ", "")
            .split(", ")
            .collect::<Vec<&str>>()
            .iter()
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>();
        let devisible = chunk[3]
            .replace("  Test: divisible by ", "")
            .parse::<i64>()
            .unwrap();
        let targetTrue = chunk[4]
            .replace("    If true: throw to monkey ", "")
            .parse::<i64>()
            .unwrap();
        let targetFalse = chunk[5]
            .replace("    If false: throw to monkey ", "")
            .parse::<i64>()
            .unwrap();

        // Parse operation.
        let operationStr = chunk[2].replace("  Operation: new = old ", "");
        let operation = parseOperation(&operationStr);

        let monkey: Monkey = Monkey::new(
            id,
            items,
            operation.0,
            operation.1,
            devisible,
            targetTrue,
            targetFalse,
        );
        Monkeys.push(RefCell::new(monkey));
    }

    // Simulate rounds.
    for _ in 1..=20 {
        for monkey in Monkeys.iter() {
            for item in monkey.borrow().items.iter() {
                let mut newItem =
                    (monkey.borrow().operation)(*item, monkey.borrow().operationValue);
                newItem = newItem / 3;
                let target = if (newItem % monkey.borrow().devisible == 0) {
                    Monkeys.get(monkey.borrow().targetTrue as usize).unwrap()
                } else {
                    Monkeys.get(monkey.borrow().targetFalse as usize).unwrap()
                };
                target.borrow_mut().items.push(newItem);
            }
            let inspections: i64 = monkey.borrow().items.len() as i64;
            monkey.borrow_mut().countInspections += inspections;
            monkey.borrow_mut().items.clear();
        }

        // for monkey in Monkeys.iter() {
        //     println!("{} {:?}", monkey.borrow().id, monkey.borrow().items);
        // }
    }
    let mut mostActive: Vec<i64> = Vec::new();
    for monkey in Monkeys.iter() {
        println!(
            "{} {}",
            monkey.borrow().id,
            monkey.borrow().countInspections
        );
        mostActive.push(monkey.borrow().countInspections);
    }
    mostActive.sort();
    mostActive.reverse();
    println!("{:?}", mostActive);
    println!(
        "Result: {}",
        mostActive.get(0).unwrap() * mostActive.get(1).unwrap()
    )
}

fn part2(_text: &String) {}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
