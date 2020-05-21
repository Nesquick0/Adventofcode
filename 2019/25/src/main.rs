#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::io;
use std::io::Write;
use std::collections::HashMap;
use std::collections::VecDeque;
use regex::Regex;
use itertools::Itertools;
//extern crate pancurses;
//use pancurses::{initscr, endwin};

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
    print!("{}", output[i] as u8 as char);
  }
}

#[derive(PartialEq,PartialOrd,Debug,Clone)]
enum Direction {
  Left = 0,
  Up,
  Right,
  Down,
}

impl Direction {
  fn _as_str(&self) -> &'static str
  {
    match *self // *self has type Direction
    {
        Direction::Left => "east",
        Direction::Up => "north",
        Direction::Right => "west",
        Direction::Down => "south",
    }
  }

  fn fromStr(from: &str) -> Direction
  {
    match from
    {
      "east" => return Direction::Left,
      "north" => return Direction::Up,
      "west" => return Direction::Right,
      "south" => return Direction::Down,
      _ => panic!("Wrong direction: {}", from),
    }
  }
}

struct Place
{
  x: i64,
  y: i64,
  dirs: Vec<Direction>,
}

impl Place
{
  fn new() -> Place
  {
    return Place{
      x: 0,
      y: 0,
      dirs: Vec::new(),
    };
  }
}

fn printWorld(world: &HashMap<String, Place>, xp: i64, yp: i64)
{
  // Sizes.
  let mut minX: i64 = 0; let mut maxX: i64 = 0; let mut minY: i64 = 0; let mut maxY: i64 = 0;
  for pos in world
  {
    minX = std::cmp::min(minX, pos.1.x);
    maxX = std::cmp::max(maxX, pos.1.x);
    minY = std::cmp::min(minY, pos.1.y);
    maxY = std::cmp::max(maxY, pos.1.y);
  }
  let width: i64 = (maxX+1-minX)*3;
  let height: i64 = (maxY+1-minY)*3;

  // Format.
  let mut output: Vec<char> = vec![' '; (width * height) as usize];
  /*for y in minY..maxY+1
  {
    for x in minX..maxX+1
    {
      if (world.contains_key(&(x, y)))
      {
        output[((x - minX) * 3 + 1 + ((y - minY) * 3 + 1) * width) as usize] = if (x == xp && y == yp) {'x'} else {'#'};

        let place: &Place = world.get(&(x, y)).unwrap();
        for dir in &place.dirs
        {
          match dir
          {
            Direction::Left  => output[((x - minX) * 3 + 0 + ((y - minY) * 3 + 1) * width) as usize] = '.',
            Direction::Up    => output[((x - minX) * 3 + 1 + ((y - minY) * 3 + 0) * width) as usize] = '.',
            Direction::Right => output[((x - minX) * 3 + 2 + ((y - minY) * 3 + 1) * width) as usize] = '.',
            Direction::Down  => output[((x - minX) * 3 + 1 + ((y - minY) * 3 + 2) * width) as usize] = '.',
          }
        }
      }
    }
  }*/
  for pos in world
  {
    let x = pos.1.x;
    let y = pos.1.y;
    output[((x - minX) * 3 + 1 + ((y - minY) * 3 + 1) * width) as usize] = if (x == xp && y == yp) {'x'} else {'#'};

    for dir in &pos.1.dirs
    {
      match dir
      {
        Direction::Left  => output[((x - minX) * 3 + 0 + ((y - minY) * 3 + 1) * width) as usize] = '.',
        Direction::Up    => output[((x - minX) * 3 + 1 + ((y - minY) * 3 + 0) * width) as usize] = '.',
        Direction::Right => output[((x - minX) * 3 + 2 + ((y - minY) * 3 + 1) * width) as usize] = '.',
        Direction::Down  => output[((x - minX) * 3 + 1 + ((y - minY) * 3 + 2) * width) as usize] = '.',
      }
    }
  }

  // Print.
  println!("==========================================");
  for i in 0..output.len()
  {
    print!("{}", output[i]);
    if (i as i64 % width == width-1)
    {
      println!("");
    }
  }
  println!("==========================================");
}

fn runComp(comp: &mut Computer, world: &mut HashMap<String, Place>, print: bool, x: &mut i64, y: &mut i64, inputPlayer: &mut String) -> Vec<String>
{
  let patternPlace = Regex::new(r"^== (?P<place>.+) ==$").unwrap();
  let patternDirs = Regex::new(r"^- (?P<dir>east|south|west|north)$").unwrap();
  let patternItems = Regex::new(r"^- (?P<item>.+)$").unwrap();
  let patternBack = Regex::new(r"^.*(you are ejected back to the checkpoint\.|You can't go that way\.)$").unwrap();

  // Shortcuts.
  match inputPlayer.as_str()
  {
    "a\n" => *inputPlayer = "east\n".to_string(),
    "w\n" => *inputPlayer = "north\n".to_string(),
    "d\n" => *inputPlayer = "west\n".to_string(),
    "s\n" => *inputPlayer = "south\n".to_string(),
    "" => *inputPlayer = "\n".to_string(),
    _ => (),
  }
  // Convert input to numbers.
  comp.input.extend(inputPlayer.as_bytes().iter().map(|x| *x as i64).collect::<Vec<i64>>());
  inputPlayer.clear();

  // React to input.
  let xl: i64 = *x; let yl: i64 = *y;
  if (comp.input.len() > 0)
  {
    match comp.input[0]
    {
      101 => *x -= 1,
      110 => *y -= 1,
      119 => *x += 1,
      115 => *y += 1,
      _ => (),
    }
  }

  // Run.
  comp.run();

  // Convert output.
  if (print)
  {
    print!("\x1B[2J");
    printOutput(&comp.output);
  }
  let mut output: String = "".to_string();
  for i in 0..comp.output.len()
  {
    output.push(comp.output[i] as u8 as char);
  }
  comp.output.clear();

  // Parse output.
  let mut placeName: String = "".to_string();
  let mut dirs: Vec<Direction> = Vec::new();
  let mut items: Vec<String> = Vec::new();
  for line in output.lines()
  {
    if (patternPlace.is_match(line))
    {
      for m in patternPlace.captures_iter(line)
      {
        placeName = m.name("place").unwrap().as_str().to_string();
      }
    }
    else if (patternDirs.is_match(line))
    {
      for m in patternDirs.captures_iter(line)
      {
        dirs.push(Direction::fromStr(m.name("dir").unwrap().as_str()));
      }
    }
    else if (patternItems.is_match(line))
    {
      for m in patternItems.captures_iter(line)
      {
        items.push(m.name("item").unwrap().as_str().to_string());
      }
    }
    else if (patternBack.is_match(line))
    {
      // Clear.
      dirs.clear();
      items.clear();
      *x = xl; *y = yl;
    }
  }
  if (!world.contains_key(&placeName))
  {
    if (!placeName.is_empty())
    {
      // Special cases, custom position offset.
      if (placeName == "Sick Bay")
      {
        *x = *x + 2;
      }

      let mut newPlace: Place = Place::new();
      newPlace.x = *x;
      newPlace.y = *y;
      newPlace.dirs = dirs.clone();
      world.insert(placeName.clone(), newPlace);
    }
  }
  else
  {
    let oldPlace: &Place = world.get(&placeName).unwrap();
    *x = oldPlace.x;
    *y = oldPlace.y;
  }
  if (print)
  {
    println!("{} - {:?}, {:3}, {:3}, - {:?}", &placeName, &dirs, x, y, &items);
    printWorld(&world, *x, *y);
  }

  return items;
}

fn main()
{
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  let valuesStr: Vec<&str> = input.split(",").collect();
  let values: Vec<i64> = valuesStr.iter().map(|x| x.trim().parse::<i64>().unwrap()).collect();

  // First part:
  let mut comp: Computer = Computer::new(&values);
  let mut world: HashMap<String, Place> = HashMap::new();
  let mut inputPlayer = String::new();
  let mut x: i64 = 0; let mut y: i64 = 0;

  // Prerecorded input:
  let mut prerecordedInput: VecDeque<String> = VecDeque::new();
  prerecordedInput.extend(["a", "d",
    "s", "take cake", "a", /*"take giant electromagnet",*/ "a", /*"take infinite loop",*/ "w", /*"take photons",*/ "s", "d", "d",
    "s", "d", "take mutex", "a", "w", "w",
    "d", "take klein bottle", "s", "a", "take monolith", "s", "take fuel cell", "d", /*"take escape pod",*/ "d", "take astrolabe", "a", "a", "w", "d",
    "d", /*"take molten lava",*/ "a", "w",
    "d", "w", "take tambourine", "s",
    "d", "take dark matter", "d",
    "drop klein bottle", "drop mutex", "drop cake", "drop fuel cell"].iter().map(|x| x.to_string()));

  runComp(&mut comp, &mut world, false, &mut x, &mut y, &mut inputPlayer);

  // Run prerecorded input to collect items.
  while (!prerecordedInput.is_empty())
  {
    inputPlayer = prerecordedInput.pop_front().unwrap() + "\n";
    runComp(&mut comp, &mut world, false, &mut x, &mut y, &mut inputPlayer);
  }

  // Try to go through security checkpoint.
  let items: Vec<String> = runComp(&mut comp, &mut world, false, &mut x, &mut y, &mut "inv\n".to_string());
  println!("{:?}", items);

  let mut itemsComb: Vec<Vec<&String>> = Vec::new();
  for i in 1..items.len()+1
  {
    itemsComb.extend( items.iter().combinations(i) );
  }

  /*// For every item combination.
  for comb in itemsComb
  {
    // Drop every item.
    let mut itemsNow: Vec<String> = runComp(&mut comp, &mut world, false, &mut x, &mut y, &mut "inv\n".to_string());
    for item in itemsNow
    {
      inputPlayer = format!("drop {}\n", item).to_string();
      runComp(&mut comp, &mut world, false, &mut x, &mut y, &mut inputPlayer);
    }

    // Pick items in combination and move.
    for item in &comb
    {
      inputPlayer = format!("take {}\n", item).to_string();
      runComp(&mut comp, &mut world, false, &mut x, &mut y, &mut inputPlayer);
    }
    // Move up.
    let oldY = y;
    runComp(&mut comp, &mut world, false, &mut x, &mut y, &mut "w\n".to_string());
    if (y != oldY)
    {
      println!("{:?}", comb);
      break;
    }
  }*/

  // Print inventory.
  runComp(&mut comp, &mut world, true, &mut x, &mut y, &mut "inv\n".to_string());

  // Player manual input.
  loop
  {
    // Put input.
    print!("Input: ");
    io::stdout().flush().expect("Flush failed!");
    io::stdin().read_line(&mut inputPlayer).expect("Unable to read user input");
    inputPlayer = inputPlayer.replace("\r", "");
    runComp(&mut comp, &mut world, true, &mut x, &mut y, &mut inputPlayer);
  }
}