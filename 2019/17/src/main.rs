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

  fn inputFunc(&mut self, inValue: i64, paramMode: &Vec<u32>)
  {
    //let target: usize = self.values[&(self.index+3)] as usize;
    let target: usize = self.getValue(0, paramMode, true) as usize;
    self.values.insert(target, inValue);
    self.index += 2;
  }

  fn outputFunc(&mut self, paramMode: &Vec<u32>) -> i64
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
          self.inputFunc(inputValue, &paramMode);
        }
        4 => {
          let result = self.outputFunc(&paramMode);
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

fn printOutput(output: &Vec<i64>)
{
  for i in 0..output.len()
  {
    if (output[i] == 10)
    {
      println!("");
    }
    else
    {
      print!("{}", output[i] as u8 as char);
    }
  }
}

fn getPos(x: i64, y: i64, dir: i64) -> (i64, i64)
{
  match dir
  {
    0 => return (x, y - 1),
    1 => return (x + 1, y),
    2 => return (x, y + 1),
    3 => return (x - 1, y),
    _ => panic!("Wrong direction."),
  }
}

fn isWall(x: i64, y: i64, world: &Vec<i64>, width: usize, height: usize) -> bool
{
  return (x >= 0 && x < width as i64 && y >= 0 && y < height as i64 && world[(x + y*width as i64) as usize] == 1);
}

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  let valuesStr: Vec<&str> = input.split(",").collect();
  let values: Vec<i64> = valuesStr.iter().map(|x| x.trim().parse::<i64>().unwrap()).collect();

  // First part:
  let mut comp = Computer::new(&values);
  comp.run();
  printOutput(&comp.output);

  // Convert output to array.
  let mut world: Vec<i64> = Vec::new();
  let mut botDir: i64 = -1;
  let mut width = 0;
  for i in 0..comp.output.len()
  {
    match comp.output[i]
    {
      10 => if (width == 0) {width = i;},
      46 => world.push(0), // Empty
      35 => world.push(1), // Wall
      60 => {botDir = 3; world.push(2)}, // <
      62 => {botDir = 1; world.push(2)}, // >
      94 => {botDir = 0; world.push(2)}, // ^
      118 => {botDir = 2; world.push(2)}, // v
      _ => panic!("Unknown pos."), // Robot on wall.
    }
  }
  let height = world.len() / width;

  // Find all intersections.
  let mut calibSum: i64 = 0;
  for i in width..(world.len()-width)
  {
    let x: usize = i % width;
    let y: usize = i / width;

    if (world[i] == 1 && y > 0 && y < width-1)
    {
      if (world[i - width] == 1 && world[i + width] == 1 && world[i - 1] == 1 && world[i + 1] == 1)
      {
        calibSum += (x*y) as i64;
      }
    }
  }

  println!("Calibration: {}", calibSum);

  // Second part:
  // Find start.
  let mut botX: i64 = 0;
  let mut botY: i64 = 0;
  for i in 0..world.len()
  {
    if (world[i] == 2)
    {
      botX = (i % width) as i64;
      botY = (i / width) as i64;
    }
  }
  // Find path through points.
  let mut path: Vec<String> = Vec::new();
  loop
  {
    let (x, y): (i64, i64) = getPos(botX, botY, botDir);

    // If inside and wall go forward.
    if (isWall(x, y, &world, width, height))
    {
      if (path.len() > 0)
      {
        let lastString: &String = path.last().unwrap();
        let numberPossible = lastString.parse::<i64>();
        if (!numberPossible.is_err())
        {
          let number: i64 = numberPossible.unwrap();
          path.pop();
          path.push((number+1).to_string());
        }
        else
        {
          path.push("1".to_string());
        }
      }
      else
      {
        path.push("1".to_string());
      }

      botX = x;
      botY = y;
    }
    // Find turn.
    else
    {
      // Check left
      let newDir = (botDir - 1).rem_euclid(4);
      let (x, y): (i64, i64) = getPos(botX, botY, newDir);
      if (isWall(x, y, &world, width, height))
      {
        path.push("L".to_string());
        botDir = newDir;
        continue;
      }

      // Check right
      let newDir = (botDir + 1).rem_euclid(4);
      let (x, y): (i64, i64) = getPos(botX, botY, newDir);
      if (isWall(x, y, &world, width, height))
      {
        path.push("R".to_string());
        botDir = newDir;
        continue;
      }

      break;
    }
  }
  println!("Path {:?}", &path);

  let mut comp = Computer::new(&values);
  comp.values.insert(0, 2);

  // Manual path added:
  // Main routine - A, B, A, C, A, C, B, C, C, B
  comp.input.extend("A,B,A,C,A,C,B,C,C,B\n".as_bytes().iter().map(|x| *x as i64).collect::<Vec<i64>>());
  // A - "L", "4", "L", "4", "L", "10", "R", "4"
  comp.input.extend("L,4,L,4,L,10,R,4\n".as_bytes().iter().map(|x| *x as i64).collect::<Vec<i64>>());
  // B - "R", "4", "L", "4", "L", "4", "R", "8", "R", "10"
  comp.input.extend("R,4,L,4,L,4,R,8,R,10\n".as_bytes().iter().map(|x| *x as i64).collect::<Vec<i64>>());
  // C - "R", "4", "L", "10", "R", "10"
  comp.input.extend("R,4,L,10,R,10\n".as_bytes().iter().map(|x| *x as i64).collect::<Vec<i64>>());
  // Feed?
  comp.input.extend("n\n".as_bytes().iter().map(|x| *x as i64).collect::<Vec<i64>>());

  // Run.
  comp.run();
  printOutput(&comp.output);
  println!("Dust: {}", comp.output.last().unwrap());
}