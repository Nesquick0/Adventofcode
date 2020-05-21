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

fn drawMaze(maze: &std::collections::HashMap<(i64, i64), i64>, pos: &[i64; 2])
{
  let (mut minX, mut minY, mut maxX, mut maxY): (i64, i64, i64, i64) = (0, 0, 0, 0);
  for (pos, _) in maze
  {
    minX = std::cmp::min(minX, pos.0);
    minY = std::cmp::min(minY, pos.1);
    maxX = std::cmp::max(maxX, pos.0);
    maxY = std::cmp::max(maxY, pos.1);
  }

  println!("==========================================");
  for y in minY..maxY+1
  {
    for x in minX..maxX+1
    {
      if (x == pos[0] && y == pos[1])
      {
        print!("D");
        continue;
      }

      let value: &i64 = maze.get(&(x, y)).unwrap_or(&-1);
      match value
      {
        0 => print!("."),
        1 => print!("#"),
        2 => print!("o"),
        _ => print!(" "),
      }
    }
    println!("");
  }
  println!("==========================================");
}

fn getPos(x: i64, y: i64, dir: i64) -> (i64, i64)
{
  match dir
  {
    1 => return (x, y-1),
    2 => return (x, y+1),
    3 => return (x+1, y),
    4 => return (x-1, y),
    _ => panic!("Wrong direction!"),
  }
}

fn findNearest(maze: &std::collections::HashMap<(i64, i64), i64>, startX: i64, startY: i64, targetType: i64) -> (Vec<i64>, usize)
{
  let mut visited: std::collections::HashSet<(i64, i64)> = std::collections::HashSet::new(); 
  let mut queue: std::collections::VecDeque<(i64, i64, Vec<i64>)> = std::collections::VecDeque::new(); 
  queue.push_back((startX, startY, Vec::new()));
  visited.insert((startX, startY));
  let mut longestPath: usize = 0;

  while (queue.len() > 0)
  {
    let (x, y, path) = queue.pop_front().unwrap();
    if (path.len() > longestPath)
    {
      longestPath = path.len();
    }

    if (maze.get(&(x, y)).unwrap_or(&-1) == &targetType)
    {
      return (path, longestPath);
    }

    for dir in 1..5
    {
      let newPos = getPos(x, y, dir);
      if (!visited.contains(&newPos))
      {
        visited.insert(newPos);
        if (maze.get(&newPos).unwrap_or(&-1) == &1)
        {
          continue;
        }
        let mut newPath: Vec<i64> = path.clone();
        newPath.push(dir);
        queue.push_back((newPos.0, newPos.1, newPath));
      }
    }
  }

  return (Vec::new(), longestPath);
}

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  let valuesStr: Vec<&str> = input.split(",").collect();
  let values: Vec<i64> = valuesStr.iter().map(|x| x.trim().parse::<i64>().unwrap()).collect();

  // First part:
  let mut maze: std::collections::HashMap<(i64, i64), i64> = std::collections::HashMap::new();
  // Maze info: 0 free, 1 wall, 2 oxygen, -1 unknown.
  maze.insert((0, 0), 0);
  let mut pos: [i64; 2] = [0, 0];

  let mut comp = Computer::new(&values);

  loop
  {
    //let dir: i64 = rand::thread_rng().gen_range(1, 5);
    // Find nearest free position and go there.
    let path: Vec<i64> = findNearest(&maze, pos[0], pos[1], -1).0;
    if (path.len() <= 0)
    {
      break;
    }
    let dir = path[0];
    comp.input.push(dir);
    comp.run();

    let result: i64 = comp.output[0];
    comp.output.clear();
    if (result == 0)
    {
      // Hit wall. No position change.
      maze.insert(getPos(pos[0], pos[1], dir), 1);
    }
    else if (result == 1)
    {
      // Free space. Moved.
      let newPos = getPos(pos[0], pos[1], dir);
      maze.insert(newPos, 0);
      pos[0] = newPos.0;
      pos[1] = newPos.1;
    }
    else if (result == 2)
    {
      // Find oxygen system.
      let newPos = getPos(pos[0], pos[1], dir);
      maze.insert(newPos, 2);
      pos[0] = newPos.0;
      pos[1] = newPos.1;
      //break;
    }

    //drawMaze(&maze, &pos);
  }
  drawMaze(&maze, &[0, 0]);

  // Find shortest path from start to oxygen.
  let path: Vec<i64> = findNearest(&maze, 0, 0, 2).0;
  println!("Path len {}", path.len());

  // Second part:
  // Get oxygen position.
  let mut oxygenPos: (i64, i64) = (0, 0);
  for (pos, value) in &maze
  {
    if (*value == 2)
    {
      oxygenPos = *pos;
    }
  }
  let longestPath: usize = findNearest(&maze, oxygenPos.0, oxygenPos.1, 99).1;
  println!("Longest path {}", longestPath);
}