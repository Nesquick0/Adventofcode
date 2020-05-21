#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::io::Read;

fn readToString(filename: &str) -> std::io::Result<String>
{
  let mut file = std::fs::File::open(&filename)?;
  let mut text = String::new();
  file.read_to_string(&mut text)?;
  Ok(text)
}

fn runProgram(mut values: Vec<i64>) -> i64
{
  let mut i: usize = 0;
  loop
  {
    let opCode: i64 = values[i];
    match opCode
    {
      1 => {
        let target = values[i+3] as usize;
        values[target] = values[values[i+1] as usize] + values[values[i+2] as usize]
      },
      2 => {
        let target = values[i+3] as usize;
        values[target] = values[values[i+1] as usize] * values[values[i+2] as usize]
      },
      99 => break,
      _ => println!("Error! {}", opCode),
    };
    i += 4;
  }
  return values[0];
}

fn runSecondProgram(values: &Vec<i64>) -> (i64, i64)
{
  for noun in 0..99
  {
    for verb in 0..99
    {
      let mut values1 = values.clone();
      values1[1] = noun;
      values1[2] = verb;
      let result = runProgram(values1);
      if (result == 19690720)
      {
        return (noun, verb);
      }
    }
  }
  return (0, 0);
}

fn main() {
  let text: String = readToString("input.txt").expect("Bad file!");
  let valuesStr: Vec<&str> = text.split(",").collect();
  let values: Vec<i64> = valuesStr.iter().map(|x| x.parse::<i64>().unwrap()).collect();

  // First part:
  let mut values1 = values.clone();
  values1[1] = 12;
  values1[2] = 2;
  println!("Result {}", runProgram(values1));

  // Second part:
  let result: (i64, i64) = runSecondProgram(&values);
  println!("Result2 noun {}, verb {}", result.0, result.1);
  println!("Result2 {}", 100 * result.0 + result.1);
}
