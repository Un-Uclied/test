import raylibpy as rl

class Game:
    def __init__(self):
        rl.init_window(1600, 800, "test")

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

        self.tile_size = 50
        self.backpack_rects = [[] for i in range(10)]
        for y in range(10):
            for x in range(10):
                self.backpack_rects[y].append(rl.Rectangle(x * 50 + 100, y * 50 + 150, 50, 50))

    def update(self):
        pass

    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLANK)
        rl.begin_mode2d(self.camera)
        #world render

        rl.end_mode2d()
        #ui render
        rl.draw_rectangle_rec(rl.Rectangle(50, 0, 600, rl.get_screen_height()), rl.BROWN)

        rl.draw_rectangle_rec(rl.Rectangle(rl.get_screen_width() - 600 - 50, 0, 600, rl.get_screen_height()), rl.WHITE)
        for y in range(10):
            for x in range(10):
                rl.draw_rectangle_rec(self.backpack_rects[y][x], rl.GREEN)
        for y in range(9):
            for x in range(9):
                rl.draw_line(x * 50 + 100, y * 50 + 200, x * 50 + 100 + 100, y * 50 + 200, rl.RED)
                rl.draw_line(x * 50 + 150, y * 50 + 150, x * 50  + 150, y * 50 + 100 + 150, rl.RED)
            
        rl.end_drawing()
if __name__ == "__main__":
    Game().run()