#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashSet;

fn printWorld(world: &Vec<i64>, size: usize)
{
  for y in 0..size
  {
    for x in 0..size
    {
      match world[x + y*size]
      {
        0 => print!("."),
        1 => print!("#"),
        _ => print!(" "),
      }
    }
    println!("");
  }
  println!("");
}

fn printWorld3d(world: &HashSet<Pos3d>, size: usize)
{
  let mut dims: Vec<i64> = Vec::new();
  for pos in world
  {
    if (!dims.contains(&pos.d))
    {
      dims.push(pos.d);
    }
  }
  dims.sort();

  for dim in dims
  {
    println!("Dimension {}", dim);
    for y in 0..size
    {
      for x in 0..size
      {
        if (world.contains(&Pos3d::new(x as i64, y as i64, dim)))
        {
          print!("#");
        }
        else
        {
          print!(".");
        }
      }
      println!("");
    }
    println!("");
  }
}

fn diversity(world: &Vec<i64>, size: usize) -> u32
{
  let mut divers: u32 = 0;
  for i in 0..size*size
  {
    if (world[i] == 1)
    {
      divers += (2 as u32).pow(i as u32)
    }
  }
  return divers;
}

#[derive(Hash, Eq, PartialEq, Debug)]
struct Pos3d
{
  x: i64,
  y: i64,
  d: i64,
}

impl Pos3d
{
  fn new(x: i64, y: i64, d: i64) -> Pos3d
  {
    return Pos3d{x: x, y: y, d: d};
  }
  
  fn newCopy(pos: &Pos3d) -> Pos3d
  {
    return Pos3d{x: pos.x, y: pos.y, d: pos.d};
  }

  fn get(&self, index: usize) -> i64
  {
    match index
    {
      0 => return self.x,
      1 => return self.y,
      2 => return self.d,
      _ => panic!("Wrong index {}", index),
    }
  }

  fn neighbours(&self, size: i64) -> Vec<Pos3d>
  {
    let mut positions: Vec<Pos3d> = Vec::new();

    for dir in 0..4
    {
      let i1: usize;
      //let i2: usize;
      let ox: i64;
      let oy: i64;
      match dir
      {
        0 => {i1 = 0; ox = -1; oy = 0;}, // Left
        1 => {i1 = 1; ox = 0; oy = -1;}, // Up
        2 => {i1 = 0; ox = 1; oy = 0;}, // Right
        3 => {i1 = 1; ox = 0; oy = 1;}, // Down
        _ => panic!("Wrong dir {}", dir),
      }

      if (self.get(i1) == 0 && (dir == 0 || dir == 1)) // Top or left.
      {
        positions.push(Pos3d::new(2 + ox, 2 + oy, self.d+1));
      }
      else if (self.get(i1) == size-1 && (dir == 2 || dir == 3)) // Bottom or right.
      {
        positions.push(Pos3d::new(2 + ox, 2 + oy, self.d+1));
      }
      else if (self.x + ox == 2 && self.y + oy == 2) // Next to center.
      {
        for i in 0..size
        {
          match dir
          {
            0 => {positions.push(Pos3d::new(size-1, i, self.d-1));}, // Left
            1 => {positions.push(Pos3d::new(i, size-1, self.d-1));}, // Up
            2 => {positions.push(Pos3d::new(0, i, self.d-1));}, // Right
            3 => {positions.push(Pos3d::new(i, 0, self.d-1));}, // Down
            _ => panic!("Wrong dir {}", dir),
          }
        }
      }
      else // Other.
      {
        positions.push(Pos3d::new(self.x + ox, self.y + oy, self.d));
      }
    }

    return positions;
  }
}

fn main()
{
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");

  // First part:
  let mut world: Vec<i64> = Vec::new();
  let size = 5;
  for line in input.lines()
  {
    for character in line.chars()
    {
      match character
      {
        '#' => {world.push(1)},
        '.' => {world.push(0)},
        _ => panic!("Unknown char {}", character),
      };
    }
  }

  let mut diversityHistory: HashSet<u32> = HashSet::new();
  printWorld(&world, size);

  loop
  {
    let mut newWorld: Vec<i64> = vec![0; world.len()];
    for i in 0..size*size
    {
      let x = i % size;
      let y = i / size;

      let mut neighbours = 0;
      if (x > 0 && world[x-1 + y*size] == 1) {neighbours += 1;}
      if (x < size-1 && world[x+1 + y*size] == 1) {neighbours += 1;}
      if (y > 0 && world[x + (y-1)*size] == 1) {neighbours += 1;}
      if (y < size-1 && world[x + (y+1)*size] == 1) {neighbours += 1;}

      if (world[i] == 1 && neighbours != 1)
      {
        newWorld[i] = 0;
      }
      else if (world[i] == 0 && (neighbours == 1 ||  neighbours == 2))
      {
        newWorld[i] = 1;
      }
      else
      {
        newWorld[i] = world[i];
      }
    }

    world = newWorld;
    //printWorld(&world, size);
    let divers = diversity(&world, size);
    if (diversityHistory.contains(&divers))
    {
      println!("Diversity {}", divers);
      break;
    }
    diversityHistory.insert(divers);
  }

  // Second part:
  let mut world: HashSet<Pos3d> = HashSet::new();
  let size: usize = 5;
  let mut i: i64 = 0;
  for line in input.lines()
  {
    for character in line.chars()
    {
      if (character == '#')
      {
        world.insert(Pos3d::new(i % size as i64, i / size as i64, 0));
      }
      i += 1;
    }
  }

  printWorld3d(&world, size);

  for _ in 0..200
  {
    let mut newWorld: HashSet<Pos3d> = HashSet::new();
    let mut checking: HashSet<Pos3d> = HashSet::new();

    for pos in &world
    {
      for posN in pos.neighbours(size as i64)
      {
        checking.insert(posN);
      }
    }

    for pos in &checking
    {
      let mut neighbours = 0;
      for posN in pos.neighbours(size as i64)
      {
        if (world.contains(&posN))
        {
          neighbours += 1;
        }
      }

      if (world.contains(pos) && neighbours != 1)
      {
        // Dies.
      }
      else if (!world.contains(pos) && (neighbours == 1 ||  neighbours == 2))
      {
        // New.
        newWorld.insert(Pos3d::newCopy(pos));
      }
      else
      {
        if (world.contains(pos))
        {
          newWorld.insert(Pos3d::newCopy(pos));
        }
      }
    }

    world = newWorld;
    //printWorld3d(&world, size);
  }
  //printWorld3d(&world, size);
  println!("Bugs: {}", world.len());
}
