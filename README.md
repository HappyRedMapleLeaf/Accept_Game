# "Accept"
A short top-down point-and-click story game following Freddie's journey towards university acceptance, submitted in June 2022 as the final assignment for my grade 11 computer science course.

The game uses Pygame Zero, a Python library great for beginner graphics: https://pygame-zero.readthedocs.io/en/stable/

The main technical challenge of this program was the collision detection and resolution between the square player hitbox and the rectangular blocks that make the different levels. The levels are defined with the coordinates and sizes of the rectangles in pixels rather than an array representing a square grid. This makes level creation easier and more flexible, but also makes collisions a bit more complex. I based my algorithm around this amazing video: https://www.youtube.com/watch?v=8JJ-4JgR7Dg

Some other challenges included the somewhat realistic physics simulation in the minigame, as well as the point-and-click movement.

The game itself focuses on racial discrimination, and Freddie is made to face various challenges based on some real first- and second-hand experiences.
