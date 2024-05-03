from world import World

# Create a world and run simulations
world = World()
for _ in range(100):
    world.simulate_interaction()
