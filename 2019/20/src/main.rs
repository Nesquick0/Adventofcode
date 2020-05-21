#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::collections::HashMap;
use std::collections::HashSet;
type TPositions = HashMap<(i64, i64), i64>;

struct Portal
{
  pos1: (i64, i64),
  pos2: (i64, i64),
}

impl Portal
{
  fn new(x1: i64, y1: i64, x2: i64, y2: i64) -> Portal
  {
    return Portal{pos1: (x1, y1), pos2: (x2, y2)};
  }
}

fn getPos(x: i64, y: i64, dir: i64) -> (i64, i64)
{
  match dir
  {
    0 => return (x, y-1),
    1 => return (x+1, y),
    2 => return (x, y+1),
    3 => return (x-1, y),
    _ => panic!("Wrong direction!"),
  }
}

fn findPath(maze: &TPositions, portals: &HashMap<String, Portal>, startX: i64, startY: i64, targetX: i64, targetY: i64) -> i64
{
  let mut visited: HashSet<(i64, i64)> = HashSet::new();
  visited.insert((startX, startY));
  let mut queue: std::collections::VecDeque<(i64, i64, i64)> = std::collections::VecDeque::new(); 
  queue.push_back((startX, startY, 0));

  while (queue.len() > 0)
  {
    let (x, y, dist) = queue.pop_front().unwrap();

    if (x == targetX && y == targetY)
    {
      return dist;
    }

    for dir in 0..4
    {
      let newPos = getPos(x, y, dir);
      if (!visited.contains(&newPos))
      {
        visited.insert(newPos);
        let mut foundPortal = false;
        for portal in portals
        {
          if (portal.1.pos1.0 == newPos.0 && portal.1.pos1.1 == newPos.1)
          {
            queue.push_back((portal.1.pos2.0, portal.1.pos2.1, dist+2));
            visited.insert((portal.1.pos2.0, portal.1.pos2.1));
            foundPortal = true;
            break;
          } else if (portal.1.pos2.0 == newPos.0 && portal.1.pos2.1 == newPos.1)
          {
            queue.push_back((portal.1.pos1.0, portal.1.pos1.1, dist+2));
            visited.insert((portal.1.pos1.0, portal.1.pos1.1));
            foundPortal = true;
            break;
          }
        }
        if (foundPortal)
        {
          continue;
        }
        if (maze.get(&newPos).unwrap_or(&-1) != &0) // Only 0 is empty
        {
          continue;
        }
        queue.push_back((newPos.0, newPos.1, dist+1));
      }
    }
  }
  return -1; // Path not found.
}

fn findPathLevels(maze: &TPositions, portals: &HashMap<String, Portal>, startX: i64, startY: i64, targetX: i64, targetY: i64) -> i64
{
  let mut visited: HashSet<(i64, i64, i64)> = HashSet::new();
  visited.insert((startX, startY, 0));
  let mut queue: std::collections::VecDeque<(i64, i64, i64, i64)> = std::collections::VecDeque::new(); 
  queue.push_back((startX, startY, 0, 0));

  while (queue.len() > 0)
  {
    let (x, y, dist, level) = queue.pop_front().unwrap();

    if (x == targetX && y == targetY && level == 0)
    {
      return dist;
    }

    for dir in 0..4
    {
      let newPos = getPos(x, y, dir);
      if (!visited.contains(&(newPos.0, newPos.1, level)))
      {
        visited.insert((newPos.0, newPos.1, level));
        let mut foundPortal = false;
        for portal in portals
        {
          if (portal.1.pos1.0 == newPos.0 && portal.1.pos1.1 == newPos.1)
          {
            queue.push_back((portal.1.pos2.0, portal.1.pos2.1, dist+2, level+1));
            visited.insert((portal.1.pos2.0, portal.1.pos2.1, level+1));
            foundPortal = true;
            break;
          } else if (portal.1.pos2.0 == newPos.0 && portal.1.pos2.1 == newPos.1 && level > 0)
          {
            queue.push_back((portal.1.pos1.0, portal.1.pos1.1, dist+2, level-1));
            visited.insert((portal.1.pos1.0, portal.1.pos1.1, level-1));
            foundPortal = true;
            break;
          }
        }
        if (foundPortal)
        {
          continue;
        }
        if (maze.get(&newPos).unwrap_or(&-1) != &0) // Only 0 is empty
        {
          continue;
        }
        queue.push_back((newPos.0, newPos.1, dist+1, level));
      }
    }
  }
  return -1; // Path not found.
}

fn main()
{
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");

  let mut maze: TPositions = HashMap::new();
  let mut portals: HashMap<String, Portal> = HashMap::new();
  let mut width: usize = 0;
  
  let lines: Vec<&str> = input.lines().collect();
  for y in 0..lines.len()
  {
    let chars: Vec<char> = lines[y].chars().collect();
    width = chars.len();
    for x in 0..chars.len()
    {
      match chars[x]
      {
        '#' => {maze.insert((x as i64, y as i64), 1);},
        '.' => {maze.insert((x as i64, y as i64), 0);},
        'A'..='Z' => {
          for dir in 0..4
          {
            let (newX, newY) = getPos(x as i64, y as i64, dir);
            if (newX < 0 || newY < 0)
            {
              continue;
            }
            if (lines.get(newY as usize).unwrap_or(&"").get(newX as usize..newX as usize + 1).unwrap_or(&"") == ".")
            {
              let (opX, opY): (i64, i64) = getPos(x as i64, y as i64, (dir + 2) % 4);
              let name: String;
              if (dir == 0 || dir == 3)
              {
                name = chars[x].to_string() + &lines.get(opY as usize).unwrap_or(&"").get(opX as usize..opX as usize + 1).unwrap_or(&"").to_string();
              }
              else
              {
                name = lines.get(opY as usize).unwrap_or(&"").get(opX as usize..opX as usize + 1).unwrap_or(&"").to_string() + &chars[x].to_string();
              }
              if (portals.contains_key(&name))
              {
                let p: &mut Portal = portals.get_mut(&name).unwrap();
                p.pos2.0 = newX;
                p.pos2.1 = newY;
              }
              else
              {
                portals.insert(name, Portal::new(newX, newY, 0, 0));
              }
            }
          }
        },
        ' ' => {},
        _ => panic!("Unknown char {}", chars[x]),
      };
    }
  }
  let height: usize = lines.len();

  let startP: &Portal = portals.get(&"AA".to_string()).unwrap();
  let start: (i64, i64) = startP.pos1;
  portals.remove(&"AA".to_string());
  let targetP: &Portal = portals.get(&"ZZ".to_string()).unwrap();
  let target: (i64, i64) = targetP.pos1;
  portals.remove(&"ZZ".to_string());
  // for portal in &portals
  // {
  //   println!("{} - {:?} {:?}", portal.0, portal.1.pos1, portal.1.pos2);
  // }
  for portal in &mut portals
  {
    if (portal.1.pos1.0 == 2 || portal.1.pos1.1 == 2 || portal.1.pos1.0 == (width as i64)-3 || portal.1.pos1.1 == (height as i64)-3)
    {
      std::mem::swap(&mut portal.1.pos1, &mut portal.1.pos2);
    }
  }

  // First part:
  let dist: i64 = findPath(&maze, &portals, start.0, start.1, target.0, target.1);
  println!("Dist {}", dist);

  // Second part:
  let dist: i64 = findPathLevels(&maze, &portals, start.0, start.1, target.0, target.1);
  println!("Dist {}", dist);
} 