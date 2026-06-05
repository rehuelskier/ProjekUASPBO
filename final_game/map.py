import pygame
from zombie import ZombieHorizontal,ZombieVertical
from rock import Rock,Coin
from obstacle import Exit,Bush,Wall,SwitchDoor,KeyDoor,Checkpoint,Switch,Treasure

TILE = 40

stage_1 = [
"############################################",
"######################################.....#",
"############O##.G...Z........c.O....#..#O#.#",
"##########..b...##################CC#..#O#.#",
"##########.z....##################Cb#..#O#.#",
"######...#.......#########........Ob#..#O#.#",
"######.T.-...z..cG.#######CC#########..#O#.#",
"##########y#CC..##.....###bC#########..#O#.#",
"####################...###bO........#...O..#",
"###############C####...###########CC##.#T#.#",
"#####..CCO##OObbb#bbO..###########Cb##.###.#",
".1Pc..CCCbb#ObbCbbbOOO.######.....Ob##.....#",
"#########ObCb################..##########..#",
"##########bCb###############bbO#.########..#",
"###########CbO############..bO##.gc........#",
"############bb.###########F.Cb...###.....###",
"#############O..####################.....###",
"##############O.C############F....##.....###",
"###############.b.############.....#.....###",
"################b....#.T######.....#.....###",
"#################....D.#######.....G......gE",
"###################Y########################",
"############################################",
"############################################",
"############################################",


]

stage_2 = [
"############################################",
"E........Z....##############################",
"###OOC##########.........###################",
"##.bb##..C..####C........###################",
"#O.C##...Cb...####C......##O.O.O..##########",
"#b.##...b.O...####C......##bzb.bz.##########",
"#.##....bCb....####....OO##...zZ.Z##########",
"#.#....#CbCb...####....bb....C...C##########",
"#.#...##bbCb...####....######T#C#T##########",
"#.#.......bO...####....#####################",
"#O#........b...####....###.OOOO....2....####",
"#O#........O.....##....###.bbbb...q#..F.####",
"#b-.y###...b.....cg....GGG........##########",
"#.###..........####....#####################",
"#.###.O..#.....######OC#####################",
"#####################OC#####################",
"#####################Ob#####################",
"#####################bOO####################",
"#####################Tbb..Z.c....#########",
"#################################.##########",
"############################..zz.O.#########",
"####.O.OOCO...bOb.CCC...###......b.#########",
"####.bCbCCb...bOb.bCb.T.###.......Z#########",
"####..bb##bCC.bOb.bCb######.....Z..#########",
"####......bbbbbbb..b....######.....#########",
"####....bCb..O..........#######....#########",
"####.....C...b..........#....####..#########",
"####...b.b.C...b......Y.Dc...####C.#########",
"####...Cbb.b...#.....#######bb####.#########",
"####..bbCCbC.bb#.....#######bOb###.#########",
"1Pc...CCbbbbbCC#############CO..G..#########",
"############################################",
"############################################",

]
stage_3 = [
"############################################",
"##.O.#....OC..OC...Dc..#####################",
"#.OOO.c...bb..bb...#...#####################",
"#.bbb#..O..........#...###########....######",
"#.####..b..........#...########CO#..bO######",
"#c..###...C.#.....#.....##....ObO...bC######",
"##...##.CCb.#.....#.....##.#.##.#.CCC#OO###",
"###...#.bC..#.....#.....##.#.##.##CC#.bb...#",
"####..O#.b..#....#....Z..#.#.##.##b#####...#",
"#####bO#....#....#..###..#.....O.....##OO..#",
"#####bO#....#....#..###..##########..##Cb..#",
"#####bOO#...#...#..Z###Z..#######....##b...#",
"#..T##Ob#...#...#...###...######....####...#",
"#Z.###OO#.......#.#######.#####....####..C##",
"#....Gbb##.....#....O......###....###....###",
"#C...#.z##.....#..###.###..##....###..q.####",
"##...bb###..Y..#z...#.#...z##.O.###...######",
"##....#####.#.###.#.#.#.#.###c#..-c....2gg.E",
"##....####b...b#O.#F#T#F#..GG.#by###########",
"1Pc.CC####b...b#T.##########################",
"############################################",
"############################################",

]

stage_0 = [
    "############################################",
    "############################################",
    "############################################",
    "############################################",
    "###.O.###...OO.T############################",
    "###.#.###...bb###.z.########################",
    ".1P....Dc...CC.G.....E######################",
    "######Y#####################################",
    "############################################",
    "############################################",
]

all_maps = [
    stage_1,
    stage_2,
    stage_3,
    stage_0
]

def load_map(map_data):

    bushes = []
    walls = []
    zombies = []
    rocks = []
    traps = []
    switch_doors = []
    key_doors =[]
    switches = []
    coins = []
    treasures = []
    checkpoints = []
    player_spawn = (0,0)
    exit_door = None

    for y,row in enumerate(map_data):
        for x,tile in enumerate(row):

            world_x = x*TILE
            world_y = y*TILE

            if tile == "#":
                walls.append(Wall(world_x,world_y))

            elif tile =="b":
                bushes.append(Bush(world_x,world_y))

            elif tile == "C":
                coins.append(Coin(world_x,world_y))

            elif tile == "Z":
                zombies.append(ZombieHorizontal(world_x,world_y))

            elif tile == "z":
                zombies.append(ZombieVertical(world_x,world_y))

            elif tile == "O":
                rocks.append(Rock(world_x,world_y))

            elif tile == "S":
                traps.append(pygame.Rect(world_x,world_y,TILE,TILE))

            elif tile == "P":
                player_spawn = (world_x,world_y)

            elif tile == "G":
                key_doors.append(KeyDoor(world_x,world_y,1))

            elif tile == "g":
                key_doors.append(KeyDoor(world_x,world_y,2))

            elif tile == "D":
                switch_doors.append(SwitchDoor(world_x,world_y,1))

            elif tile == "2":
                switch_doors.append(SwitchDoor(world_x,world_y,3))

            elif tile == "1":
                switch_doors.append(SwitchDoor(world_x,world_y,0))

            elif tile == "-":
                switch_doors.append(SwitchDoor(world_x,world_y,2))

            elif tile == "Y":
                switches.append(Switch(world_x, world_y,1))

            elif tile == "y":
                switches.append(Switch(world_x, world_y,2))

            elif tile == "q":
                switches.append(Switch(world_x, world_y,3))

            elif tile == "T":
                treasures.append(Treasure(world_x,world_y,1))

            elif tile == "F":
                treasures.append(Treasure(world_x,world_y,2))

            elif tile == "c":
                checkpoints.append(Checkpoint(world_x,world_y))

            elif tile == "E":
                exit_door = Exit(world_x,world_y)

        # PAIRING SWITCH - DOOR (ONLY ONCE)
    door_map = {door.door_id: door for door in switch_doors}

    for switch in switches:
        switch.door = door_map.get(switch.door_id)


    return walls,bushes,zombies,coins,traps,rocks,player_spawn,switch_doors,key_doors,switches,treasures,checkpoints,exit_door