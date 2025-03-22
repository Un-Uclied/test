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

        self.pendant_rects = [[] for i in range(10)]
        for y in range(10):
            for x in range(10):
                self.pendant_rects[y].append(rl.Rectangle(x * 50 + 100, y * 50 + 150, 50, 50))

        self.pendnant_wall_rects = [
            rl.Rectangle(100, 100, 450, 50),
            rl.Rectangle(50, 150, 50, 500),
            rl.Rectangle(550, 150, 50, 500),
            rl.Rectangle(100, 650, 450, 50)
        ]

        self.selected_item = rl.Rectangle(50, 50, 50, 50)

    def move_selected_item(self, delta_x, delta_y):
        self.selected_item.x += delta_x * 50
        self.selected_item.y += delta_y * 50

    def update(self):
        if rl.is_key_pressed(rl.KEY_W):
            self.move_selected_item(0, 1)
        if rl.is_key_pressed(rl.KEY_A):
            self.move_selected_item(-1, 0)
        if rl.is_key_pressed(rl.KEY_S):
            self.move_selected_item(0, -1)
        if rl.is_key_pressed(rl.KEY_D):
            self.move_selected_item(1, 0)

    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLANK)
        rl.begin_mode2d(self.camera)
        #world render

        rl.end_mode2d()
        #ui render
        
        #backpack bg
        rl.draw_rectangle_rec(rl.Rectangle(50, 0, 550, rl.get_screen_height()), rl.BROWN)

        #inventory bg
        rl.draw_rectangle_rec(rl.Rectangle(rl.get_screen_width() - 600 - 50, 0, 600, rl.get_screen_height()), rl.WHITE)

        #draw backpack rects
        for y in range(10):
            for x in range(10):
                rl.draw_rectangle_rec(self.pendant_rects[y][x], rl.GREEN)

        #draw lines
        for y in range(9):
            for x in range(9):
                rl.draw_line(x * 50 + 100, y * 50 + 200, x * 50 + 100 + 100, y * 50 + 200, rl.RED)
                rl.draw_line(x * 50 + 150, y * 50 + 150, x * 50  + 150, y * 50 + 100 + 150, rl.RED)
        
        for rects in self.pendnant_wall_rects:
            rl.draw_rectangle_rec(rects, rl.BLUE)

        rl.draw_fps(20, 20)

        rl.end_drawing()

if __name__ == "__main__":
    Game().run()