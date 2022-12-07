#![allow(non_snake_case)]
#![allow(unused_parens)]

use std::cell::RefCell;
use std::fs;
use std::rc::Rc;

fn readToString(filename: &str) -> std::io::Result<String> {
    let text = fs::read_to_string(filename)?;
    Ok(text)
}

struct Item {
    name: String,
    files: Vec<Rc<RefCell<Item>>>,
    size: usize,
    parent: Option<Rc<RefCell<Item>>>,
}

impl Item {
    pub fn new(name: String) -> Self {
        Self {
            name: name,
            files: Vec::new(),
            size: 0,
            parent: None,
        }
    }
}

fn calculateStructure(text: &String) -> Rc<RefCell<Item>> {
    // Read directory structure.
    let root: Rc<RefCell<Item>> = Rc::new(RefCell::new(Item::new("/".to_string())));
    let mut currentDir: Rc<RefCell<Item>> = Rc::clone(&root);
    for line in text.lines() {
        if (line.starts_with("$ cd ")) {
            let path = &line[5..];
            if (path == "/") {
                currentDir = Rc::clone(&root);
            } else if (path == "..") {
                let tempParent = Rc::clone(&currentDir.as_ref().borrow().parent.as_ref().unwrap());
                currentDir = tempParent;
            } else {
                let child: Rc<RefCell<Item>>;
                {
                    let mut currentRef = currentDir.as_ref().borrow_mut();
                    let childFound = currentRef
                        .files
                        .iter()
                        .find(|x| x.as_ref().borrow().name == path.to_string());
                    if (childFound.is_none()) {
                        let newChild: Rc<RefCell<Item>> =
                            Rc::new(RefCell::new(Item::new(path.to_string())));
                        newChild.as_ref().borrow_mut().parent = Some(Rc::clone(&currentDir));
                        currentRef.files.push(Rc::clone(&newChild));
                        child = Rc::clone(&newChild);
                    } else {
                        child = Rc::clone(&childFound.unwrap());
                    }
                }
                currentDir = Rc::clone(&child);
            }
            //println!("{}", path);
        } else if (line.starts_with("$ ls")) {
            // Ignore.
        } else if (line.starts_with("dir ")) {
            // Ignore.
        } else {
            let mut split = line.split_whitespace();
            let fileSize: usize = split.next().unwrap().parse::<usize>().unwrap();
            let name: String = split.next().unwrap().to_string();

            let mut currentRef = currentDir.as_ref().borrow_mut();
            let newChild: Rc<RefCell<Item>> = Rc::new(RefCell::new(Item::new(name)));
            newChild.as_ref().borrow_mut().size = fileSize;
            newChild.as_ref().borrow_mut().parent = Some(Rc::clone(&currentDir));
            currentRef.files.push(Rc::clone(&newChild));
        }
    }

    // Calculate size of directories.
    currentDir = Rc::clone(&root);
    loop {
        let mut found: Option<Rc<RefCell<Item>>> = None;
        let mut dirSize: usize = 0;
        {
            for x in currentDir.as_ref().borrow().files.iter() {
                if (x.borrow().size == 0) {
                    found = Some(Rc::clone(&x));
                    break;
                } else {
                    dirSize += x.borrow().size;
                }
            }
        }

        if (found.is_none()) {
            currentDir.as_ref().borrow_mut().size = dirSize;
            if (currentDir.as_ref().borrow().name == "/") {
                break;
            } else {
                let tempParent = Rc::clone(&currentDir.as_ref().borrow().parent.as_ref().unwrap());
                currentDir = tempParent;
            }
        } else {
            currentDir = Rc::clone(&found.unwrap());
        }
    }

    return root;
}

fn part1(text: &String) {
    let root = calculateStructure(text);
    let mut queue: Vec<Rc<RefCell<Item>>> = Vec::new();
    queue.push(Rc::clone(&root));
    let mut sumSize: usize = 0;

    // Check all directories and find dirs with size at most 100_000.
    while (!queue.is_empty()) {
        let currentDir: Rc<RefCell<Item>> = queue.pop().unwrap();

        for x in currentDir.as_ref().borrow().files.iter() {
            // If is directory.
            if (x.borrow().files.len() > 0) {
                if (x.borrow().size <= 100_000) {
                    sumSize += x.borrow().size;
                }
                queue.push(Rc::clone(&x));
            }
        }
    }
    println!("Sum size: {}", sumSize);
}

fn part2(text: &String) {
    let root = calculateStructure(text);
    let totalDisk: usize = 70_000_000;
    let targetFree: usize = 30_000_000;
    let targetToFree: usize = targetFree - (totalDisk - root.as_ref().borrow().size);
    println!("Target to free: {}", targetToFree);

    let mut queue: Vec<Rc<RefCell<Item>>> = Vec::new();
    queue.push(Rc::clone(&root));
    let mut smallestSize: usize = root.as_ref().borrow().size;

    // Check all directories and find dirs with size at most 100_000.
    while (!queue.is_empty()) {
        let currentDir: Rc<RefCell<Item>> = queue.pop().unwrap();

        for x in currentDir.as_ref().borrow().files.iter() {
            // If is directory.
            if (x.borrow().files.len() > 0) {
                if (x.borrow().size < smallestSize && x.borrow().size >= targetToFree) {
                    smallestSize = x.borrow().size;
                }
                queue.push(Rc::clone(&x));
            }
        }
    }
    println!("Size to free: {}", smallestSize);
}

fn main() {
    let text: String = readToString("input.txt").expect("Bad file!");

    part1(&text);
    part2(&text);
}
