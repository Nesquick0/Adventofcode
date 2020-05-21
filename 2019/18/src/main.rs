#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashMap;
use std::collections::HashSet;
type TPositions = HashMap<(i64, i64), i64>;
use std::collections::BinaryHeap;
use std::cmp::Reverse;

fn getPos(x: i64, y: i64, dir: i64) -> (i64, i64)
{
  match dir
  {
    0 => return (x, y-1),
    1 => return (x, y+1),
    2 => return (x+1, y),
    3 => return (x-1, y),
    _ => panic!("Wrong direction!"),
  }
}

fn findPath(maze: &TPositions, doors: &HashMap<&(i64, i64), &i64>, startX: i64, startY: i64, targetX: i64, targetY: i64) -> (i64, Vec<i64>)
{
  let mut visited: HashSet<(i64, i64)> = HashSet::new();
  visited.insert((startX, startY));
  let mut queue: BinaryHeap<Reverse<(i64, i64, i64, i64, Vec<i64>)>> = BinaryHeap::new();
  queue.push(Reverse((i64::abs(targetX-startX) + i64::abs(targetY-startY), startX, startY, 0, Vec::new())));

  while (queue.len() > 0)
  {
    let (_, x, y, dist, blocking) = queue.pop().unwrap().0;

    if (x == targetX && y == targetY)
    {
      return (dist, blocking);
    }

    for dir in 0..4
    {
      let newPos = getPos(x, y, dir);
      if (!visited.contains(&newPos))
      {
        visited.insert(newPos);
        if (maze.get(&newPos).unwrap() != &0) // Only 0 is empty
        {
          continue;
        }
        let mut newBlocked = blocking.clone();
        if (doors.contains_key(&newPos))
        {
          newBlocked.push(**doors.get(&newPos).unwrap())
        }
        queue.push(Reverse((i64::abs(targetX-newPos.0) + i64::abs(targetY-newPos.1), newPos.0, newPos.1, dist+1, newBlocked)));
      }
    }
  }
  return (-1, Vec::new()); // Path not found.
}

struct DepthFirstState
{
  key: i64,
  dist: i64,
  keys: HashSet<i64>,
  doors: HashSet<i64>,
  visitedKeys: Vec<i64>, // Keep sorted
}

impl DepthFirstState
{
  fn new(key: i64, dist: i64, keys: HashSet<i64>, doors: HashSet<i64>, visitedKeys: Vec<i64>) -> DepthFirstState
  {
    return DepthFirstState{
      key: key, dist: dist, keys: keys, doors: doors, visitedKeys: visitedKeys
    }
  }
}

struct DepthFirstState2
{
  robots: [i64; 4],
  dist: i64,
  keys: HashSet<i64>,
  doors: HashSet<i64>,
  visitedKeys: Vec<i64>, // Keep sorted
}

impl DepthFirstState2
{
  fn new(robots: [i64; 4], dist: i64, keys: HashSet<i64>, doors: HashSet<i64>, visitedKeys: Vec<i64>) -> DepthFirstState2
  {
    return DepthFirstState2{
      robots: robots, dist: dist, keys: keys, doors: doors, visitedKeys: visitedKeys
    }
  }
}

fn main()
{
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");

  let mut maze: TPositions = HashMap::new();
  let mut keys: HashMap<i64, (i64, i64)> = HashMap::new();
  let mut doors: HashMap<i64, (i64, i64)> = HashMap::new();
  let mut start: (i64, i64) = (0, 0);

  let mut width: usize = 0;
  
  let mut y = 0;
  for line in input.lines()
  {
    let mut x = 0;
    for character in line.chars()
    {
      match character
      {
        '#' => {maze.insert((x, y), 1);},
        '.' => {maze.insert((x, y), 0);},
        'a'..='z' => {
          maze.insert((x, y), 0);
          keys.insert((character as u8 - 'a' as u8) as i64, (x, y));
        },
        'A'..='Z' => {
          maze.insert((x, y), 0);
          doors.insert((character as u8 - 'A' as u8) as i64, (x, y));
        },
        '@' => {
          maze.insert((x, y), 0);
          start = (x, y);
        },
        _ => panic!("Unknown char {}", character),
      };
      x += 1;
    }
    y += 1;
    width = line.chars().count();
  }
  let height = input.lines().count();

  println!("W {}, H {}", width, height);

  // First part
  // Precompute distances between all keys. Mark blocking doors.
  let mut keyDistances: HashMap<(&i64, &i64), (i64, Vec<i64>)> = HashMap::new();
  let mut doorsSet: HashMap<&(i64, i64), &i64> = HashMap::new();
  for (door, pos) in &doors
  {
    doorsSet.insert(pos, door);
  }

  for (k1, pos1) in &keys
  {
    for (k2, pos2) in &keys
    {
      if (k1 != k2)
      {
        let (dist, blocking) = findPath(&maze, &doorsSet, pos1.0, pos1.1, pos2.0, pos2.1);
        if (dist > 0)
        {
          keyDistances.insert((k1, k2), (dist, blocking.clone()));
          keyDistances.insert((k2, k1), (dist, blocking));
        }
        else
        {
          panic!("Wrong distance {}", dist);
        }
      }
    }

    // Distances from start.
    let (dist, blocking) = findPath(&maze, &doorsSet, start.0, start.1, pos1.0, pos1.1);
    if (dist > 0)
    {
      keyDistances.insert((k1, &-1), (dist, blocking.clone()));
      keyDistances.insert((&-1, k1), (dist, blocking));
    }
    else
    {
      panic!("Wrong distance {}", dist);
    }
  }

  // Go through all combination and find shortes path
  let mut queue: Vec<DepthFirstState> = Vec::new();
  queue.push(DepthFirstState::new(-1, 0, keys.keys().copied().collect(), doors.keys().copied().collect(), Vec::new()));
  let mut shortestDist: i64 = std::i64::MAX;
  let mut shortestStates: HashMap<Vec<i64>, i64> = HashMap::new();

  while (queue.len() > 0)
  {
    let state = queue.pop().unwrap();

    // No keys left, finish.
    if (state.keys.len() == 0)
    {
      if (state.dist < shortestDist)
      {
        shortestDist = state.dist;
      }
      continue;
    }

    for key in &state.keys
    {
      let (dist, blocking) = keyDistances.get(&(&state.key, key)).unwrap();
      let mut valid = true;
      for door in blocking
      {
        if (state.doors.contains(door))
        {
          valid = false;
          break;
        }
      }

      if (valid)
      {
        let newDist: i64 = state.dist+dist;

        let mut newVisitedKeys: Vec<i64> = state.visitedKeys.clone();
        newVisitedKeys.sort();
        newVisitedKeys.push(*key);
        if (shortestStates.contains_key(&newVisitedKeys))
        {
          if (shortestStates.get(&newVisitedKeys).unwrap() <= &newDist)
          {
            continue; // Skip this state. It is longer than previous one.
          }
          else
          {
            shortestStates.insert(newVisitedKeys.clone(), newDist);
          }
        }
        else
        {
          shortestStates.insert(newVisitedKeys.clone(), newDist);
        }

        let mut newKeys: HashSet<i64> = state.keys.clone();
        newKeys.remove(key);
        let mut newDoors: HashSet<i64> = state.doors.clone();
        newDoors.remove(key);
        queue.push(DepthFirstState::new(*key, newDist, newKeys, newDoors, newVisitedKeys));
      }
    }
  }

  println!("Dist: {}", shortestDist);

  // Second part
  maze.insert((start.0, start.1), 1);
  maze.insert((start.0+1, start.1), 1);
  maze.insert((start.0-1, start.1), 1);
  maze.insert((start.0, start.1+1), 1);
  maze.insert((start.0, start.1-1), 1);

  // Precompute distances between all keys. Mark blocking doors.
  keyDistances.clear();

  for (k1, pos1) in &keys
  {
    for (k2, pos2) in &keys
    {
      if (k1 != k2)
      {
        // Find path between keys. They might not connect.
        let (dist, blocking) = findPath(&maze, &doorsSet, pos1.0, pos1.1, pos2.0, pos2.1);
        if (dist > 0)
        {
          keyDistances.insert((k1, k2), (dist, blocking.clone()));
          keyDistances.insert((k2, k1), (dist, blocking));
        }
      }
    }

    // Distances from start all 4 starts.
    for startNew in [ (start.0-1, start.1-1, &-1), (start.0+1, start.1-1, &-2), (start.0+1, start.1+1, &-3), (start.0-1, start.1+1, &-4) ].iter()
    {
      let (dist, blocking) = findPath(&maze, &doorsSet, startNew.0, startNew.1, pos1.0, pos1.1);
      if (dist > 0)
      {
        keyDistances.insert((k1, startNew.2), (dist, blocking.clone()));
        keyDistances.insert((startNew.2, k1), (dist, blocking));
      }
    }
  }

  let mut queue: Vec<DepthFirstState2> = Vec::new();
  queue.push(DepthFirstState2::new([-1, -2, -3, -4], 0, keys.keys().copied().collect(), doors.keys().copied().collect(), Vec::new()));
  let mut shortestDist: i64 = std::i64::MAX;
  let mut shortestStates: HashMap<Vec<i64>, i64> = HashMap::new();

  while (queue.len() > 0)
  {
    let state = queue.pop().unwrap();

    // No keys left, finish.
    if (state.keys.len() == 0)
    {
      if (state.dist < shortestDist)
      {
        shortestDist = state.dist;
      }
      continue;
    }
    
    for iRobot in 0..4
    {
      for key in &state.keys
      {
        let distOption = keyDistances.get(&(&state.robots[iRobot], key));
        if (distOption.is_none())
        {
          continue;
        }

        let (dist, blocking) = distOption.unwrap();
        let mut valid = true;
        for door in blocking
        {
          if (state.doors.contains(door))
          {
            valid = false;
            break;
          }
        }

        if (valid)
        {
          let newDist: i64 = state.dist+dist;

          let mut futureVisitedKeys: Vec<i64> = state.visitedKeys.clone();
          let mut newRobotsPos = state.robots.clone();
          newRobotsPos[iRobot] = *key;
          futureVisitedKeys.extend(newRobotsPos.iter());
          if (shortestStates.contains_key(&futureVisitedKeys) && shortestStates.get(&futureVisitedKeys).unwrap() <= &newDist)
          {
            continue; // Skip this state. It is longer than previous one.
          }
          else
          {
            shortestStates.insert(futureVisitedKeys, newDist);
          }

          let mut newKeys: HashSet<i64> = state.keys.clone();
          newKeys.remove(key);
          let mut newDoors: HashSet<i64> = state.doors.clone();
          newDoors.remove(key);

          let mut newVisitedKeys = state.visitedKeys.clone();
          newVisitedKeys.push(*key);
          newVisitedKeys.sort();
          queue.push(DepthFirstState2::new(newRobotsPos, newDist, newKeys, newDoors, newVisitedKeys));
        }
      }
    }
  }

  println!("Dist: {}", shortestDist);
} 