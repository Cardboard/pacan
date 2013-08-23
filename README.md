# =PACAN=
=====

Roguelike Pac-Man made using curses. Or something like that.

### Symbols:
  @ : pacan
  # : ghost
  . : pellet
  o : power pellet
  X : wall
  
  
### Rules:  
Collect all the pellets to win. You have three lives. Touching a ghost while they are not scared costs you one life (and the ghost dies).
When you run out of lives the game is over. Ghosts have three states: scared, chase, and free. Scared (blue) ghosts run away,
chasing (magenta) ghosts run towards the player, and free (white) ghosts move randomly. Ghosts alternate between 
chase and free when they are not scared. Up to four ghosts can be in the game at once. Losing lives negatively affects your 
score, while eating pellets and ghosts increases your score.
