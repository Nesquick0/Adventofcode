#![allow(non_snake_case)]
#![allow(unused_parens)]

struct Computer
{
  index: usize,
  values: std::collections::HashMap<usize, i64>,
  input: Vec<i64>,
  output: Vec<i64>,
  relativeBase: i64,
  tiles: std::collections::HashMap<(i64, i64), i64>,
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
      tiles: std::collections::HashMap::new(),
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

  fn printState(&self)
  {
    let mut maxX: i64 = 0;
    let mut maxY: i64 = 0;
    for (x, y) in self.tiles.keys()
    {
      maxX = std::cmp::max(maxX, *x);
      maxY = std::cmp::max(maxY, *y);
    }

    for y in 0..maxY+1
    {
      for x in 0..maxX+1
      {
        let tile: i64 = *self.tiles.get(&(x, y)).unwrap();
        match tile
        {
          0 => print!(" "),
          1 => print!("#"),
          2 => print!("B"),
          3 => print!("="),
          4 => print!("o"),
          _ => print!(" "),
        }
      }
      println!("")
    }
  }

  fn countBlocks(&self) -> i64
  {
    let mut blocks: i64 = 0;
    for t in &self.tiles
    {
      if (*t.1 == 2)
      {
        blocks += 1;
      }
    }
    return blocks;
  }

  fn getDir(&self) -> i64
  {
    // Find ball and paddle x pos.
    let mut ballX = 0;
    let mut paddleX = 0;
    for t in &self.tiles
    {
      if (*t.1 == 3)
      {
        paddleX = (t.0).0;
      }
      if (*t.1 == 4)
      {
        ballX = (t.0).0;
      }
    }
    if (ballX > paddleX) {return 1;}
    else if (ballX < paddleX) {return -1;}
    return 0;
  }
}

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  let valuesStr: Vec<&str> = input.split(",").collect();
  let values: Vec<i64> = valuesStr.iter().map(|x| x.trim().parse::<i64>().unwrap()).collect();

  // First part:
  {
    let mut comp = Computer::new(&values);
    let mut blocks: i64 = 0;

    comp.run();
    for s in comp.output.chunks(3)
    {
      let t = s[2];
      if (t == 2)
      {
        blocks += 1;
      }
    }
    println!("Blocks {}", blocks);
  }

  // Second part:
  {
    let mut comp = Computer::new(&values);
    comp.values.insert(0, 2);
    loop
    {
      comp.run();
      for s in comp.output.chunks(3)
      {
        let x = s[0];
        let y = s[1];
        let t = s[2];
        comp.tiles.insert((x, y), t);
      }
      comp.input.push(comp.getDir());
      if (comp.countBlocks() == 0)
      {
        break;
      }
    }
    comp.printState();
    println!("Score {}, blocks {}", comp.tiles.get(&(-1, 0)).unwrap(), comp.countBlocks());
  }
} 