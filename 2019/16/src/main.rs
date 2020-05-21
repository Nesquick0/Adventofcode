#![allow(non_snake_case)]
#![allow(unused_parens)]

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  let digits: Vec<u32> = input.trim().chars().map(|x| x.to_digit(10).unwrap()).collect();

  let phases = 100;
  let pattern: [i64; 4] = [0, 1, 0, -1];

  // First part:
  let mut number: Vec<u32> = digits.clone();
  
  for _ in 0..phases
  {
    let mut newNumber: Vec<u32> = Vec::new();

    for i in 0..number.len()
    {
      let mut value: i64 = 0;
      
      for j in 0..number.len()
      {
        let patternIdx = ((j + 1) / (i + 1)) % pattern.len();
        value += (number[j] as i64) * pattern[patternIdx];
      }

      newNumber.push((i64::abs(value) % 10) as u32);
    }
    number = newNumber;
  }
  let nStr: String = number[0..8].iter().map(|x| x.to_string()).collect::<String>();
  println!("Result1 {}", nStr);

  // Second part:
  let offset: u32 = digits[0..7].iter().map(|x| x.to_string()).collect::<String>().parse::<u32>().unwrap();
  println!("\nOffset: {}", offset);
  let mut number2: Vec<u32> = Vec::new();
  number2.reserve_exact((digits.len() * 10000) - offset as usize);
  for i in (offset as usize)..((digits.len() * 10000) as usize)
  {
    number2.push(digits[i % digits.len()]);
  }

  for _ in 0..phases
  {
    let mut newNumber: Vec<u32> = Vec::new();
    newNumber.resize(number2.len(), 0);

    let mut lastValue: u32 = 0;
    for i in (0..number2.len()).rev()
    {
      //let value: u32 = number2[i..].iter().sum();
      lastValue += number2[i];
      newNumber[i] = (lastValue % 10);
    }
    number2 = newNumber;
  }
  let nStr: String = number2[0..8].iter().map(|x| x.to_string()).collect::<String>();
  println!("Result2 {}", nStr);
} 