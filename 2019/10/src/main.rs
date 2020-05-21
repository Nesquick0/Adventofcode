#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashMap;
use std::cell::Cell;

type TAsteroids = HashMap<(i64, i64), Cell<i64>>;

fn isVisible(x: i64, y: i64, xt: i64, yt: i64, asteroids: &TAsteroids) -> bool
{
  // Same spot = visible.
  if (x == xt && y == yt)
  {
    return false;
  }

  // Find the lowest fraction.
  let mut i: i64 = 2;
  let mut stepX: i64 = xt - x;
  let mut stepY: i64 = yt - y;
  while (i <= i64::abs(stepX) && i <= i64::abs(stepY))
  {
    if (stepX % i == 0 && stepY % i == 0)
    {
      stepX = stepX / i;
      stepY = stepY / i;
      i = 1;
    }

    i += 1;
  }

  if (stepX == 0)
  {
    stepY /= i64::abs(stepY);
  }
  if (stepY == 0)
  {
    stepX /= i64::abs(stepX);
  }

  // Check each asteroid if in way.
  let mut posX: i64 = x + stepX;
  let mut posY: i64 = y + stepY;
  while (posX != xt || posY != yt)
  {
    if (asteroids.contains_key(&(posX, posY)))
    {
      // Other asteroid in way.
      return false;
    }

    posX = posX + stepX;
    posY = posY + stepY;
  }

  // Nothing found. Visible.
  return true;
}

fn printSpace(height: usize, width: usize, asteroids: &TAsteroids, (maxX, maxY): (i64, i64))
{
  for y in 0..height as i64
  {
    for x in 0..width as i64
    {
      if (asteroids.contains_key(&(x, y)))
      {
        if (x == maxX && y == maxY)
        {
          print!(".");
        }
        else
        {
          print!("#");
        }
        //print!("{}", asteroids.get(&(x, y)).unwrap().get())
      }
      else
      {
        print!(" ");
      }
    }
    print!("\n");
  }
}

fn dotProduct(ax: i64, ay: i64, bx: i64, by :i64) -> f64
{
  let aLen: f64 = 1.0/((ax*ax + ay*ay) as f64).sqrt();
  let bLen: f64 = 1.0/((bx*bx + by*by) as f64).sqrt();
  return ((ax * bx) as f64 * aLen * bLen) + ((ay * by) as f64 * aLen * bLen);
}

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");

  let mut asteroids: TAsteroids = HashMap::new();

  let mut width: usize = 0;
  
  let mut y = 0;
  for line in input.lines()
  {
    let mut x = 0;
    for char in line.chars()
    {
      if (char == '#')
      {
        asteroids.insert((x, y), Cell::new(0));
      }
      x += 1;
    }
    y += 1;
    width = line.chars().count();
  }
  let height = input.lines().count();

  println!("W {}, H {}", width, height);

  // First part:
  let mut maxVisible: i64 = 0;
  for (asteroid, value) in &asteroids
  {
    let mut count: i64 = 0;
    let (x, y) = asteroid;
    for (other, _) in &asteroids
    {
      let (xt, yt) = other;
      if (isVisible(*x, *y, *xt, *yt, &asteroids))
      {
        count += 1;
      }
    }
    value.set(count);
    maxVisible = std::cmp::max(maxVisible, count);
  }
  // Find max.
  let mut maxX: i64 = -1;
  let mut maxY: i64 = -1;
  for (asteroid, value) in &asteroids
  {
    if (value.get() == maxVisible)
    {
      maxX = asteroid.0;
      maxY = asteroid.1;
    }
  }

  printSpace(height, width, &asteroids, (maxX, maxY));
  println!("Max visible {}", maxVisible);

  // Second part:
  // Get all visible asteroids and sort them by angle.
  let laser: (i64, i64) = (maxX, maxY);
  let mut destroyed = 0;
  
  while (asteroids.len() > 1)
  {
    let mut targets: Vec<(i64, i64)> = Vec::new();

    for (asteroid, _) in &asteroids
    {
      let (x, y) = asteroid;
      if (isVisible(laser.0, laser.1, *x, *y, &asteroids))
      {
        targets.push((*x, *y));
      }
    }

    targets.sort_by(|a, b| {
      if ((a.0 >= laser.0 && b.0 < laser.0) || (a.0 < laser.0 && b.0 >= laser.0)) // Different side
      {
        return b.0.cmp(&a.0);
      }
      else // Same side
      {
        let result = dotProduct(0, 1, a.0 - laser.0, a.1 - laser.1).partial_cmp(&dotProduct(0, 1, b.0 - laser.0, b.1 - laser.1)).unwrap();
        return if (a.0 >= laser.0) {result} else {result.reverse()};
      }
    });
    for target in targets
    {
      destroyed += 1;
      asteroids.remove(&target);
      if (destroyed == 200)
      {
        println!("{}th {},{} - Result {}", destroyed, target.0, target.1, target.0*100+target.1);
      }
    }
  }
} 