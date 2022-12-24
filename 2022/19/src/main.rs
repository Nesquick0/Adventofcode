#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use regex::Regex;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

#[derive(Debug, Clone)]
struct Materials {
    ore: i64,
    clay: i64,
    obsidian: i64,
    geode: i64,
}

impl Materials {
    pub fn new(ore: i64, clay: i64, obsidian: i64, geode: i64) -> Self {
        Self {
            ore: ore,
            clay: clay,
            obsidian: obsidian,
            geode: geode,
        }
    }

    fn add(&mut self, other: &Materials) {
        self.ore += other.ore;
        self.clay += other.clay;
        self.obsidian += other.obsidian;
        self.geode += other.geode;
    }

    fn sub(&mut self, other: &Materials) {
        self.ore -= other.ore;
        self.clay -= other.clay;
        self.obsidian -= other.obsidian;
        self.geode -= other.geode;
    }

    fn isEnough(&self, cost: &Materials) -> bool {
        if (self.ore >= cost.ore
            && self.clay >= cost.clay
            && self.obsidian >= cost.obsidian
            && self.geode >= cost.geode)
        {
            return true;
        }
        return false;
    }
}

#[derive(Debug, Clone)]
struct State {
    time: i64,
    materials: Materials,
    robots: Materials,
    goal: u8,
}

impl State {
    pub fn new() -> Self {
        Self {
            time: 24,
            materials: Materials::new(0, 0, 0, 0),
            robots: Materials::new(1, 0, 0, 0),
            goal: 0,
        }
    }
}

#[derive(Debug)]
struct Blueprint {
    id: i64,
    ore: Materials,
    clay: Materials,
    obsidian: Materials,
    geode: Materials,
}

impl Blueprint {
    pub fn new() -> Self {
        Self {
            id: 0,
            ore: Materials::new(0, 0, 0, 0),
            clay: Materials::new(0, 0, 0, 0),
            obsidian: Materials::new(0, 0, 0, 0),
            geode: Materials::new(0, 0, 0, 0),
        }
    }
}

// Based on https://github.com/ash42/adventofcode/blob/main/adventofcode2022/src/nl/michielgraat/adventofcode2022/day19/Day19.java
fn getMaxGeodes(bp: &Blueprint, mut state: State) -> i64 {
    if (state.time <= 0) {
        return state.materials.geode;
    }

    let maxCostOre = std::cmp::max(
        bp.ore.ore,
        std::cmp::max(bp.clay.ore, std::cmp::max(bp.obsidian.ore, bp.geode.ore)),
    );
    if ((state.goal == 0 && state.robots.ore >= maxCostOre)
        || (state.goal == 1 && state.robots.clay >= bp.obsidian.clay)
        || (state.goal == 2
            && (state.materials.obsidian >= bp.geode.obsidian || state.robots.clay == 0)) // I assume this should be state.robots.obsidian, but is running too long with that.
        || (state.goal == 3 && state.robots.obsidian == 0))
    {
        return 0;
    }

    let mut max: i64 = 0;

    while (state.time > 0) {
        let newMaterials = state.robots.clone();
        state.time -= 1;

        if (state.goal == 0 && state.materials.isEnough(&bp.ore)) {
            for goal in 0..4 {
                let mut newState = state.clone();
                newState.materials.sub(&bp.ore);
                newState.materials.add(&newMaterials);
                newState.robots.ore += 1;
                newState.goal = goal;
                max = std::cmp::max(max, getMaxGeodes(bp, newState));
            }
            return max;
        } else if (state.goal == 1 && state.materials.isEnough(&bp.clay)) {
            for goal in 0..4 {
                let mut newState = state.clone();
                newState.materials.sub(&bp.clay);
                newState.materials.add(&newMaterials);
                newState.robots.clay += 1;
                newState.goal = goal;
                max = std::cmp::max(max, getMaxGeodes(bp, newState));
            }
            return max;
        } else if (state.goal == 2 && state.materials.isEnough(&bp.obsidian)) {
            for goal in 0..4 {
                let mut newState = state.clone();
                newState.materials.sub(&bp.obsidian);
                newState.materials.add(&newMaterials);
                newState.robots.obsidian += 1;
                newState.goal = goal;
                max = std::cmp::max(max, getMaxGeodes(bp, newState));
            }
            return max;
        } else if (state.goal == 3 && state.materials.isEnough(&bp.geode)) {
            for goal in 0..4 {
                let mut newState = state.clone();
                newState.materials.sub(&bp.geode);
                newState.materials.add(&newMaterials);
                newState.robots.geode += 1;
                newState.goal = goal;
                max = std::cmp::max(max, getMaxGeodes(bp, newState));
            }
            return max;
        }

        // Can not build a robot, so continue gathering resources.
        state.materials.add(&newMaterials);
        max = std::cmp::max(max, state.materials.geode);
    }

    return max;
}

fn part1(text: &String) {
    // Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    let pattern = Regex::new(r"^Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.$").unwrap();
    let mut totalQuality: i64 = 0;
    for line in text.lines() {
        let m = pattern.captures(line).expect("Wrong pattern");
        let mut bp: Blueprint = Blueprint::new();
        bp.id = m.get(1).unwrap().as_str().parse().unwrap();
        bp.ore = Materials::new(m.get(2).unwrap().as_str().parse().unwrap(), 0, 0, 0);
        bp.clay = Materials::new(m.get(3).unwrap().as_str().parse().unwrap(), 0, 0, 0);
        bp.obsidian = Materials::new(
            m.get(4).unwrap().as_str().parse().unwrap(),
            m.get(5).unwrap().as_str().parse().unwrap(),
            0,
            0,
        );
        bp.geode = Materials::new(
            m.get(6).unwrap().as_str().parse().unwrap(),
            0,
            m.get(7).unwrap().as_str().parse().unwrap(),
            0,
        );

        let mut maxGeodes: i64 = 0;
        for goal in 0..4 {
            let mut initState: State = State::new();
            initState.goal = goal;
            maxGeodes = std::cmp::max(maxGeodes, getMaxGeodes(&bp, initState));
        }

        println!("{} - {}", bp.id, maxGeodes);
        totalQuality += bp.id * maxGeodes;
    }
    println!("Total: {}", totalQuality)
}

fn part2(text: &String) {
    // Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    let pattern = Regex::new(r"^Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.$").unwrap();
    let mut totalScore: i64 = 1;
    let lines = text.lines().collect::<Vec<&str>>();
    for line in &lines[0..(std::cmp::min(3, lines.len()))] {
        let m = pattern.captures(line).expect("Wrong pattern");
        let mut bp: Blueprint = Blueprint::new();
        bp.id = m.get(1).unwrap().as_str().parse().unwrap();
        bp.ore = Materials::new(m.get(2).unwrap().as_str().parse().unwrap(), 0, 0, 0);
        bp.clay = Materials::new(m.get(3).unwrap().as_str().parse().unwrap(), 0, 0, 0);
        bp.obsidian = Materials::new(
            m.get(4).unwrap().as_str().parse().unwrap(),
            m.get(5).unwrap().as_str().parse().unwrap(),
            0,
            0,
        );
        bp.geode = Materials::new(
            m.get(6).unwrap().as_str().parse().unwrap(),
            0,
            m.get(7).unwrap().as_str().parse().unwrap(),
            0,
        );

        let mut maxGeodes: i64 = 0;
        for goal in 0..4 {
            let mut initState: State = State::new();
            initState.time = 32;
            maxGeodes = std::cmp::max(maxGeodes, getMaxGeodes(&bp, initState));
        }

        println!("{} - {}", bp.id, maxGeodes);
        totalScore *= maxGeodes;
    }
    println!("Total: {}", totalScore)
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
