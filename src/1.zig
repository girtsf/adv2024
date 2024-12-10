const std = @import("std");
var gpa = std.heap.GeneralPurposeAllocator(.{}){};
const ally = gpa.allocator();

fn parseLists(text: []const u8) !struct { std.ArrayList(u32), std.ArrayList(u32) } {
    var list1 = std.ArrayList(u32).init(ally);
    var list2 = std.ArrayList(u32).init(ally);
    var it = std.mem.split(u8, text, "\n");
    while (it.next()) |line| {
        if (line.len == 0) {
            continue;
        }

        var it2 = std.mem.tokenizeScalar(u8, line, ' ');

        const s1 = it2.next() orelse {
            std.debug.panic("invalid line: '{s}'", .{line});
        };
        const int1 = std.fmt.parseInt(u32, s1, 10) catch {
            std.debug.panic("invalid number: '{s}'", .{s1});
        };
        try list1.append(int1);
        const s2 = it2.next() orelse {
            std.debug.panic("invalid line2: '{s}'", .{line});
        };
        const int2 = std.fmt.parseInt(u32, s2, 10) catch {
            std.debug.panic("invalid number2: '{s}', line: '{s}'", .{ s2, line });
        };

        try list2.append(int2);
    }
    return .{ list1, list2 };
}

fn part1(list1_in: []u32, list2_in: []u32) !u32 {
    const list1 = try ally.alloc(u32, list1_in.len);
    defer ally.free(list1);
    @memcpy(list1, list1_in);

    const list2 = try ally.alloc(u32, list2_in.len);
    defer ally.free(list2);
    @memcpy(list2, list2_in);

    std.mem.sort(u32, list1, {}, comptime std.sort.asc(u32));
    std.mem.sort(u32, list2, {}, comptime std.sort.asc(u32));

    var dist: u32 = 0;

    for (list1, list2) |n1, n2| {
        dist += if (n1 < n2) n2 - n1 else n1 - n2;
    }

    return dist;
}

fn part2(list1: []u32, list2: []u32) !u32 {
    var list2_map = std.hash_map.AutoHashMap(u32, u32).init(ally);
    defer list2_map.deinit();

    for (list2) |n| {
        if (list2_map.get(n)) |k| {
            try list2_map.put(n, k + 1);
        } else {
            try list2_map.put(n, 1);
        }
    }

    var score: u32 = 0;

    for (list1) |n| {
        if (list2_map.get(n)) |k| {
            score += n * k;
        }
    }

    return score;
}

pub fn main() !void {
    const args = try std.process.argsAlloc(ally);
    defer std.process.argsFree(ally, args);

    if (args.len != 2) {
        @panic("no input file");
    }
    const text = try std.fs.cwd().readFileAlloc(ally, args[1], 1_000_000);
    defer ally.free(text);
    var list1, var list2 = try parseLists(text);
    defer list1.deinit();
    defer list2.deinit();

    const part1_result = try part1(list1.items, list2.items);
    std.debug.print("part 1: {d}\n", .{part1_result});

    const part2_result = try part2(list1.items, list2.items);
    std.debug.print("part 2: {d}\n", .{part2_result});
}
