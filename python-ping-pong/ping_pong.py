"""A simple two-player Ping-Pong game built with Python's turtle module."""

from __future__ import annotations

import turtle


WIDTH = 900
HEIGHT = 600
PADDLE_STEP = 30
WINNING_SCORE = 10


class PingPongGame:
    """Coordinate the screen, paddles, ball, scoring, and controls."""

    def __init__(self) -> None:
        self.screen = turtle.Screen()
        self.screen.title("Python Ping-Pong")
        self.screen.bgcolor("#101820")
        self.screen.setup(width=WIDTH, height=HEIGHT)
        self.screen.tracer(0)

        self.left_score = 0
        self.right_score = 0
        self.running = True

        self.left_paddle = self._make_paddle(-WIDTH // 2 + 50)
        self.right_paddle = self._make_paddle(WIDTH // 2 - 60)
        self.ball = self._make_ball()
        self.scoreboard = self._make_writer(0, HEIGHT // 2 - 70, 28)
        self.message = self._make_writer(0, 0, 24)

        self._draw_center_line()
        self._bind_controls()
        self._update_scoreboard()

    @staticmethod
    def _make_writer(x: int, y: int, size: int) -> turtle.Turtle:
        writer = turtle.Turtle(visible=False)
        writer.color("white")
        writer.penup()
        writer.goto(x, y)
        writer.font_size = size
        return writer

    @staticmethod
    def _make_paddle(x: int) -> turtle.Turtle:
        paddle = turtle.Turtle("square")
        paddle.color("white")
        paddle.penup()
        paddle.shapesize(stretch_wid=5, stretch_len=1)
        paddle.goto(x, 0)
        return paddle

    @staticmethod
    def _make_ball() -> turtle.Turtle:
        ball = turtle.Turtle("circle")
        ball.color("#f2aa4c")
        ball.penup()
        ball.dx = 5
        ball.dy = 4
        return ball

    def _draw_center_line(self) -> None:
        line = turtle.Turtle(visible=False)
        line.color("#66727c")
        line.penup()
        line.goto(0, -HEIGHT // 2)
        line.setheading(90)
        for _ in range(15):
            line.pendown()
            line.forward(20)
            line.penup()
            line.forward(20)

    def _bind_controls(self) -> None:
        self.screen.listen()
        self.screen.onkeypress(lambda: self._move(self.left_paddle, PADDLE_STEP), "w")
        self.screen.onkeypress(lambda: self._move(self.left_paddle, -PADDLE_STEP), "s")
        self.screen.onkeypress(lambda: self._move(self.right_paddle, PADDLE_STEP), "Up")
        self.screen.onkeypress(lambda: self._move(self.right_paddle, -PADDLE_STEP), "Down")
        self.screen.onkeypress(self.restart, "r")
        self.screen.onkeypress(self.quit, "Escape")

    @staticmethod
    def _move(paddle: turtle.Turtle, distance: int) -> None:
        limit = HEIGHT // 2 - 60
        paddle.sety(max(-limit, min(limit, paddle.ycor() + distance)))

    def _update_scoreboard(self) -> None:
        self.scoreboard.clear()
        self.scoreboard.write(
            f"{self.left_score}     {self.right_score}",
            align="center",
            font=("Arial", self.scoreboard.font_size, "bold"),
        )

    def _reset_ball(self, direction: int) -> None:
        self.ball.goto(0, 0)
        self.ball.dx = 5 * direction
        self.ball.dy = 4 if self.ball.dy >= 0 else -4

    def _score_point(self, left_player: bool) -> None:
        if left_player:
            self.left_score += 1
            self._reset_ball(1)
        else:
            self.right_score += 1
            self._reset_ball(-1)
        self._update_scoreboard()

        if max(self.left_score, self.right_score) >= WINNING_SCORE:
            winner = "Left player" if self.left_score > self.right_score else "Right player"
            self.running = False
            self.message.write(
                f"{winner} wins!\nPress R to restart or Esc to quit",
                align="center",
                font=("Arial", self.message.font_size, "bold"),
            )

    def _handle_wall_collision(self) -> None:
        vertical_limit = HEIGHT // 2 - 20
        if self.ball.ycor() > vertical_limit:
            self.ball.sety(vertical_limit)
            self.ball.dy *= -1
        elif self.ball.ycor() < -vertical_limit:
            self.ball.sety(-vertical_limit)
            self.ball.dy *= -1

    def _handle_paddle_collision(self) -> None:
        for paddle, moving_toward in (
            (self.right_paddle, self.ball.dx > 0),
            (self.left_paddle, self.ball.dx < 0),
        ):
            if moving_toward and self.ball.distance(paddle) < 55:
                horizontal_gap = abs(self.ball.xcor() - paddle.xcor())
                if horizontal_gap < 25:
                    self.ball.dx *= -1.05
                    self.ball.dy += (self.ball.ycor() - paddle.ycor()) * 0.04
                    self.ball.setx(paddle.xcor() - (25 if paddle is self.right_paddle else -25))

    def restart(self) -> None:
        self.left_score = 0
        self.right_score = 0
        self.running = True
        self.message.clear()
        self._update_scoreboard()
        self._reset_ball(1)

    def quit(self) -> None:
        self.screen.bye()

    def game_loop(self) -> None:
        if self.running:
            self.ball.setx(self.ball.xcor() + self.ball.dx)
            self.ball.sety(self.ball.ycor() + self.ball.dy)
            self._handle_wall_collision()
            self._handle_paddle_collision()

            if self.ball.xcor() > WIDTH // 2:
                self._score_point(left_player=True)
            elif self.ball.xcor() < -WIDTH // 2:
                self._score_point(left_player=False)

        self.screen.update()
        self.screen.ontimer(self.game_loop, 16)

    def run(self) -> None:
        self.game_loop()
        self.screen.mainloop()


if __name__ == "__main__":
    PingPongGame().run()
