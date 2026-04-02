extends Control

@onready var color_bg: ColorRect = $ColorRect
@onready var texture_bg: TextureRect = $TextureRect
@onready var texture_ch: TextureRect = $TextureRect2

# Variables para controlar la línea de tiempo
var timeline_data: Array = []
var current_time: float = 0.0
var current_frame_index: int = -1 # Empezamos en -1 para forzar la carga del primer frame


func _ready() -> void:
	# 1. Obtener argumentos
	var argumentos = OS.get_cmdline_user_args()
	if argumentos.size() > 0:
		var ruta_json = argumentos[0]
		_load_json(ruta_json)
	else:
		print("Error: No se proporcionó ninguna ruta de JSON en los argumentos.")
		var ruta_json = "./../lip_sync.json"
		_load_json(ruta_json)

# Función para leer y parsear el JSON
func _load_json(path: String) -> void:
	if FileAccess.file_exists(path):
		var file = FileAccess.open(path, FileAccess.READ)
		var json_text = file.get_as_text()
		var json = JSON.new()
		var error = json.parse(json_text)
		
		if error == OK:
			timeline_data = json.data
			print("JSON cargado con éxito. Total de frames: ", timeline_data.size())
		else:
			print("Error al parsear el JSON en la línea: ", json.get_error_line())
	else:
		print("El archivo JSON no existe en la ruta proporcionada: ", path)

func _process(delta: float) -> void:
	# Si no hay datos cargados, no hacemos nada
	if timeline_data.is_empty():
		return
		
	# Acumular el tiempo (fuera de la variable local para que no se reinicie)
	current_time += delta
	
	# Determinar cuál es el índice del próximo frame
	var next_index = current_frame_index + 1
	
	# Revisamos si es hora de avanzar al siguiente frame del JSON
	while next_index < timeline_data.size() and current_time >= timeline_data[next_index][0]:
		current_frame_index = next_index
		_apply_frame(timeline_data[current_frame_index])
		next_index += 1
		
	# FINALIZAR LA PELÍCULA
	# Cuando usas --write-movie, el motor grabará infinitamente.
	# Debes cerrar el árbol (quit) para que el .avi se guarde correctamente.
	if current_frame_index == timeline_data.size() - 1:
		# Añadimos un pequeño margen de 0.1 segundos extra al final para que renderice el último frame
		if current_time > timeline_data[current_frame_index][0] + 0.1:
			print("Animación terminada. Cerrando para guardar el video...")
			get_tree().quit()
	
	if current_time > 600:
		get_tree().quit()

# Función que actualiza los nodos visuales
func _apply_frame(frame_data: Array) -> void:
	# Estructura esperada: [0.09, "none_03", "#fff"]
	print(frame_data[0])
	var tex_name: String = frame_data[1]
	print(tex_name)
	var color_hex: String = frame_data[2]
	print(color_hex)
	
	# 1. Actualizar Color de Fondo
	color_bg.color = Color(color_hex)
	
	# 2. Actualizar Textura (Boca/Personaje)
	# Construimos la ruta completa, por ejemplo: "res://assets/ch/none_04.png"
	var tex_path: String = "res://assets/ch/" + tex_name + ".png" 
	print("-> ", tex_path)
	var tex: Texture2D = load(tex_path)
	if tex != null:
		texture_ch.texture = tex
