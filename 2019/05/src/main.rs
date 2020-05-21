#![allow(non_snake_case)]
#![allow(unused_parens)]

fn add(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> usize
{
  let target: usize = values[i+3] as usize;
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};
  
  values[target] = first + second;
  return i+4;
}

fn mult(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> usize
{
  let target: usize = values[i+3] as usize;
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};
  
  values[target] = first * second;
  return i+4;
}

fn input(values: &mut Vec<i64>, i: usize, inValue: i64) -> usize
{
  let target: usize = values[i+1] as usize;
  values[target] = inValue;
  return i+2;
}

fn output(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> (usize, i64)
{
  if (paramMode.len() >= 1 && paramMode[0] == 1)
  {
    return (i+2, values[i+1]);  
  }
  else
  {
    let target: usize = values[i+1] as usize;
    return (i+2, values[target]);
  }
}

fn jumpIfTrue(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>, ifTrue: bool) -> usize
{
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};
  if (ifTrue)
  {
    if (first != 0)
    {
      return second as usize;
    }
  }
  else
  {
    if (first == 0)
    {
      return second as usize;
    }
  }
  return i+3;
}

fn lessThan(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> usize
{
  let target: usize = values[i+3] as usize;
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};

  values[target] = if (first < second) {1} else {0};
  
  return i+4;
}

fn equals(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> usize
{
  let target: usize = values[i+3] as usize;
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};

  values[target] = if (first == second) {1} else {0};
  
  return i+4;
}

fn runProgram(values: &mut Vec<i64>, inValue: i64) -> i64
{
  let mut i: usize = 0;
  loop
  {
    let value: i64 = values[i];
    let opCode: i64 = value % 100;
    let mut paramMode: Vec<u32> = (value / 100).to_string().chars().map(|x| x.to_digit(10).unwrap()).collect();
    paramMode.reverse();
    match opCode
    {
      1 => i = add(values, i, &paramMode),
      2 => i = mult(values, i, &paramMode),
      3 => i = input(values, i, inValue),
      4 => {
        let result = output(values, i, &paramMode);
        println!("Output: {}, Before: {:?}, index: {}", result.1, &values[i-4..i], i);
        i = result.0;
      }
      5 => i = jumpIfTrue(values, i, &paramMode, true),
      6 => i = jumpIfTrue(values, i, &paramMode, false),
      7 => i = lessThan(values, i, &paramMode),
      8 => i = equals(values, i, &paramMode),
      99 => {
        println!("Finished, index: {}", i);
        break;
      }
      _ => println!("Error! {}", opCode),
    };
  }
  return values[0];
}

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  let valuesStr: Vec<&str> = input.split(",").collect();
  let values: Vec<i64> = valuesStr.iter().map(|x| x.trim().parse::<i64>().unwrap()).collect();

  // First part:
  let mut values1 = values.clone();
  let inputValue = 1;
  println!("Result {}", runProgram(&mut values1, inputValue));

  // Second part:
  let mut values2 = values.clone();
  let inputValue = 5;
  println!("Result {}", runProgram(&mut values2, inputValue));
}
