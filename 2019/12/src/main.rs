#![allow(non_snake_case)]
#![allow(unused_parens)]

extern crate num;

use regex::Regex;
use std::cell::RefCell;

#[derive(Debug)]
#[derive(Clone)]
struct Moon
{
  x: i64,
  y: i64,
  z: i64,
  vx: i64,
  vy: i64,
  vz: i64
}

impl Moon
{
  fn new(ix: i64, iy: i64, iz: i64) -> Moon
  {
    return Moon {x: ix, y: iy, z: iz, vx: 0, vy: 0, vz: 0};
  }

  fn updatePosition(&mut self)
  {
    self.x += self.vx;
    self.y += self.vy;
    self.z += self.vz;
  }

  fn get(&self, i: usize) -> i64
  {
    match i
    {
      0 => return self.x,
      1 => return self.y,
      2 => return self.z,
      3 => return self.vx,
      4 => return self.vy,
      5 => return self.vz,
      _ => return 0,
    }
  }
}

fn getPotencial(moon: &Moon) -> i64
{
  return (i64::abs(moon.x) + i64::abs(moon.y) + i64::abs(moon.z));
}

fn getKinetic(moon: &Moon) -> i64
{
  return (i64::abs(moon.vx) + i64::abs(moon.vy) + i64::abs(moon.vz));
}

fn getEnergy(moon: &Moon) -> i64
{
  return getPotencial(moon) * getKinetic(moon);
}

fn getTotalEnergy(moons: &Vec<RefCell<Moon>>) -> i64
{
  let mut totalEnergy: i64 = 0;
  for moon in moons
  {
    totalEnergy += getEnergy(&moon.borrow());
  }
  return totalEnergy;
}

fn printState(moons: &Vec<RefCell<Moon>>)
{
  for moon in moons
  {
    println!("pos: {:3} {:3} {:3}, vel: {:3} {:3} {:3}",
      moon.borrow().x, moon.borrow().y, moon.borrow().z,
      moon.borrow().vx, moon.borrow().vy, moon.borrow().vz);
  }
  println!("Energy: {}", getTotalEnergy(moons));
}

fn main()
{
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");

  // Create map.
  let mut moons: Vec<RefCell<Moon>> = Vec::new();
  let re = Regex::new(r"^<x=(?P<x>[-\d]+), y=(?P<y>[-\d]+), z=(?P<z>[-\d]+)>$").unwrap();
  // Periods for each axis.
  let mut periods: [i64; 3] = [0, 0, 0];

  for line in input.lines()
  {
    for m in re.captures_iter(line)
    {
      //println!("{:?}", m);
      let moon: Moon = Moon::new(
        m.name("x").unwrap().as_str().parse::<i64>().unwrap(),
        m.name("y").unwrap().as_str().parse::<i64>().unwrap(),
        m.name("z").unwrap().as_str().parse::<i64>().unwrap());
        moons.push(RefCell::new(moon));
    }
  }
  //println!("{:?}", moons);
  let startState = moons.clone();
  printState(&moons);

  let mut iter: i64 = 0;
  loop
  {
    // Simulate gravity.
    for moon in &moons
    {
      let (mut gx, mut gy, mut gz): (i64, i64, i64) = (0, 0, 0);
      for other in &moons
      {
        if (moon.borrow().x < other.borrow().x) {gx += 1;}
        else if (moon.borrow().x > other.borrow().x) {gx -= 1;}

        if (moon.borrow().y < other.borrow().y) {gy += 1;}
        else if (moon.borrow().y > other.borrow().y) {gy -= 1;}

        if (moon.borrow().z < other.borrow().z) {gz += 1;}
        else if (moon.borrow().z > other.borrow().z) {gz -= 1;}
      }
      moon.borrow_mut().vx += gx;
      moon.borrow_mut().vy += gy;
      moon.borrow_mut().vz += gz;
    }
    // Update position.
    for moon in &moons
    {
      moon.borrow_mut().updatePosition();
    }

    iter += 1;

    // Print.
    if (iter == 1000)
    {
      println!("Step {}", iter);
      printState(&moons);
    }

    // Calculate periods. Based on solution from net.
    for ax in 0..3
    {
      // Skip already found.
      if (periods[ax] != 0)
      {
        continue;
      }

      // Find period.
      let mut allOrig = true;
      for i in 0..moons.len()
      {
        if !(moons[i].borrow().get(ax) == startState[i].borrow().get(ax) && moons[i].borrow().get(ax+3) == 0 && periods[ax] == 0)
        {
          allOrig = false;
        }
      }
      if (allOrig)
      {
        periods[ax] = iter;
      }
    }
    // Check if all periods found.
    let mut allPeriods: bool = true;
    for p in &periods
    {
      if (*p == 0)
      {
        allPeriods = false;
        break;
      }
    }
    
    // Finish by calculating LCM.
    if (allPeriods)
    {
      println!("Periods {:?}", &periods);
      println!("Iter {}", iter);
      let lcm: i64 = num::integer::lcm(periods[0], num::integer::lcm(periods[1], periods[2]));
      println!("Lcm {}", lcm);
      break;
    }
  }
}
