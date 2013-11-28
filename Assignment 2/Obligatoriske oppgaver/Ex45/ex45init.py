import ex45main
import ex45routecontrol
import ex45encounter1
import ex45scene

a_map = ex45routecontrol.Map('first_encounter')
a_game = ex45main.GameMain(a_map)
a_game.play()