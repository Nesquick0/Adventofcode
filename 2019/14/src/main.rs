#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashMap;
use std::cell::Cell;

struct Rule
{
  nResult: i64,
  needed: Vec<(String, i64)>,
}

impl Rule
{
  fn new() -> Rule
  {
    return Rule {
      nResult: 0,
      needed: Vec::new(),
    }
  }
}

fn run(chemicals: &HashMap<String, Cell<i64>>, rules: &HashMap<String, Rule>)
{
  loop
  {
    let mut found = false;
    let mut useChem: &String = &"".to_string();
    {
      for (chem, count) in chemicals.iter()
      {
        if (count.get() > 0 && chem != "ORE")
        {
          found = true;
          useChem = chem;
          break;
        }
      }
      if (found == false)
      {
        break;
      }
    }

    let count: i64;
    let resultChems: &Cell<i64> = chemicals.get(useChem).unwrap();
    if (resultChems.get() % rules.get(useChem).unwrap().nResult > 0)
    {
      count = (resultChems.get() / rules.get(useChem).unwrap().nResult) + 1;
      resultChems.set((resultChems.get() % rules.get(useChem).unwrap().nResult) - rules.get(useChem).unwrap().nResult);
    }
    else
    {
      count = resultChems.get() / rules.get(useChem).unwrap().nResult;
      resultChems.set(0);
    }
    for (need, countNeed) in &rules.get(useChem).unwrap().needed
    {
      chemicals.get(need).unwrap().set(chemicals.get(need).unwrap().get() + (*countNeed * count));
    }
  }
}

fn reset(chemicals: &HashMap<String, Cell<i64>>)
{
  for (_, count) in chemicals.iter()
  {
    count.set(0);
  }
}

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");

  let mut chemicals: HashMap<String, Cell<i64>> = HashMap::new();
  let mut rules: HashMap<String, Rule> = HashMap::new();

  for line in input.lines()
  {
    let lineSplit: Vec<&str> = line.split(" => ").collect();
    let result: Vec<&str> = lineSplit[1].split(" ").collect();
    let mut rule = Rule::new();
    rule.nResult = result[0].parse::<i64>().unwrap();
    chemicals.insert(result[1].to_string(), Cell::new(0));

    for need in lineSplit[0].split(", ")
    {
      let needChem: Vec<&str> = need.split(" ").collect();
      rule.needed.push((needChem[1].to_string(), needChem[0].parse::<i64>().unwrap()));
      chemicals.insert(needChem[1].to_string(), Cell::new(0));
    }
    rules.insert(result[1].to_string(), rule);
  }
  chemicals.get("FUEL").unwrap().set(1);

  // First part:
  run(&chemicals, &rules);
  println!("Ores: {}", chemicals.get("ORE").unwrap().get());

  // Second part:
  let mut low = 1000000000000 / chemicals.get("ORE").unwrap().get();
  let mut high = 2 * low;
  while (high - low > 1)
  {
    reset(&chemicals);
    let middle: i64 = low + ((high - low) / 2);
    println!("h {} m {} l {}", high, middle, low);
    chemicals.get("FUEL").unwrap().set(middle);
    run(&chemicals, &rules);
    if (chemicals.get("ORE").unwrap().get() > 1000000000000)
    {
      high = middle;
    }
    else
    {
      low = middle;
    }
  }
  println!("TotalFuel: {}", low);
}
