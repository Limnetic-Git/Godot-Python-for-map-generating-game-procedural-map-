import random, math

    
def neibs(x, y, world):
    a = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                pass
            else:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(world) and 0 <= ny < len(world[0]):
                    if world[nx][ny] != world[x][y]:
                        a += 1
    return a

def scale_water(world):
    step_world = [[1 for i in range(len(world))] for j in range(len(world))]
    for x in range(len(world)):
        for y in range(len(world)):
            if world[x][y] != 0:
                bioms_near = [world[x - 1][y], world[x + 1][y], world[x][y + 1], world[x][y - 1]]
                if 0 in bioms_near:
                    step_world[x][y] = 0
    for x in range(len(world)):
        for y in range(len(world)):
            if step_world[x][y] == 0:
                world[x][y] = 0
                
def resize_array(world, scale):
    scaled_vertically = []
    for row in world:
        for _ in range(scale):
            scaled_vertically.append(row.copy())

    scaled_horizontally = []
    for row in scaled_vertically:
        new_row = []
        for item in row:
            new_row.extend([item] * scale)
        scaled_horizontally.append(new_row)
    
    return scaled_horizontally


def most_common_element(arr):
    if not arr:
        return None
    frequency = {}
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
    return max(frequency.items(), key=lambda x: x[1])[0]

def generate_bioms(world, number):
    bioms_to_gen = [2, 2, 3, 4]
    for i in range(number):
        rx, ry = random.randint(0, len(world)-1), random.randint(0, len(world)-1)
        while world[rx][ry] != 1: rx, ry = random.randint(0, len(world)-1), random.randint(0, len(world)-1)
        world[rx][ry] = random.randint(2, 4)
        if number == len(bioms_to_gen):
            world[rx][ry] = bioms_to_gen[i]
        
    for _ in range(200):
        step_world = [[0 for i in range(len(world))] for j in range(len(world))]
        for x in range(len(world)):
            for y in range(len(world)):
                if world[x][y] == 1:
                    bioms_near = [world[x - 1][y], world[x + 1][y], world[x][y - 1], world[x][y + 1]]
                    if max(bioms_near) >= 2:
                        wanted_bioms = []
                        for i in range(len(bioms_near)):
                            if bioms_near[i] >= 2: wanted_bioms.append(bioms_near[i])
                        if random.randint(1, 100) <= 60:
                            step_world[x][y] = most_common_element(wanted_bioms)
        for x in range(len(world)):
            for y in range(len(world)):
                if step_world[x][y] != 0:
                    world[x][y] = step_world[x][y]
                    
                    
def generate_beach(world):

    step_world = [[0 for i in range(world_size)] for j in range(world_size)]
    for x in range(len(world)):
        for y in range(len(world)):
            if world[x][y] != 0:
                bioms_near = [world[x - 1][y], world[x + 1][y], world[x][y + 1], world[x][y - 1]]
                if 0 in bioms_near:
                    step_world[x][y] = 5
    for x in range(len(world)):
        for y in range(len(world)):
            if step_world[x][y] == 5:
                world[x][y] = 5      
    for i in range(2):

        step_world = [[0 for i in range(world_size)] for j in range(world_size)]
        for x in range(len(world)):
            for y in range(len(world)):
                if world[x][y] != 0:
                    bioms_near = [world[x - 1][y], world[x + 1][y], world[x][y + 1], world[x][y - 1]]
                    if 5 in bioms_near:
                        step_world[x][y] = 5
        for x in range(len(world)):
             for y in range(len(world)):
                if step_world[x][y] == 5:
                    world[x][y] = 5
            
def generate_rivers(world):
    step_world = world.copy()
    for x in range(len(world)):
        for y in range(len(world)):
            if world[x][y] != 0:
                bioms_near = [world[x - 1][y], world[x + 1][y], world[x][y + 1], world[x][y - 1]]
                wanted_bioms = []
                for i in range(len(bioms_near)):
                    if bioms_near[i] >= 2:
                        if not bioms_near[i] in wanted_bioms:
                            wanted_bioms.append(bioms_near[i])
                if len(wanted_bioms) > 1:
                    step_world[x][y] = 0
    world = step_world.copy()
            
def smoothing(world):
    step_world = world.copy()
    for x in range(len(world)):
        for y in range(len(world)):
            n = neibs(x, y, world)
            if n >= 5:
                step_world[x][y] = (0 if world[x][y] == 1 else 1)
    world = step_world.copy()
    
def bioms_smoothing(world):
    step_world = world.copy()
    for x in range(len(world)):
        for y in range(len(world)):
            if world[x][y] != 0:
                bioms_near = [world[x - 1][y], world[x + 1][y], world[x][y + 1], world[x][y - 1], world[x - 1][y - 1], world[x - 1][y + 1], world[x + 1][y - 1], world[x + 1][y + 1]]
                for i in range(len(bioms_near)):
                    if bioms_near[i] == 0:
                        bioms_near[i] = world[x][y]
                n = neibs(x, y, world)
                if n >= 5:
                    step_world[x][y] = most_common_element(bioms_near)
    world = step_world.copy()

def reset_bioms(world):
    for x in range(len(world)):
        for y in range(len(world)):
            if world[x][y] >= 2:
                world[x][y] = 1

def generate_land(world):
    world_center_x, world_center_y = len(world) // 2, len(world) // 2

    for x in range(len(world)):
        for y in range(len(world)):
            dist = math.hypot(x - world_center_x, y - world_center_y)
            max_chance = math.hypot(0 - world_center_x, 0 - world_center_y)
            land_chance = max_chance - dist
            if random.randint(0, int(max_chance)) <= int(land_chance):
                world[x][y] = 1
            
    for x in range(len(world)):
        for y in range(len(world)):
            dist = math.hypot(x - world_center_x, y - world_center_y)
            if dist <= 25:
                world[x][y] = 1
    for i in range(len(world)):
        world[i][0] = 0
        world[0][i] = 0
        world[i][len(world)-1] = 0
        world[len(world)-1][i] = 0
        
        
def generate_world(seed):
    random.seed(seed)
    world = [[0 for i in range(world_size)] for j in range(world_size)]
    generate_land(world)
    for _ in range(15):
        smoothing(world)
    
    world_without_rivers = eval(str(world.copy()))
    generate_bioms(world_without_rivers, 4)
    generate_beach(world_without_rivers)
    
    generate_bioms(world, 10)
    generate_rivers(world)
    reset_bioms(world)
    scale_water(world)
#    world = resize_array(world, 2)
    for _ in range(15):
        smoothing(world)

    for x in range(len(world)):
        for y in range(len(world)):
            if world[x][y] == 0:
                world_without_rivers[x][y] = 0
    world = world_without_rivers
    bioms_smoothing(world)

#    generate_bioms(world, 10)
    return world


world_size = 256
biom_colors = {'0': 'blue',
              '1': 'black',
              '2': 'dark green',
              '3': 'yellow',
              '4': 'white',
              '5': (150, 150, 20)
             }

seed = random.randint(0, 100000)
world = generate_world(seed)

# Открываем файл для записи (если файла нет - он создастся)
with open('map.json', 'w', encoding='utf-8') as file:
    file.write(str(world))
