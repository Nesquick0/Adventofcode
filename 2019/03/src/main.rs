#![allow(non_snake_case)]
#![allow(unused_parens)] 

use std::collections::HashMap;
use std::cmp::min;

fn distance((x1, y1): (i64, i64), (x2, y2): (i64, i64)) -> i64
{
  return i64::abs(x2 - x1) + i64::abs(y2 - y1);
}

fn checkPos(x: i64, y: i64, positions: &HashMap<(i64, i64), i64>, shortestDist: &mut i64, steps: i64, leastSteps: &mut i64)
{
  if (positions.contains_key(&(x, y)))
  {
    *shortestDist = min(*shortestDist, distance((x, y), (0, 0)));
    *leastSteps = min(*leastSteps, *positions.get(&(x, y)).unwrap() + steps);
  }
}

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");

  let lines: Vec<&str> = input.lines().collect();
  let first: &str = lines[0];
  let second: &str = lines[1];

  // Save visited positions.
  let mut positions: HashMap<(i64, i64), i64> = HashMap::new();
  let mut shortestDist: i64 = std::i64::MAX;
  let mut leastSteps: i64 = std::i64::MAX;
  let mut steps: i64 = 0;

  // Run first cable.
  let mut x: i64 = 0;
  let mut y: i64 = 0;
  for item in first.split(",")
  {
    let value: i64 = item[1..].parse().unwrap();

    for _ in 1..value+1
    {
      steps += 1;
      match &item[0..1]
      {
        "R" => {x += 1;}
        "L" => {x -= 1;}
        "U" => {y += 1;}
        "D" => {y -= 1;}
        _ => panic!("Wrong value {}", &item[0..1]),
      }
      positions.insert((x, y), steps);
    }
  }

  // Run second cable and check for already visited locations.
  x = 0; y = 0; steps = 0;
  for item in second.split(",")
  {
    let value: i64 = item[1..].parse().unwrap();

    for _ in 1..value+1
    {
      steps += 1;
      match &item[0..1]
      {
        "R" => {x += 1;}
        "L" => {x -= 1;}
        "U" => {y += 1;}
        "D" => {y -= 1;}
        _ => panic!("Wrong value {}", &item[0..1]),
      }
      checkPos(x, y, &positions, &mut shortestDist, steps, &mut leastSteps);
    }
  }
  println!("Shortest {}", shortestDist);
  println!("Shortest {}", leastSteps);
}
