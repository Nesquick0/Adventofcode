#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use std::collections::VecDeque;
use std::fs;
use std::rc::Rc;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

#[derive(Debug)]
struct Item {
    value: i64,
    origPos: usize,
}

impl Item {
    pub fn new(value: i64, origPos: usize) -> Self {
        Self {
            value: value,
            origPos: origPos,
        }
    }
}

fn part1(text: &String) {
    let mut list: VecDeque<Rc<Item>> = VecDeque::new();

    for (i, line) in text.lines().enumerate() {
        let value: i64 = line.parse::<i64>().unwrap();
        let item: Item = Item::new(value, i);
        list.push_back(Rc::new(item));
    }

    // For each item shift position.
    for i in 0..list.len() {
        // Find item by original position.
        let mut item: Option<Rc<Item>> = None;
        let mut curPos: usize = 0;
        for j in 0..list.len() {
            let testItem = list.get(j).unwrap();
            if (testItem.origPos == i) {
                item = Some(testItem.clone());
                curPos = j;
            }
        }
        let value = item.as_ref().unwrap().value;
        list.remove(curPos);
        let mut targetPos = (curPos as i64 + value).rem_euclid(list.len() as i64) as usize;
        if (targetPos == 0) {
            targetPos = list.len();
        }
        list.insert(targetPos, item.as_ref().unwrap().clone());
        // for item in &list {
        //     print!("{}, ", item.value);
        // }
        // println!();
    }

    // Get values for result.
    let mut zeroOffset: usize = 0;
    for (i, item) in list.iter().enumerate() {
        if (item.value == 0) {
            zeroOffset = i;
            break;
        }
    }
    let mut result: i64 = 0;
    for pos in [1000, 2000, 3000] {
        let value = list
            .get((pos as usize + zeroOffset).rem_euclid(list.len()))
            .unwrap();
        println!("{}", value.value);
        result += value.value;
    }
    println!("Result: {}", result);
}

fn part2(text: &String) {
    let mut list: VecDeque<Rc<Item>> = VecDeque::new();

    for (i, line) in text.lines().enumerate() {
        let value: i64 = line.parse::<i64>().unwrap() * 811589153;
        let item: Item = Item::new(value, i);
        list.push_back(Rc::new(item));
    }

    // For each item shift position.
    for _ in 0..10 {
        for i in 0..list.len() {
            // Find item by original position.
            let mut item: Option<Rc<Item>> = None;
            let mut curPos: usize = 0;
            for j in 0..list.len() {
                let testItem = list.get(j).unwrap();
                if (testItem.origPos == i) {
                    item = Some(testItem.clone());
                    curPos = j;
                }
            }
            let value = item.as_ref().unwrap().value;
            list.remove(curPos);
            let mut targetPos = (curPos as i64 + value).rem_euclid(list.len() as i64) as usize;
            if (targetPos == 0) {
                targetPos = list.len();
            }
            list.insert(targetPos, item.as_ref().unwrap().clone());
            // for item in &list {
            //     print!("{}, ", item.value);
            // }
            // println!();
        }
    }

    // Get values for result.
    let mut zeroOffset: usize = 0;
    for (i, item) in list.iter().enumerate() {
        if (item.value == 0) {
            zeroOffset = i;
            break;
        }
    }
    let mut result: i64 = 0;
    for pos in [1000, 2000, 3000] {
        let value = list
            .get((pos as usize + zeroOffset).rem_euclid(list.len()))
            .unwrap();
        println!("{}", value.value);
        result += value.value;
    }
    println!("Result: {}", result);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
