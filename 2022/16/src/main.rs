#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use pathfinding::directed::dijkstra::dijkstra_all;
use regex::Regex;
use std::collections::{HashMap, HashSet, VecDeque};
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

#[derive(Debug)]
struct Valve {
    id: i64,
    flow: i64,
    connections: HashMap<i64, i64>,
}

impl Valve {
    pub fn new() -> Self {
        Self {
            id: 0,
            flow: 0,
            connections: HashMap::new(),
        }
    }

    fn nameToId(name: &str) -> i64 {
        if (name.len() != 2) {
            panic!("Wrong length {}", name.len());
        }

        let mut id: i64 = 0;
        let mut chars = name.chars();
        id += chars.next().unwrap() as i64 * 100;
        id += chars.next().unwrap() as i64;
        return id;
    }

    fn idToName(id: i64) -> String {
        let name: String = format!("{}{}", (id / 100) as u8 as char, (id % 100) as u8 as char);
        return name;
    }
}

trait StatePressure {
    fn getOpened(&self) -> &HashMap<i64, i64>;

    fn totalPressure(&self, valves: &HashMap<i64, Valve>) -> i64 {
        let mut result: i64 = 0;
        for o in self.getOpened() {
            let valve = valves.get(&o.0).unwrap();
            result += valve.flow * o.1;
        }
        return result;
    }
}

#[derive(Debug, Clone)]
struct State {
    pos: i64,
    time: i64,
    opened: HashMap<i64, i64>, // Valve id and when opened.
    visited: HashSet<i64>,     // Valves visited.
}

impl State {
    pub fn new(pos: i64, time: i64) -> Self {
        Self {
            pos: pos,
            time: time,
            opened: HashMap::new(),
            visited: HashSet::new(),
        }
    }
}

impl StatePressure for State {
    fn getOpened(&self) -> &HashMap<i64, i64> {
        return &self.opened;
    }
}

#[derive(Debug, Clone)]
struct State2 {
    pos: i64,
    time: i64,
    opened: HashMap<i64, i64>, // Valve id and when opened.
    visited: HashSet<i64>,     // Valves visited.
    simulateFirst: bool,
}

impl State2 {
    pub fn new(pos: i64, time: i64) -> Self {
        Self {
            pos: pos,
            time: time,
            opened: HashMap::new(),
            visited: HashSet::new(),
            simulateFirst: true,
        }
    }
}

impl StatePressure for State2 {
    fn getOpened(&self) -> &HashMap<i64, i64> {
        return &self.opened;
    }
}

fn part1(text: &String) {
    let pattern =
        Regex::new(r"^Valve (?P<valve>.+) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<other>.+)$").unwrap();
    let mut initValves: HashMap<i64, Valve> = HashMap::new();
    for line in text.lines() {
        let m = pattern.captures(line).unwrap();
        let mut valve = Valve::new();
        valve.id = Valve::nameToId(m.name("valve").unwrap().as_str());
        valve.flow = m.name("flow").unwrap().as_str().parse::<i64>().unwrap();
        let connections: Vec<i64> = m
            .name("other")
            .unwrap()
            .as_str()
            .split(", ")
            .map(|x| Valve::nameToId(x))
            .collect();
        for c in connections {
            valve.connections.insert(c, 1);
        }
        initValves.insert(valve.id, valve);
    }

    // Get only interesting valves. Start and those with flow.
    let mut valves: HashMap<i64, Valve> = HashMap::new();
    let mut valvesWithFlow: Vec<i64> = Vec::new();
    for valve in &initValves {
        if (valve.1.flow > 0 || valve.1.id == 6565/*AA*/) {
            valvesWithFlow.push(*valve.0);
        }
    }

    // Use dijkstra algorithm to find distance between all valves so we won't bother with 0 flow valves.
    for id in initValves.keys() {
        let costs: HashMap<i64, (i64, i64)> = dijkstra_all(id, |&x| {
            let connected: Vec<(i64, i64)> = initValves
                .get(&x)
                .unwrap()
                .connections
                .iter()
                .map(|a| (*a.0, *a.1))
                .collect();
            return connected;
        });
        let valve = initValves.get(id).unwrap();
        if (valve.flow > 0 || valve.id == 6565/*AA*/) {
            let mut newValve = Valve::new();
            newValve.id = valve.id;
            newValve.flow = valve.flow;
            for c in costs {
                if (valvesWithFlow.contains(&c.0)) {
                    newValve.connections.insert(c.0, c.1 .1);
                }
            }
            valves.insert(*id, newValve);
        }
    }

    for valve in &valves {
        println!("{} {:?}", Valve::idToName(*valve.0), valve.1);
    }

    let mut queue: VecDeque<State> = VecDeque::new();
    let mut startState = State::new(6565, 30);
    startState.opened.insert(6565, 0);
    startState.visited.insert(6565);
    queue.push_back(startState);
    let mut maxPressure: i64 = 0;

    while (!queue.is_empty()) {
        let state = queue.pop_front().unwrap();
        if (state.time <= 1) {
            let pressure = state.totalPressure(&valves);
            if (pressure > maxPressure) {
                maxPressure = pressure;
            }
        }

        // Time is at least 2. Open valve if not opened.
        if (!state.opened.contains_key(&state.pos)) {
            let mut newState = state.clone();
            newState.time -= 1;
            newState.opened.insert(newState.pos, newState.time);
            queue.push_front(newState);
            continue;
        }

        // Try to move to other not opened valve.
        let connections = &valves.get(&state.pos).unwrap().connections;
        for c in connections {
            if (c.1 < &(state.time - 1)) {
                if (!state.opened.contains_key(c.0) && !state.visited.contains(c.0)) {
                    let mut newState = state.clone();
                    newState.pos = *c.0;
                    newState.time -= c.1;
                    newState.visited.insert(state.pos);
                    queue.push_front(newState);
                }
            }
        }

        let pressure = state.totalPressure(&valves);
        if (pressure > maxPressure) {
            maxPressure = pressure;
        }
    }
    println!("{}", maxPressure)
}

fn part2(text: &String) {
    let pattern =
    Regex::new(r"^Valve (?P<valve>.+) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<other>.+)$").unwrap();
    let mut initValves: HashMap<i64, Valve> = HashMap::new();
    for line in text.lines() {
        let m = pattern.captures(line).unwrap();
        let mut valve = Valve::new();
        valve.id = Valve::nameToId(m.name("valve").unwrap().as_str());
        valve.flow = m.name("flow").unwrap().as_str().parse::<i64>().unwrap();
        let connections: Vec<i64> = m
            .name("other")
            .unwrap()
            .as_str()
            .split(", ")
            .map(|x| Valve::nameToId(x))
            .collect();
        for c in connections {
            valve.connections.insert(c, 1);
        }
        initValves.insert(valve.id, valve);
    }

    // Get only interesting valves. Start and those with flow.
    let mut valves: HashMap<i64, Valve> = HashMap::new();
    let mut valvesWithFlow: Vec<i64> = Vec::new();
    for valve in &initValves {
        if (valve.1.flow > 0 || valve.1.id == 6565/*AA*/) {
            valvesWithFlow.push(*valve.0);
        }
    }

    // Use dijkstra algorithm to find distance between all valves so we won't bother with 0 flow valves.
    for id in initValves.keys() {
        let costs: HashMap<i64, (i64, i64)> = dijkstra_all(id, |&x| {
            let connected: Vec<(i64, i64)> = initValves
                .get(&x)
                .unwrap()
                .connections
                .iter()
                .map(|a| (*a.0, *a.1))
                .collect();
            return connected;
        });
        let valve = initValves.get(id).unwrap();
        if (valve.flow > 0 || valve.id == 6565/*AA*/) {
            let mut newValve = Valve::new();
            newValve.id = valve.id;
            newValve.flow = valve.flow;
            for c in costs {
                if (valvesWithFlow.contains(&c.0)) {
                    newValve.connections.insert(c.0, c.1 .1);
                }
            }
            valves.insert(*id, newValve);
        }
    }

    for valve in &valves {
        println!("{} {:?}", Valve::idToName(*valve.0), valve.1);
    }

    let mut queue: VecDeque<State2> = VecDeque::new();
    let mut startState = State2::new(6565, 26);
    startState.opened.insert(6565, 0);
    startState.visited.insert(6565);
    queue.push_back(startState);
    let mut maxPressure: i64 = 0;

    while (!queue.is_empty()) {
        let mut state = queue.pop_front().unwrap();
        if (state.time <= 1) {
            let pressure = state.totalPressure(&valves);
            if (pressure > maxPressure) {
                maxPressure = pressure;
                println!("{} {:?}", maxPressure, state.opened);
            }
        }

        // Switch to second. Reset position and time.
        if (state.simulateFirst) {
            let mut newState = state.clone();
            newState.pos = 6565;
            newState.time = 26;
            newState.simulateFirst = false;
            queue.push_front(newState);
        }

        // Time is at least 2. Open valve if not opened.
        if (!state.opened.contains_key(&state.pos)) {
            let mut newState = state.clone();
            newState.time -= 1;
            newState.opened.insert(newState.pos, newState.time);
            queue.push_front(newState);
            continue;
        }

        // Try to move to other not opened valve.
        let connections = &valves.get(&state.pos).unwrap().connections;
        for c in connections {
            if (c.1 < &(state.time - 1)) {
                if (!state.opened.contains_key(c.0) && !state.visited.contains(c.0)) {
                    let mut newState = state.clone();
                    newState.pos = *c.0;
                    newState.time -= c.1;
                    newState.visited.insert(state.pos);
                    queue.push_front(newState);
                }
            }
        }

        let pressure = state.totalPressure(&valves);
        if (pressure > maxPressure) {
            maxPressure = pressure;
            println!("{} {:?}", maxPressure, state.opened);
        }
    }
    println!("{}", maxPressure)
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    //part1(&text);
    part2(&text);
}
