#![allow(non_snake_case)]
#![allow(unused_parens)]

struct Computer
{
  index: usize,
  values: std::collections::HashMap<usize, i64>,
  input: Vec<i64>,
  output: Vec<i64>,
  relativeBase: i64,
}

impl Computer
{
  fn new(inValues: &Vec<i64>) -> Computer
  {
    let mut newValues: std::collections::HashMap<usize, i64> = std::collections::HashMap::new();
    for (i, value) in inValues.iter().enumerate()
    {
      newValues.insert(i, *value);
    }

    return Computer {
      index: 0,
      values: newValues,
      input: Vec::new(),
      output: Vec::new(),
      relativeBase: 0,
    };
  }

  fn getValue(&mut self, offset: usize, paramMode: &Vec<u32>, isTarget: bool) -> i64
  {
    if ((paramMode.len() >= offset+1) && paramMode[offset] == 1)
    {
      return *self.values.entry( self.index+offset+1 ).or_insert(0);
    }
    else if ((paramMode.len() >= offset+1) && paramMode[offset] == 2)
    {
      let target: i64 = (*self.values.entry(self.index+offset+1).or_insert(0) + self.relativeBase);
      return if (isTarget) {target} else {*self.values.entry(target as usize).or_insert(0)};
    }
    else
    {
      let target: i64 = *self.values.entry(self.index+offset+1).or_insert(0);
      return if (isTarget) {target} else {*self.values.entry(target as usize).or_insert(0)};
    }
  }

  fn add(&mut self, paramMode: &Vec<u32>)
  {
    //let target: usize = self.values[&(self.index+3)] as usize;
    let target: usize = self.getValue(2, paramMode, true) as usize;
    let first = self.getValue(0, paramMode, false);
    let second = self.getValue(1, paramMode, false);
    
    self.values.insert(target, first + second);
    self.index += 4;
  }

  fn mult(&mut self, paramMode: &Vec<u32>)
  {
    //let target: usize = self.values[&(self.index+3)] as usize;
    let target: usize = self.getValue(2, paramMode, true) as usize;
    let first = self.getValue(0, paramMode, false);
    let second = self.getValue(1, paramMode, false);
    
    self.values.insert(target, first * second);
    self.index += 4;
  }

  fn input(&mut self, inValue: i64, paramMode: &Vec<u32>)
  {
    //let target: usize = self.values[&(self.index+3)] as usize;
    let target: usize = self.getValue(0, paramMode, true) as usize;
    self.values.insert(target, inValue);
    self.index += 2;
  }

  fn output(&mut self, paramMode: &Vec<u32>) -> i64
  {
    let first = self.getValue(0, paramMode, false);
    self.index += 2;
    return first;
  }

  fn jumpIfTrue(&mut self, paramMode: &Vec<u32>, ifTrue: bool)
  {
    let first = self.getValue(0, paramMode, false);
    let second = self.getValue(1, paramMode, false);
    if (ifTrue)
    {
      if (first != 0)
      {
        self.index = second as usize;
        return;
      }
    }
    else
    {
      if (first == 0)
      {
        self.index = second as usize;
        return;
      }
    }
    self.index += 3;
  }

  fn lessThan(&mut self, paramMode: &Vec<u32>)
  {
    //let target: usize = self.values[&(self.index+3)] as usize;
    let target: usize = self.getValue(2, paramMode, true) as usize;
    let first = self.getValue(0, paramMode, false);
    let second = self.getValue(1, paramMode, false);

    self.values.insert(target, if (first < second) {1} else {0});
    self.index += 4;
  }

  fn equals(&mut self, paramMode: &Vec<u32>)
  {
    //let target: usize = self.values[&(self.index+3)] as usize;
    let target: usize = self.getValue(2, paramMode, true) as usize;
    let first = self.getValue(0, paramMode, false);
    let second = self.getValue(1, paramMode, false);

    self.values.insert(target, if (first == second) {1} else {0});
    self.index += 4;
  }

  fn updateRelativeBase(&mut self, paramMode: &Vec<u32>)
  {
    let first = self.getValue(0, paramMode, false);
    self.relativeBase += first;
    self.index += 2;
  }


  fn run(&mut self) -> bool
  {
    loop
    {
      let value: i64 = self.values[&self.index];
      let opCode: i64 = value % 100;
      let mut paramMode: Vec<u32> = (value / 100).to_string().chars().map(|x| x.to_digit(10).unwrap()).collect();
      paramMode.reverse();
      match opCode
      {
        1 => self.add(&paramMode),
        2 => self.mult(&paramMode),
        3 => {
          if (self.input.len() == 0)
          {
            return false; // Wait for more input.
          }
          let inputValue: i64 = self.input.remove(0);
          self.input(inputValue, &paramMode);
        }
        4 => {
          let result = self.output(&paramMode);
          self.output.push(result);
        }
        5 => self.jumpIfTrue(&paramMode, true),
        6 => self.jumpIfTrue(&paramMode, false),
        7 => self.lessThan(&paramMode),
        8 => self.equals(&paramMode),
        9 => self.updateRelativeBase(&paramMode),
        99 => {
          return true;
        }
        _ => panic!("Error! {}", opCode),
      };
    }
  }
}

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  let valuesStr: Vec<&str> = input.split(",").collect();
  let values: Vec<i64> = valuesStr.iter().map(|x| x.trim().parse::<i64>().unwrap()).collect();

  // First part:
  {
    let mut comp = Computer::new(&values);
    let mut panels: std::collections::HashMap<(i64, i64), i64> = std::collections::HashMap::new();
    let mut x: i64 = 0;
    let mut y: i64 = 0;
    let mut direction: i64 = 0;
    loop
    {
      if (!panels.contains_key(&(x, y)) || panels.get(&(x, y)).unwrap() == &0)
      {
        comp.input.push(0);
      }
      else
      {
        comp.input.push(1);
      }
  
      let result = comp.run();
      if (result)
      {
        break;
      }
      
      let colorWrite: i64 = *comp.output.get(comp.output.len() - 2).unwrap();
      panels.insert((x, y), colorWrite);
      let rotate: i64 = *comp.output.get(comp.output.len() - 1).unwrap();
      if (rotate == 0)
      {
        direction = (direction - 1).rem_euclid(4);
      }
      else
      {
        direction = (direction + 1).rem_euclid(4);
      }
  
      match direction
      {
        0 => y -= 1,
        1 => x += 1,
        2 => y += 1,
        3 => x -= 1,
        _ => panic!("Wrong direction!"),
      }
    }
    println!("Panels {}", panels.len());
  }


  // Second part:
  {
    let mut comp = Computer::new(&values);
    let mut panels: std::collections::HashMap<(i64, i64), i64> = std::collections::HashMap::new();
    let mut x: i64 = 0;
    let mut y: i64 = 0;
    let mut minMax: [i64; 4] = [0,0,0,0];
    let mut direction: i64 = 0;
    panels.insert((x, y), 1);
    loop
    {
      if (!panels.contains_key(&(x, y)) || panels.get(&(x, y)).unwrap() == &0)
      {
        comp.input.push(0);
      }
      else
      {
        comp.input.push(1);
      }
  
      let result = comp.run();
      if (result)
      {
        break;
      }
      
      let colorWrite: i64 = *comp.output.get(comp.output.len() - 2).unwrap();
      panels.insert((x, y), colorWrite);
      minMax[0] = std::cmp::min(minMax[0], x);
      minMax[1] = std::cmp::min(minMax[1], y);
      minMax[2] = std::cmp::max(minMax[2], x);
      minMax[3] = std::cmp::max(minMax[3], y);

      let rotate: i64 = *comp.output.get(comp.output.len() - 1).unwrap();
      if (rotate == 0)
      {
        direction = (direction - 1).rem_euclid(4);
      }
      else
      {
        direction = (direction + 1).rem_euclid(4);
      }
  
      match direction
      {
        0 => y -= 1,
        1 => x += 1,
        2 => y += 1,
        3 => x -= 1,
        _ => panic!("Wrong direction!"),
      }
    }
    println!("Panels {}", panels.len());
    // Print what was drawn.
    println!("MinMax {:?}", minMax);
    for yp in minMax[1]..minMax[3]+1
    {
      for xp in minMax[0]..minMax[2]+1
      {
        if (!panels.contains_key(&(xp, yp)) || panels.get(&(xp, yp)).unwrap() == &0)
        {
          print!(".");
        }
        else
        {
          print!("#");
        }
      }
      println!("");
    }
  }
} 