import raylibpy as rl
import copy

class Game:
    def __init__(self):
        rl.init_window(1600, 800, "test")
        rl.set_target_fps(60)

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

class Item:
    def __init__(self, name, rects):
        self.name = name
        self.rects = rects

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

        self.items = {"test_item_1" : Item("test_item_1", [rl.Rectangle(100, 150, 50, 50), rl.Rectangle(100, 200, 50, 50), rl.Rectangle(150, 150, 50, 50)]),
                      "test_item_2" : Item("test_item_2", [rl.Rectangle(100, 450, 50, 50), rl.Rectangle(100, 500, 50, 50), rl.Rectangle(150, 450, 50, 50)])}

        self.selected_item = None
        self.start_rects = []

    def move_selected_item(self, delta_x, delta_y):
        for item_one_rect in self.selected_item.rects:
            item_one_rect.x += delta_x * 50
            item_one_rect.y += delta_y * 50

        is_collided = False
        for wall_rect in self.pendnant_wall_rects:
            for item_one_rect in self.selected_item.rects:
                if rl.check_collision_recs(wall_rect, item_one_rect):
                    is_collided = True

        if is_collided:
            for item_one_rect in self.selected_item.rects:
                if delta_x > 0:
                    item_one_rect.x -= 50
                if delta_x < 0:
                    item_one_rect.x += 50
                        
                if delta_y > 0:
                    item_one_rect.y -= 50
                if delta_y < 0:
                    item_one_rect.y += 50

    def update(self):
        if not self.selected_item and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            for item in self.items.values():
                for item_one_rect in item.rects:
                    if rl.check_collision_point_rec(rl.get_mouse_position(), item_one_rect):
                        self.selected_item = item
                        self.start_rects = copy.deepcopy(item.rects)

        if self.selected_item:
            if rl.is_key_pressed(rl.KEY_W):
                self.move_selected_item(0, -1)
            if rl.is_key_pressed(rl.KEY_A):
                self.move_selected_item(-1, 0)
            if rl.is_key_pressed(rl.KEY_S):
                self.move_selected_item(0, 1)
            if rl.is_key_pressed(rl.KEY_D):
                self.move_selected_item(1, 0)

        if rl.is_key_pressed(rl.KEY_BACKSPACE):
            for item in self.items.values():
                if item == self.selected_item: 
                    continue
                for item_one_rect in item.rects:
                    for selected_item_one_rect in self.selected_item.rects:
                        if rl.check_collision_recs(item_one_rect, selected_item_one_rect):
                            self.selected_item.rects = copy.deepcopy(self.start_rects)  # 원래 자리로 복귀
                            self.selected_item = None  # 선택 아이템을 없앰
                            break  # 더 이상 루프를 돌 필요 없음
                    if self.selected_item is None:
                        break  # 내부 루프를 빠져나감
                if self.selected_item is None:
                    break  # 최상위 루프까지 빠져나감
                
            self.selected_item = None

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
        
        for item in self.items.values():
            for item_one_rect in item.rects:
                rl.draw_rectangle_rec(item_one_rect, rl.RED)

        if self.selected_item:
            rl.draw_text(self.selected_item.name, 970, 100, 40, rl.BLACK)

        rl.draw_fps(20, 20)

        rl.end_drawing()

if __name__ == "__main__":
    Game().run()