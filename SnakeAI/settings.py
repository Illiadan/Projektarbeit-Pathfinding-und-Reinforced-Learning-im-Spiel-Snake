from os import path

# free to change
COLUMNS = 32
ROWS = 24
DEFAULTSPEED = 20
BLOCKSIZE = 20

# not for change
DIRECTORY = path.dirname(__file__)
HS_MANUAL = "highscore_manual.txt"
S_MANUAL = "score_manual.txt"
HS_HAMILTON = "highscore_hamilton.txt"
S_HAMILTON = "score_hamilton.txt"
HS_ASTAR = "highscore_astar.txt"
S_ASTAR = "score_astar.txt"
HS_ASTARLONG = "highscore_astarlong.txt"
S_ASTARLONG = "score_astarlong.txt"
SCREENWIDTH = COLUMNS * BLOCKSIZE
SCREENHIGHT = ROWS * BLOCKSIZE
TEXTSIZE = 16
TITLEHEIGHTMULT = 0.2
VICTORYWIDTH = 128
DEFEATWIDTH = 112
SCOREHEIGHTMULT = 0.4
SCOREWIDTH = 256
INFOHEIGHTMULT = 0.6
INFOWIDTH = 160

# Colors
BLACK = (0, 0, 0)
LGREY = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
