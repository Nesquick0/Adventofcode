#![allow(non_snake_case)]
#![allow(unused_parens)]
#![allow(unused_variables)]

use regex::Regex;
use std::fs;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

fn part1(text: &String) {
    let pattern =
        Regex::new(r"^Sensor at x=(?P<sx>[-\d]+), y=(?P<sy>[-\d]+): closest beacon is at x=(?P<bx>[-\d]+), y=(?P<by>[-\d]+)$").unwrap();
    let targetY: i64 = 2000000; //10;
    let mut cover: Vec<(i64, i64)> = Vec::new();
    for line in text.lines() {
        let m = pattern.captures(line).unwrap();
        let [sx, sy, bx, by] = [m.name("sx"), m.name("sy"), m.name("bx"), m.name("by")]
            .map(|x| x.unwrap().as_str().parse::<i64>().unwrap());

        let distance = (bx - sx).abs() + (by - sy).abs();

        // Get limits on target Y.
        let distToTargetY = (targetY - sy).abs();
        if (distance >= distToTargetY) {
            let offsetX: i64 = distance - distToTargetY;
            cover.push((sx - offsetX, sx + offsetX));
        }
    }
    cover.sort_by_key(|x| x.0);
    let mut totalPositions: i64 = 0;
    let mut curPos: i64 = cover.get(0).unwrap().0;
    for pos in cover {
        if (pos.0 <= curPos && pos.1 > curPos) {
            totalPositions += pos.1 - curPos;
            curPos = pos.1;
        } else if (pos.0 > curPos) {
            curPos = pos.1;
            totalPositions += pos.1 - pos.0;
        }
    }
    println!("{}\n", totalPositions);
}

fn part2(text: &String) {
    let pattern =
        Regex::new(r"^Sensor at x=(?P<sx>[-\d]+), y=(?P<sy>[-\d]+): closest beacon is at x=(?P<bx>[-\d]+), y=(?P<by>[-\d]+)$").unwrap();
    let limits: (i64, i64) = (0, 4000000); // (0, 20);
    let mut sensors: Vec<(i64, i64, i64)> = Vec::new();
    for line in text.lines() {
        let m = pattern.captures(line).unwrap();
        let [sx, sy, bx, by] = [m.name("sx"), m.name("sy"), m.name("bx"), m.name("by")]
            .map(|x| x.unwrap().as_str().parse::<i64>().unwrap());

        let distance = (bx - sx).abs() + (by - sy).abs();
        sensors.push((sx, sy, distance));
    }
    // Sort by Y to get range of valid
    //sensors.sort_by_key(|x| x.1);
    //let yRange = (sensors.first().unwrap().1, sensors.last().unwrap().1);
    let yRange: (i64, i64) = (limits.0, limits.1);
    sensors.sort_by_key(|x| x.0);

    let mut found: Option<(i64, i64)> = None;
    for y in yRange.0..=yRange.1 {
        let mut cover: Vec<(i64, i64)> = Vec::new();
        for sensor in sensors.iter() {
            // Get limits on target Y.
            let distToTargetY = (y - sensor.1).abs();
            if (sensor.2 >= distToTargetY) {
                let offsetX: i64 = sensor.2 - distToTargetY;
                cover.push((
                    sensor.0 - offsetX,
                    std::cmp::min(sensor.0 + offsetX, limits.1),
                ));
            }
        }

        cover.sort_by_key(|x| x.0);
        let mut curPos: i64 = 0;
        for pos in cover {
            if (pos.0 > curPos + 1) {
                found = Some((curPos + 1, y));
                break;
            } else if (pos.0 <= curPos && pos.1 > curPos) {
                curPos = pos.1;
            } else if (pos.0 > curPos) {
                curPos = pos.1;
            }
        }
        if (found.is_some()) {
            break;
        }
    }
    println!("{},{}", found.unwrap().0, found.unwrap().1);
    println!("{}", found.unwrap().0 * 4000000 + found.unwrap().1);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
