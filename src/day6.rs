#![allow(dead_code)]

use std::collections::HashSet;

use adv2024::{self, Pos};
use itertools::Itertools;

struct Map {
    size: Pos,
    obstacles: HashSet<Pos>,
    guard: Guard,
}

#[derive(Clone, Hash, PartialEq, Eq)]
struct Guard {
    pos: Pos,
    dir: Pos,
}

impl Map {
    fn parse(input: &str) -> Self {
        let lines: Vec<&str> = input.lines().collect_vec();
        let size = Pos::new(lines.len(), lines[0].len());
        let mut obstacles = HashSet::new();
        let mut guard = None;
        for (y, line) in lines.iter().enumerate() {
            for (x, c) in line.chars().enumerate() {
                if c == '#' {
                    obstacles.insert(Pos::new(y as i32, x as i32));
                } else if c != '.' {
                    guard = Some(Guard {
                        pos: Pos::new(y as i32, x as i32),
                        dir: Pos::from_char(c),
                    });
                }
            }
        }

        Self {
            size,
            obstacles,
            guard: guard.unwrap(),
        }
    }

    fn simulate(&self) -> (bool, HashSet<Pos>) {
        let mut guard = self.guard.clone();
        let mut visited = HashSet::new();
        let mut visited_with_dir: HashSet<Guard> = HashSet::new();
        visited.insert(guard.pos);
        visited_with_dir.insert(guard.clone());
        loop {
            let next = guard.pos + guard.dir;
            if !next.check_bounds(&self.size) {
                // Walking out of bounds, we are done.
                return (true, visited);
            }
            if self.obstacles.contains(&next) {
                // Would walk into an obstacle - turn right.
                guard.dir = guard.dir.cw();
            } else {
                guard.pos = next;
                if visited_with_dir.contains(&guard) {
                    return (false, visited);
                }
                visited.insert(guard.pos);
                visited_with_dir.insert(guard.clone());
            }
        }
    }
}

fn main() {
    let input = adv2024::read_input();
    let mut map = Map::parse(&input);

    // Part 1:
    let (exited, visited) = map.simulate();
    println!("visited: {}", visited.len());
    assert!(exited);

    // Part 2:
    let mut count = 0u32;
    for y in 0..map.size.y {
        for x in 0..map.size.x {
            let pos = Pos::new(y, x);
            if pos == map.guard.pos {
                continue;
            }
            if map.obstacles.contains(&pos) {
                continue;
            }
            if !visited.contains(&pos) {
                continue;
            }
            map.obstacles.insert(pos);
            let (exited, _) = map.simulate();
            if !exited {
                count += 1;
            }
            map.obstacles.remove(&pos);
        }
    }
    println!("stuck count: {count}");
}
