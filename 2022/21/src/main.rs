#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use std::cell::RefCell;
use std::collections::HashMap;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

#[derive(Debug)]
struct Value {
    num: Option<i64>,
    operation: String,
}

fn solveOperation(
    name: &String,
    values: &mut HashMap<String, RefCell<Value>>,
    write: &mut bool,
) -> i64 {
    {
        let value = values.get(name).unwrap().borrow();
        if (value.num.is_some()) {
            return value.num.unwrap();
        }
    }

    // Solve operation.
    let operation: String = values.get(name).unwrap().borrow().operation.clone();
    let opSplit = operation.split_whitespace().collect::<Vec<&str>>();
    let str1 = opSplit.get(0).unwrap();
    let str2 = opSplit.get(2).unwrap();
    let mut write1: bool = true;
    let num1 = solveOperation(&str1.to_string(), values, &mut write1);
    let mut write2: bool = true;
    let num2 = solveOperation(&str2.to_string(), values, &mut write2);
    if (str1 == &"humn" || str2 == &"humn" || !write1 || !write2) {
        *write = false;
    }
    let num = match opSplit.get(1).unwrap() {
        &"+" => num1 + num2,
        &"-" => num1 - num2,
        &"*" => num1 * num2,
        &"/" => num1 / num2,
        _ => panic!("Wrong operation!"),
    };
    if (*write) {
        let mut value = values.get(name).unwrap().borrow_mut();
        value.num = Some(num);
    }
    return num;
}

fn findSolution(targetName: &String, values: &mut HashMap<String, RefCell<Value>>) -> i64 {
    let mut num: i64 = {
        let value = values.get(targetName).unwrap().borrow();
        value.num.unwrap()
    };

    if (targetName == &"humn") {
        return num;
    }

    let newName: String;
    {
        // Solve operation.
        let operation: String = values.get(targetName).unwrap().borrow().operation.clone();
        let opSplit = operation.split_whitespace().collect::<Vec<&str>>();
        let str1 = opSplit.get(0).unwrap();
        let str2 = opSplit.get(2).unwrap();

        let mut value1 = values.get(&str1.to_string()).unwrap().borrow_mut();
        let mut value2 = values.get(&str2.to_string()).unwrap().borrow_mut();
        if (value1.num.is_none()) {
            // Solve value1.
            let targetNum = match opSplit.get(1).unwrap() {
                &"+" => num - value2.num.unwrap(),
                &"-" => num + value2.num.unwrap(),
                &"*" => num / value2.num.unwrap(),
                &"/" => num * value2.num.unwrap(),
                _ => panic!("Wrong operation!"),
            };

            value1.num = Some(targetNum);
            newName = str1.to_string();
        } else if (value2.num.is_none()) {
            // Solve value2.
            let targetNum = match opSplit.get(1).unwrap() {
                &"+" => num - value1.num.unwrap(),
                &"-" => value1.num.unwrap() - num,
                &"*" => num / value1.num.unwrap(),
                &"/" => value1.num.unwrap() / num,
                _ => panic!("Wrong operation!"),
            };

            value2.num = Some(targetNum);
            newName = str2.to_string();
        } else {
            panic!("Both already solved!");
        }
    }

    {
        num = findSolution(&newName, values);
    }

    return num;
}

fn part1(text: &String) {
    let mut values: HashMap<String, RefCell<Value>> = HashMap::new();

    for line in text.lines() {
        let mut lineSplit = line.split(": ");
        let name = lineSplit.next().unwrap();
        let second = lineSplit.next().unwrap();
        let secondValue = second.parse::<i64>();
        if (secondValue.is_ok()) {
            values.insert(
                name.to_string(),
                RefCell::new(Value {
                    num: Some(secondValue.unwrap()),
                    operation: String::new(),
                }),
            );
        } else {
            values.insert(
                name.to_string(),
                RefCell::new(Value {
                    num: None,
                    operation: second.to_string(),
                }),
            );
        }
    }

    let mut writeNum: bool = true;
    let root = solveOperation(&"root".to_string(), &mut values, &mut writeNum);
    println!("Root = {}", root);
}

fn part2(text: &String) {
    let mut values: HashMap<String, RefCell<Value>> = HashMap::new();

    for line in text.lines() {
        let mut lineSplit = line.split(": ");
        let name = lineSplit.next().unwrap();
        let second = lineSplit.next().unwrap();
        let secondValue = second.parse::<i64>();
        if (secondValue.is_ok()) {
            values.insert(
                name.to_string(),
                RefCell::new(Value {
                    num: Some(secondValue.unwrap()),
                    operation: String::new(),
                }),
            );
        } else {
            values.insert(
                name.to_string(),
                RefCell::new(Value {
                    num: None,
                    operation: second.to_string(),
                }),
            );
        }
    }

    let operation: String = values
        .get(&"root".to_string())
        .unwrap()
        .borrow()
        .operation
        .clone();
    let opSplit = operation.split_whitespace().collect::<Vec<&str>>();
    let str1 = opSplit.get(0).unwrap();
    let str2 = opSplit.get(2).unwrap();
    let mut writeNum1: bool = true;
    let num1 = solveOperation(&str1.to_string(), &mut values, &mut writeNum1);
    let mut writeNum2: bool = true;
    let num2 = solveOperation(&str2.to_string(), &mut values, &mut writeNum2);

    // Which name to solve and what number is equal.
    let (targetNum, targetName): (i64, String) = {
        if (writeNum2) {
            (num2, str1.to_string())
        } else if (writeNum1) {
            (num1, str2.to_string())
        } else {
            panic!("Wrong!");
        }
    };

    // for name in &values {
    //     println!("{:?}", name);
    // }

    {
        let mut value = values.get(&targetName).unwrap().borrow_mut();
        value.num = Some(targetNum);
    }
    {
        let mut value = values.get(&"humn".to_string()).unwrap().borrow_mut();
        value.num = None;
    }

    let humn = findSolution(&targetName, &mut values);
    println!("Humn = {}", humn);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
