from Game import *

g = Game.Instance()
g.start_screen()

while g.__game_playing__:
    #create new game
    g.new()

    #game loop
    g.run()

    #auto create new generation after all bird died
    g.__game_playing__ = True
    #g.start_screen() #recursive