#![allow(non_snake_case)]
#![allow(unused_parens)]
//#![allow(unused_variables)]

use serde_json;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

#[derive(Debug, PartialEq)]
enum Order {
    Correct,
    Wrong,
    Same,
}

fn compare(left: &Vec<serde_json::Value>, right: &Vec<serde_json::Value>) -> Order {
    let nItems = std::cmp::min(left.len(), right.len());
    for i in 0..nItems {
        let valueL = left.get(i).unwrap();
        let valueR = right.get(i).unwrap();
        if (valueL.is_i64() && valueR.is_i64()) {
            let numberL = valueL.as_i64().unwrap();
            let numberR = valueR.as_i64().unwrap();
            if (numberL < numberR) {
                return Order::Correct;
            } else if (numberL > numberR) {
                return Order::Wrong;
            }
        } else if (valueL.is_array() && valueR.is_array()) {
            let arrayResult = compare(valueL.as_array().unwrap(), valueR.as_array().unwrap());
            if (arrayResult != Order::Same) {
                return arrayResult;
            }
        } else {
            if (!(valueL.is_i64() || valueR.is_i64())) {
                panic!("One of the values is not integer!")
            }

            let mut newValueL: Vec<serde_json::Value>;
            if (valueL.is_i64()) {
                newValueL = Vec::new();
                let value = serde_json::json!(valueL.as_i64().unwrap());
                newValueL.push(value);
            } else {
                newValueL = valueL.as_array().unwrap().clone();
            }
            let mut newValueR: Vec<serde_json::Value>;
            if (valueR.is_i64()) {
                newValueR = Vec::new();
                let value = serde_json::json!(valueR.as_i64().unwrap());
                newValueR.push(value);
            } else {
                newValueR = valueR.as_array().unwrap().clone();
            }

            let arrayResult = compare(&newValueL, &newValueR);
            if (arrayResult != Order::Same) {
                return arrayResult;
            }
        }
    }

    if (left.len() < right.len()) {
        return Order::Correct;
    } else if (left.len() > right.len()) {
        return Order::Wrong;
    }
    return Order::Same;
}

fn part1(text: &String) {
    let mut lines = text.lines();
    let mut sum: i64 = 0;
    let mut counter: i64 = 1;
    loop {
        let nextLine = lines.next();
        if (nextLine.is_none()) {
            break;
        }

        let first = nextLine.unwrap();
        let second = lines.next().unwrap();
        lines.next();

        // println!("{}", first);
        // println!("{}", second);
        let left: Vec<serde_json::Value> = serde_json::from_str::<serde_json::Value>(first)
            .unwrap()
            .as_array()
            .unwrap()
            .clone();
        let right: Vec<serde_json::Value> = serde_json::from_str::<serde_json::Value>(second)
            .unwrap()
            .as_array()
            .unwrap()
            .clone();
        //println!("{:?}", left);
        //println!("{:?}", right);

        let result = compare(&left, &right);
        //println!("{:?}\n", result);
        if (result == Order::Correct) {
            sum += counter;
        }
        counter += 1;
    }
    println!("Result: {}", sum);
}

fn part2(text: &String) {
    let mut lines = text.lines();
    let mut packets: Vec<Vec<serde_json::Value>> = Vec::new();
    loop {
        let nextLine = lines.next();
        if (nextLine.is_none()) {
            break;
        }

        let first = nextLine.unwrap();
        let second = lines.next().unwrap();
        lines.next();

        let left: Vec<serde_json::Value> = serde_json::from_str::<serde_json::Value>(first)
            .unwrap()
            .as_array()
            .unwrap()
            .clone();
        let right: Vec<serde_json::Value> = serde_json::from_str::<serde_json::Value>(second)
            .unwrap()
            .as_array()
            .unwrap()
            .clone();

        packets.push(left);
        packets.push(right);
    }

    // for packet in packets.iter() {
    //     println!("{:?}", packet);
    // }
    // println!();
    let compareFunc =
        |a: &Vec<serde_json::Value>, b: &Vec<serde_json::Value>| -> std::cmp::Ordering {
            let result = compare(a, b);
            let order = match result {
                Order::Correct => std::cmp::Ordering::Less,
                Order::Wrong => std::cmp::Ordering::Greater,
                Order::Same => std::cmp::Ordering::Equal,
            };
            return order;
        };
    //packets.sort_by(|a: &Vec<serde_json::Value>, b: &Vec<serde_json::Value>| std::cmp::Ordering::Less);
    packets.sort_by(compareFunc);
    // for packet in packets.iter() {
    //     println!("{:?}", packet);
    // }
    // Find [[2]] and [[6]] indices.
    let mut result: i64 = 1;
    for i in 0..packets.len() {
        // [Array [Number(2)]] || [Array [Number(6)]]
        let value = packets.get(i).unwrap();
        if (value.len() == 1 && value.get(0).unwrap().is_array()) {
            let valueArray = value.get(0).unwrap().as_array().unwrap();
            if (valueArray.len() == 1
                && valueArray.get(0).unwrap().is_number()
                && (valueArray.get(0).unwrap().as_i64().unwrap() == 2
                    || valueArray.get(0).unwrap().as_i64().unwrap() == 6))
            {
                result *= (i as i64 + 1);
            }
        }
    }
    println!("Result: {}", result);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    let text2 = text + "\n[[2]]\n[[6]]\n";
    part2(&text2);
}
