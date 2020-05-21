#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashMap;

fn check(number: i64) -> (bool, bool)
{
  let digits: Vec<u32> = number.to_string().chars().map(|x| x.to_digit(10).unwrap()).collect();
  let mut same2: bool = false;
  let mut sameValues: HashMap<u32, i64> = HashMap::new();
  for i in 0..digits.len()-1
  {
    if (digits[i] == digits[i+1])
    {
      same2 = true;

      let counter = sameValues.entry(digits[i]).or_insert(0);
      *counter += 1;
    }
    if (digits[i] > digits[i+1])
    {
      return (false, false);
    }
  }

  let mut same2ex: bool = false;
  for (_, value) in sameValues.iter()
  {
    if (*value == 1)
    {
      same2ex = true;
    }
  }

  return (same2, same2ex)
}

fn main() {
  let startNumber: i64 = 125730;
  let endNumber: i64 = 579381;

  let mut counter: i64 = 0;
  let mut counterEx: i64 = 0;
  for number in startNumber..endNumber+1
  {
    let result = check(number);
    if (result.0) {counter += 1;}
    if (result.1) {counterEx += 1;}
  }
  println!("Count: {}, {}", counter, counterEx);
}
