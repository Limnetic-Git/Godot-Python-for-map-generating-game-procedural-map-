extends CharacterBody2D

@export var speed: float = 100.0
@onready var animation_player = $AnimatedSprite2D
#@onready var sprite = $Sprite2D

func _physics_process(_delta: float) -> void:
	var input_direction = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	input_direction = input_direction.normalized()
	velocity = input_direction * speed

	if input_direction != Vector2.ZERO:
		if abs(input_direction.x) > abs(input_direction.y):
			if input_direction.x > 0:
				animation_player.play("Run_D")
			else:
				animation_player.play("Run_A")
		else:
			if input_direction.y > 0:
				animation_player.play("Run_S")
			else:
				animation_player.play("Run_W")
	else:
		animation_player.play("Idle")
	
	move_and_slide()
	
