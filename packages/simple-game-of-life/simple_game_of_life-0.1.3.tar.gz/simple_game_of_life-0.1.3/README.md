# Game Of Life

Simple way to play Conway's game of life in python.<br>
You can import your own map as json file name "save.json", using `get_MAP` methode.<br>
All you custom maps (in the save.json file) are available in the list `custom_maps`.<br>
Other custom maps are available such as: `my_map_1` and `my_map_2`, created using `Map` class : <br>
```python
from simple_game_of_life import Map
m = Map(100)
my_map_1 = m.mini_random_MAP((25, 20))
my_map_2 = m.kind(kind="line 10")
```

NOTE : Two artificials borders are created for each map, <br>
The first one is visible while playing, it's in black.<br>
The second one is white (invisible) just after the black border, no cell can born here


## Installation

Run the following command to install:<br>
```$ pip install simple-game-of-life ```

## Usage

for a random map
```python
from simple_game_of_life import GameOfLife
game = GameOfLife(50) # 50 is the side (width, height) of the map
game.start_animation()
```

for a custom map
```python
from simple_game_of_life import GameOfLife
from random import choice
my_custom_map = GameOfLife.get_MAP() 
game = GameOfLife(custom_map=choice(my_custom_map))
game.start_animation()
# Note you can also import custom_map like that :
# from simple_game_of_life import custom_map 
```

to implement a pattern :
```python
from simple_game_of_life import GameOfLife, Map
glider = [[0,1,0],
          [0,0,1],
          [1,1,1]]
m = Map(100) # 100 is the side (width, height) of the map
my_map = m.my_pattern(glider)
game = GameOfLife(custom_map=my_map)
game.start_animation()
```

## Other usage

`GameOfLife` classe :<br>
- You can save a map by using `saved_MAP` methode.<br>
- You can get a map by using `get_MAP` methode.<br>
- You can reset all saved map by using `reset_MAP` methode.<br>
- You can get all frames by using `get_history` methode.<br>
- You can set a new animation with the same instance using `new_animation` methode.<br>


`Map` classe :<br>
- `full_random_MAP` : all the map gonna be random.<br>
- `mini_random_MAP` : a portion of the map gonna be random.<br>
- `my_pattern` : insert your pattern into an empty map.<br>
- `kind` : 
    - insert well know pattern into an empty map, (currenly 5 patterns are available).<br>
    - random : choice randomly one of the following map<br>
    - `"glider"` <br>
    - `"lwss"` : Lightweight spaceship<br>
    - `"mwss"` : Middleweight spaceship<br>
    - `"hwss"` : Heavyweight spaceship<br>

You can also calculate the average time of instancing, using `timeit` function:
```python
game = timeit(GameOfLife, loop=10, size_or_side=50, frames=200) # loop : number of loop
game.start_animation()
```

### Optionals parameters

- When instancing `GameOfLife` classe : <br>
    Args: <br>
        size_or_side ((iterable, lenght = 2) or int): 
        either size of a matrix  
        or side (width, height) of a square matrix. 
        Defaults to None.
        
        custom_map (iterable, matrix): 
        a custom map that you created using an iterable (dim=2, matrix), or by using `Board` classe . 
        Defaults to None.
        
        seed (int, optional): 
        set the seed, by using `np.random.seed`. 
        Defaults to None.
        
        frames (int, optional):
        number of frames calculated. 
        Defaults to 100.
        
        zoom (float, optional): 
        allow to create larger plot, if zoom=10 (square matrix) then the figure size will be (5, 5) inch. 
        Defaults to 10.

- when starting the animation using `start_animation`: <br>
    NOTE : <br>
        For saving, 
        You need first to install ffmpeg,
        First search : Homebrew website (https://brew.sh/),
        Copy past the command in a Terminal, press enter.
        Then in a Terminal : brew install ffmpeg

    Args:<br>
        interval_between_two_frames (int, optional):
        Interval between two frames in milisecond. Defaults to 100.

        plot (bool, optional): 
        Allow plotting. Defaults to True.

        save (bool, optional):
        Allow save. Defaults to False.

        fps (int, optional):  
        Frames per second if saved. Defaults to 30.

        file_name (str, optional): 
        file name for saved, must end by ".mp4", ".mov", ".avi", ".flv" or ".wmv", otherwise it's save with ".mp4".
        Defaults to None.