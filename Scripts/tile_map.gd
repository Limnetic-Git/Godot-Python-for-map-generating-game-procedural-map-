extends TileMap

const WATER_TILE = Vector2i(1, 1)
const LAND_TILE = Vector2i(2, 3)


func parse_2d_array(str_data: String) -> Array:
	#var result = []
	var json = JSON.new()
	
	var error = json.parse(str_data)
	if error != OK:
		push_error("Ошибка парсинга JSON: " + json.get_error_message())
		return []
	var parsed_data = json.get_data()
	if typeof(parsed_data) == TYPE_ARRAY:
		return _convert_numbers_to_int(parsed_data)
	else:
		push_error("Ожидался массив, получен: " + str(typeof(parsed_data)))
		return []

func _convert_numbers_to_int(data):
	if typeof(data) == TYPE_ARRAY:
		return data.map(func(x): return _convert_numbers_to_int(x))
	elif typeof(data) == TYPE_FLOAT and data == int(data):
		return int(data)  
	else:
		return data  

func run_python_script() -> Array:
	var output = []
	var exit_code = OS.execute("python3", ["GameMap/generator.py"], output, true)
	return output

func draw_world(world: Array, world_objects: Array):
	clear()
	set_cell(1, Vector2i(0, 0), 1, Vector2i(0, 0))
	#var terrain_set = 0  
	#var terrain = 0     
	for x in range(len(world)):
		for y in range(len(world[0])):
			#if world[x][y] == 0:
			set_cell(0, Vector2i(x, y), 0, Vector2i(world[x][y], 0))
	for x in range(len(world)):
		for y in range(len(world[0])):
			if world_objects[x][y] == 1:
				set_cell(1, Vector2i(x, y), 1, Vector2i(0, 0))
	#var cells = []
	#for x in range(len(world)):
	#	for y in range(len(world[0])):
	#		if world[x][y] != 0:
	#			cells.append(Vector2i(x, y))
	#set_cells_terrain_connect(0, cells, terrain_set, terrain)

func is_player_colliding_with_tree(
	player: Node2D, 
	tilemap: TileMap, 
	tree_atlas_coords: Vector2i, 
	tree_layer: int = 1, 
	tree_atlas_source_id: int = 1
	) -> bool:
	
	# Получаем клетку игрока
	var player_cell = tilemap.local_to_map(player.global_position)
	
	# Получаем данные тайла с указанием source_id (атласа)
	var tile_data = tilemap.get_cell_tile_data(tree_layer, player_cell)
	
	if tile_data:
		# Проверяем, что тайл из нужного атласа (source_id = 2)
		var source_id = tilemap.get_cell_source_id(tree_layer, player_cell)
		if source_id == tree_atlas_source_id:
			# Проверяем координаты в атласе
			var current_atlas_coords = tile_data.get_atlas_coords()
			if current_atlas_coords == tree_atlas_coords:
				# Проверка пересечения (опционально)
				var tile_pos = tilemap.map_to_local(player_cell)
				var player_rect = Rect2(player.global_position - Vector2(8, 8), Vector2(16, 16))
				var tile_texture = tile_data.tile_set.tile_get_texture(tile_data.get_cell_tile_data())
				var tile_rect = Rect2(tile_pos, tile_texture.get_size() if tile_texture else Vector2.ZERO)
				return player_rect.intersects(tile_rect)
	return false

func _ready():
	
	var data = run_python_script()[0]
	#print(data)
	var world = parse_2d_array(data)[0]
	var world_objects = parse_2d_array(data)[1]
	
	draw_world(world, world_objects)

func _physics_process(_delta: float) -> void:
	# Где-то в коде (например, в ready())
	var tree_coords = Vector2i(0, 0)  # Координаты тайла дерева в атласе

	# В physics_process()
	if is_player_colliding_with_tree($Player, $".", tree_coords, 1):
		print("Игрок касается дерева!")
