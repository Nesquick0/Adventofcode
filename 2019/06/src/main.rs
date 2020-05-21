#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;

#[derive(Debug)]
struct Orbits
{
  planets: Vec<String>,
  parent: String,
  distance: i64
}

impl Orbits
{
  fn new() -> Orbits
  {
    return Orbits {planets: Vec::new(), parent: "".to_string(), distance: 0};
  }
}

fn main()
{
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  
  // Create map.
  let mut planets: HashMap<String, Orbits> = HashMap::new();
  for line in input.lines()
  {
    let points: Vec<_> = line.split(")").collect();
    let first: String = points[0].to_string();
    let second: String = points[1].to_string();

    let planet: &mut Orbits = planets.entry(first.clone()).or_insert(Orbits::new());
    planet.planets.push(second.clone());

    let planet: &mut Orbits = planets.entry(second.clone()).or_insert(Orbits::new());
    planet.parent = first.clone();
  }

  // Start with COM and build distances.
  let mut queue: VecDeque<String> = VecDeque::new();
  queue.push_back("COM".to_string());
  while (queue.len() > 0)
  {
    let name = queue.pop_front().unwrap();
    let planet: &Orbits = planets.get(&name).unwrap();
    let mut distance = 0;

    if (!planet.parent.is_empty())
    {
      let parent: &Orbits = planets.get(&planet.parent).unwrap();
      distance = parent.distance + 1;
    }
    
    let planet: &mut Orbits = planets.get_mut(&name).unwrap();
    planet.distance = distance;
    for other in &planet.planets
    {
      queue.push_back(other.clone());
    }
  }

  // Sum of distances.
  let mut totalDist: i64 = 0;
  for (_name, planet) in &planets
  {
    totalDist += planet.distance;
  }
  println!("Total dist {}", totalDist);

  // Find distance between YOU and SAN (second part).
  // First get way from YOU to COM.
  let mut searchMap: HashSet<String> = HashSet::new();
  let start: String = "YOU".to_string();
  searchMap.insert(start.clone());
  let mut name = start;
  loop
  {
    name = planets.get(&name).unwrap().parent.clone();
    if (name.is_empty())
    {
      break;
    }
    searchMap.insert(name.clone());
  }
  // Then go through SAN to COM and check for same planet as with YOU.
  let mut name = "SAN".to_string();
  loop
  {
    name = planets.get(&name).unwrap().parent.clone();
    if (name.is_empty())
    {
      println!("Nothing found!");
      break;
    }
    if (searchMap.contains(&name))
    {
      // Found planet.
      let distance: i64 = (planets.get(&"YOU".to_string()).unwrap().distance - 1 - planets.get(&name).unwrap().distance) +
        (planets.get(&"SAN".to_string()).unwrap().distance - 1 - planets.get(&name).unwrap().distance);
      println!("Distance YOU to SAN: {}", distance);
      break;
    }
  }
}
