extends Area2D

func _on_area_entered(area):
	if area.is_in_group("tree"):
		area.modulate.a = 0.5

func _on_area_exited(area):
	if area.is_in_group("tree"):
		area.modulate.a = 1.0
