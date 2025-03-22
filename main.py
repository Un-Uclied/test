import raylibpy as rl

class Game:
    def __init__(self):
        rl.init_window(1900, 800, "test")

        self.scenes = {
            "main_game" : MainGameScene(self)
        }

        self.current_scene = self.scenes["main_game"]

        self.time_scale = 1
        self.delta_time = 0

    def run(self):
        while not rl.window_should_close():
            self.time_scale = rl.get_frame_time() * self.time_scale

            self.current_scene.update()
            self.current_scene.draw()

        rl.close_window()


class MainGameScene:
    def __init__(self, game : Game):
        self.game = game

        self.camera = rl.Camera2D(rl.Vector2(rl.get_screen_width() / 2, rl.get_screen_height() / 2), rl.Vector2(), 0, 1)

    def update(self):
        pass

    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLANK)
        rl.begin_mode2d(self.camera)
        #world render

        rl.end_mode2d()
        #ui render
        rl.draw_rectangle_rec(rl.Rectangle(0, 0, 100, 100), rl.RED)
        rl.end_drawing()
if __name__ == "__main__":
    Game().run()