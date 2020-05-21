#![allow(non_snake_case)]
#![allow(unused_parens)]

use mod_exp::mod_exp;

fn newStack(cards: &mut Vec<i64>)
{
  cards.reverse();
}

fn cutCards(cards: &mut Vec<i64>, cut: i64)
{
  if (cut >= 0)
  {
    cards.rotate_left(cut as usize);
  }
  else
  {
    cards.rotate_right((cut * -1) as usize);
  }
}

fn dealInc(cards: &mut Vec<i64>, inc: i64)
{
  let mut newCards: Vec<i64> = Vec::new();
  newCards.resize(cards.len(), 0);
  let mut index: i64 = 0;
  for i in 0..cards.len()
  {
    newCards[index as usize] = cards[i];
    index = (index + inc) % cards.len() as i64;
  }
  for i in 0..cards.len()
  {
    cards[i] = newCards[i];
  }
}

fn main()
{
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");

  // First part:
  let mut cards: Vec<i64> = Vec::new();
  let nCards: usize = 10007;
  cards.reserve_exact(nCards);
  for i in 0..nCards
  {
    cards.push(i as i64);
  }
  
  for line in input.lines()
  {
    let lineSplit: Vec<&str> = line.split(" ").collect();

    if (line.contains("deal with increment"))
    {
      let inc: i64 = lineSplit[lineSplit.len() - 1].parse::<i64>().unwrap();
      dealInc(&mut cards, inc);
    }
    else if (line.contains("deal into new stack"))
    {
      newStack(&mut cards);
    }
    else if (line.contains("cut"))
    {
      let cut: i64 = lineSplit[lineSplit.len() - 1].parse::<i64>().unwrap();
      cutCards(&mut cards, cut);
    }
    else
    {
      panic!("{}", line);
    }
  }

  //println!("{:?}", cards);
  for i in 0..cards.len()
  {
    if (cards[i] == 2019)
    {
      println!("{}", i);
      break;
    }
  }

  // Second part:
  let mut pos: i128 = 2020;
  let nCards: i128 = 119315717514047;
  let iterations: i128 = 101741582076661;
  let mut inc: i128 = 0;
  let mut multi: i128 = 1;
  for line in input.lines().rev()
  {
    let lineSplit: Vec<&str> = line.split(" ").collect();

    // Simulate one run and mark increment and multiplication of index. Based on solution from net.
    // https://gitlab.com/bwearley/advent-of-code-2019/-/blob/master/day22_rust/src/main.rs
    // Convert the whole process to a linear equation: ax + b
    if (line.contains("deal with increment"))
    {
      let increment: i128 = lineSplit[lineSplit.len() - 1].parse::<i128>().unwrap();
      let n = mod_exp(increment, nCards-2, nCards);
      multi *= n;
      inc *= n;
    }
    else if (line.contains("deal into new stack"))
    {
      multi *= -1;
      inc = -inc - 1;
    }
    else if (line.contains("cut"))
    {
      let cut: i128 = lineSplit[lineSplit.len() - 1].parse::<i128>().unwrap();
      inc += cut;
    }
    else
    {
      panic!("{}", line);
    }

    multi = multi % nCards;
    inc = inc % nCards;
  }

  // Applying the function n times simplifies to:
  // x * a^n + b * (a^n - 1) / (a-1)
  let term1 = pos * mod_exp(multi, iterations, nCards) % nCards;
  let tmp = (mod_exp(multi, iterations, nCards) - 1) * mod_exp(multi-1, nCards-2, nCards) % nCards;
  let term2 = inc * tmp % nCards;
  pos = (term1 + term2) % nCards;

  println!("Value: {}", pos);
}
