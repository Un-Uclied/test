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

import raylibpy as rl

class Item:
    def __init__(self, name, rects):
        self.name = name
        self.rects = rects  # 아이템을 이루는 블록들의 위치 리스트
        self.rotation = 0

    def rotate(self, clockwise=True):
        if clockwise:
            self.rotation = (self.rotation + 90) % 360
        else:
            self.rotation = (self.rotation - 90) % 360

        """아이템을 시계(E) 또는 반시계(Q) 방향으로 회전"""
        # 아이템의 중심 좌표 구하기
        min_x = min(rect.x for rect in self.rects)
        min_y = min(rect.y for rect in self.rects)
        max_x = max(rect.x for rect in self.rects)
        max_y = max(rect.y for rect in self.rects)
        
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        new_rects = []
        for rect in self.rects:
            # 현재 좌표를 중심 기준 상대 좌표로 변환
            rel_x = rect.x - center_x
            rel_y = rect.y - center_y
            
            # 회전 공식 적용
            if clockwise:
                new_x = center_x + rel_y  # 시계 방향 회전 (E 키)
                new_y = center_y - rel_x
            else:
                new_x = center_x - rel_y  # 반시계 방향 회전 (Q 키)
                new_y = center_y + rel_x

            # 새 좌표로 변경
            new_rects.append(rl.Rectangle(new_x, new_y, rect.width, rect.height))

        # 회전된 위치 적용
        self.rects = new_rects
    

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

        # 아이템 회전 (Q: 반시계, E: 시계)
        if rl.is_key_pressed(rl.KEY_E) and not self.selected_item is None:
            self.selected_item.rotate(clockwise=False)
        if rl.is_key_pressed(rl.KEY_Q) and not self.selected_item is None:
            self.selected_item.rotate(clockwise=True)

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

        if not self.selected_item is None:
            rl.draw_text(self.selected_item.name, 970, 100, 40, rl.BLACK)
            rl.draw_text(f"rotation : {self.selected_item.rotation}", 970, 150, 40, rl.BLACK)

        rl.draw_fps(20, 20)

        rl.end_drawing()

if __name__ == "__main__":
    Game().run()