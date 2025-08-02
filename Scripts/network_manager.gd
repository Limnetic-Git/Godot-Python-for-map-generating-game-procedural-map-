extends Node

# Сигналы для UI (например, подключение/отключение игрока)
signal player_connected(peer_id, player_info)
signal player_disconnected(peer_id)

# Порт и максимальное число игроков
const PORT = 8910
const MAX_PLAYERS = 4

# Данные игроков (id: {name: "Игрок1", color: Color.RED})
var players = {}

# ENetMultiplayerPeer для сети
var peer = ENetMultiplayerPeer.new()

func _ready():
	# Автоматически обрабатывать RPC и ввод
	multiplayer.peer_connected.connect(_on_player_connected)
	multiplayer.peer_disconnected.connect(_on_player_disconnected)

# ==== Хостинг игры ====
func host_game(player_nickname):
	players[1] = {"name": player_nickname}  # Хост — peer_id = 1
	peer.create_server(PORT, MAX_PLAYERS)
	multiplayer.multiplayer_peer = peer
	print("Сервер запущен. Ожидание игроков...")

# ==== Подключение к игре ====
func join_game(ip, player_nickname):
	peer.create_client(ip, PORT)
	multiplayer.multiplayer_peer = peer
	players[multiplayer.get_unique_id()] = {"name": player_nickname}
	print("Подключение к ", ip)

# ==== Обработка подключений ====
func _on_player_connected(peer_id):
	print("Игрок подключен: ", peer_id)
	player_connected.emit(peer_id, players.get(peer_id, {}))

func _on_player_disconnected(peer_id):
	print("Игрок отключен: ", peer_id)
	players.erase(peer_id)
	player_disconnected.emit(peer_id)
