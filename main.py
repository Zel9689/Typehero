from GameObject import *

print(D_max_hp)

p1 = Player('John', Team.TeamA)
print(p1.is_alive)
p2 = Player('Alice', Team.TeamA)
p2.get_hit(FireBall(p1))
pass