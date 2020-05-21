#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::io::Read;

fn readToString(filename: &str) -> std::io::Result<String> {
  let mut file = std::fs::File::open(&filename)?;
  let mut text = String::new();
  file.read_to_string(&mut text)?;
  Ok(text)
}


fn getFuel(mass: i64) -> i64
{
  return mass / 3 - 2;
}

fn getFuel2(mut mass: i64) -> i64
{
  let mut totalFuel: i64 = 0;
  while (mass > 0)
  {
    let fuel = getFuel(mass);
    if (fuel <= 0)
    {
      break;
    }
    totalFuel += fuel;
    mass = fuel;
  }
  return totalFuel;
}

fn main()
{
  let text: String = readToString("input.txt").expect("Bad file!");

  let mut sum: i64 = 0;
  for line in text.lines()
  {
    sum += getFuel(line.parse::<i64>().unwrap());
  }
  println!("Sum: {}", sum);

  let mut sum2: i64 = 0;
  for line in text.lines()
  {
    sum2 += getFuel2(line.parse::<i64>().unwrap());
  }
  println!("Sum: {}", sum2);
}
