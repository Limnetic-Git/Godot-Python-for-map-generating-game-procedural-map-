extends TileMapLayer

	
func parse_2d_array(str_data: String) -> Array:
	var result = []
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

func run_python_script():
	var output = []
	var exit_code = OS.execute("python", ["GameMap/generator.py"], output, true)
	return output
func _ready():
	var data = run_python_script()[0]
	var array = parse_2d_array(data)[0]
	print(array)
