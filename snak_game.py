from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
import random

# Set a fixed size for desktop testing (Android will auto-adjust)
Window.clearcolor = (0, 0, 0, 1)
# Window.size = (400, 600)

class RoadGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size

        self.speed = 5
        self.road_lines = []
        self.coins = []
        self.obstacles = []
        self.move_direction = 0
        self.game_over = False
        self.score = 0

        # Load images (ensure these files exist in your project folder)
        self.car_image = CoreImage('car.png').texture
        self.coin_image = CoreImage('coin.png').texture
        self.obstacle_image = CoreImage('obstacle.png').texture

        with self.canvas:
            # Road lines
            for y in range(0, Window.height, 70):
                Color(1, 1, 1)
                rect = Rectangle(pos=(Window.width / 2 - 5, y), size=(10, 40))
                self.road_lines.append(rect)

            # Player car
            self.car_width = 70
            self.car_height = 120
            self.car_x = Window.width / 2 - self.car_width / 2
            self.car_y = 50
            self.car = Rectangle(texture=self.car_image, pos=(self.car_x, self.car_y),
                                 size=(self.car_width, self.car_height))

            # Coins
            for _ in range(5):
                x = random.randint(100, 300)
                y = random.randint(300, 1000)
                coin = Rectangle(texture=self.coin_image, pos=(x, y), size=(50, 50))
                self.coins.append(coin)

            # Obstacles
            for _ in range(3):
                x = random.randint(100, 300)
                y = random.randint(600, 1200)
                obs = Rectangle(texture=self.obstacle_image, pos=(x, y), size=(80, 80))
                self.obstacles.append(obs)

        # Score Label
        self.score_label = Label(
            text=f"Score: {self.score}",
            font_size=24,
            size_hint=(None, None),
            size=(200, 50),
            pos=(10, Window.height - 60),
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.score_label)

        # Game Over Label
        self.game_over_label = Label(
            text="",
            font_size=32,
            size_hint=(None, None),
            size=(400, 120),
            pos=(Window.width / 2 - 200, Window.height / 2 - 60),
            color=(1, 0, 0, 1)
        )

        self.add_widget(self.game_over_label)
        self.game_over_label.opacity = 0

        # Schedule game updates
        Clock.schedule_interval(self.update, 1 / 60)
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)
        self.bind(on_touch_move=self.on_touch_move)

    def update(self, dt):
        if self.game_over:
            return

        # Move road lines
        for rect in self.road_lines:
            x, y = rect.pos
            y -= self.speed
            if y + 40 < 0:
                y = Window.height
            rect.pos = (x, y)

        # Move car
        self.car_x += self.move_direction * 6
        self.car_x = max(0, min(Window.width - self.car_width, self.car_x))
        self.car.pos = (self.car_x, self.car_y)

        # Move coins
        for coin in self.coins:
            x, y = coin.pos
            y -= self.speed
            if y < -30:
                y = Window.height + random.randint(0, 500)
                x = random.randint(50, Window.width - 50)
            coin.pos = (x, y)

            # Collision with car
            if self.check_collision(self.car, coin):
                self.score += 1
                self.score_label.text = f"Score: {self.score}"
                y = Window.height + random.randint(0, 500)
                x = random.randint(50, Window.width - 50)
                coin.pos = (x, y)

        # Move obstacles
        for obs in self.obstacles:
            x, y = obs.pos
            y -= self.speed
            if y < -50:
                y = Window.height + random.randint(0, 500)
                x = random.randint(50, Window.width - 50)
            obs.pos = (x, y)

            # Collision
            if self.check_collision(self.car, obs):
                self.end_game()

    def check_collision(self, rect1, rect2):
        x1, y1 = rect1.pos
        w1, h1 = rect1.size
        x2, y2 = rect2.pos
        w2, h2 = rect2.size
        return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )

    def end_game(self):
        self.game_over = True
        self.game_over_label.text = f"GAME OVER\nFinal Score: {self.score}"
        self.game_over_label.opacity = 1
        print(f"💥 Game Over! Final Score: {self.score}")


    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 276:
            self.move_direction = -1
        elif key == 275:
            self.move_direction = 1

    def on_key_up(self, window, key, scancode):
        if key in (276, 275):
            self.move_direction = 0

    def on_touch_move(self, instance, touch):
        if not self.game_over:
            self.car_x = touch.x - self.car_width / 2
            self.car_x = max(0, min(Window.width - self.car_width, self.car_x))
            self.car.pos = (self.car_x, self.car_y)

class CarGameApp(App):
    def build(self):
        return RoadGame()

if __name__ == "__main__":
    CarGameApp().run()
