from variables import path_elements
# from tkinter import PhotoImage

from PIL import Image, ImageTk

class Fire:
    'primary element'
    image = ImageTk.PhotoImage(Image.open(path_elements+'fire.png'))

    def __add__(self, other):
        if isinstance(other, Earth):
            return Peat()
        elif isinstance(other, Sand):
            return Glass()
        elif isinstance(other, Sea):
            return Salt()
        elif isinstance(other, Clay):
            return Brick()
        elif isinstance(other, Fire):
            return Lava()
        elif isinstance(other, Water):
            return Steam()

class Air:
    'primary element'
    image = ImageTk.PhotoImage(Image.open(path_elements+'air.png'))

    def __add__(self, other):
        if isinstance(other, Air):
            return Wind()
        elif isinstance(other, Water):
            return Fog()
        
class Earth:
    'primary element'
    image = ImageTk.PhotoImage(Image.open(path_elements+'earth.png'))

    def __add__(self, other):
        if isinstance(other, Fire):
            return Peat()
        elif isinstance(other, Storm_cloud):
            return Lighting()
        elif isinstance(other, Earth):
            return Hill()

class Water:
    'primary element'
    image = ImageTk.PhotoImage(Image.open(path_elements+'water.png'))

    def __add__(self, other):
        if isinstance(other, Water):
            return Lake()
        elif isinstance(other, Sand):
            return Clay()
        elif isinstance(other, Fire):
            return Steam()
        elif isinstance(other, Hill):
            return River()
        elif isinstance(other, Air):
            return Fog()
        elif isinstance(other, Cloud):
            return Rain()

class Lava: # Fire+Fire
    'Fire+Fire'
    image = ImageTk.PhotoImage(Image.open(path_elements+'lava.png'))

    def __add__(self, other):
        if isinstance(other, Mountain):
            return Volcano()

class Wind: # Air+Air
    'Air+Air'
    image = ImageTk.PhotoImage(Image.open(path_elements+'wind.png'))

    def __add__(self, other):
        if isinstance(other, Mountain):
            return Stone()
        elif isinstance(other, Stone):
            return Sand()
        
class Fog: # Air+Water
    'Air+Water'
    image = ImageTk.PhotoImage(Image.open(path_elements+'fog.png'))

    def __add__(self, other):
        if isinstance(other, Fog):
            return Cloud()

class Cloud: # Fog+Fog
    'Fog+Fog'
    image = ImageTk.PhotoImage(Image.open(path_elements+'cloud.png'))

    def __add__(self, other):
        if isinstance(other, Water):
            return Rain()

class Rain: # Water+Cloud
    'Water+Cloud'
    image = ImageTk.PhotoImage(Image.open(path_elements+'rain.png'))

    def __add__(self, other):
        if isinstance(other, Rain):
            return Storm_cloud()

class Storm_cloud: # Rain+Rain
    'Rain+Rain'
    image = ImageTk.PhotoImage(Image.open(path_elements+'storm_cloud.png'))

    def __add__(self, other):
        if isinstance(other, Earth):
            return Lighting()

class Lighting: # Earth+Storm_cloud
    'Earth+Storm_cloud'
    image = ImageTk.PhotoImage(Image.open(path_elements+'lighting.png'))

    def __add__(self, other):
        pass

class Hill: # Earth+Earth
    'Earth+Earth'
    image = ImageTk.PhotoImage(Image.open(path_elements+'hill.png'))

    def __add__(self, other):
        if isinstance(other, Hill):
            return Mountain()
        elif isinstance(other, Water):
            return River()

class Mountain: # Hill+Hill
    'Hill+Hill'
    image = ImageTk.PhotoImage(Image.open(path_elements+'mountain.png'))

    def __add__(self, other):
        if isinstance(other, Lava):
            return Volcano()
        elif isinstance(other, Wind):
            return Stone()
        elif isinstance(other, Time):
            return Plain()
        elif isinstance(other, Mountain):
            return Mountain_ridge()

class Mountain_ridge: # Mountain+Mountain
    'Mountain+Mountain'
    image = ImageTk.PhotoImage(Image.open(path_elements+'mountain_ridge.png'))

    def __add__(self, other):
        if isinstance(other, Plain):
            return Continent()

class River: # Water+Hill
    'Water+Hill'
    image = ImageTk.PhotoImage(Image.open(path_elements+'river.png'))

    def __add__(self, other):
        if isinstance(other, Stone):
            return Limestone()

class Stone: # Mountain+Wind
    'Mountain+Wind'
    image = ImageTk.PhotoImage(Image.open(path_elements+'stone.png'))

    def __add__(self, other):
        if isinstance(other, Wind):
            return Sand()
        elif isinstance(other, River):
            return Limestone()

class Limestone: # River+Stone
    'River+Stone'
    image = ImageTk.PhotoImage(Image.open(path_elements+'limestone.png'))
    
    def __add__(self, other):
        pass

class Sand: # Wind+Stone
    'Wind+Stone'
    image = ImageTk.PhotoImage(Image.open(path_elements+'sand.png'))

    def __add__(self, other):
        if isinstance(other, Fire):
            return Glass()
        elif isinstance(other, Water):
            return Clay()
        elif isinstance(other, Glass):
            return Time()
        elif isinstance(other, Sand):
            return Desert()
 
class Glass: # Fire+Sand
    'Fire+Sand'
    image = ImageTk.PhotoImage(Image.open(path_elements+'glass.png'))

    def __add__(self, other):
        if isinstance(other, Sand):
            return Time()
 
class Time: # Sand+Glass
    'Sand+Glass'
    image = ImageTk.PhotoImage(Image.open(path_elements+'time.png'))

    def __add__(self, other):
        if isinstance(other, Mountain):
            return Plain()
 
class Plain: # Mountain+Time
    'Mountain+Time'
    image = ImageTk.PhotoImage(Image.open(path_elements+'plain.png'))

    def __add__(self, other):
        if isinstance(other, Mountain_ridge):
            return Continent()
 
class Desert: # Sand+Sand
    'Sand+Sand'
    image = ImageTk.PhotoImage(Image.open(path_elements+'desert.png'))

    def __add__(self, other):
            pass

class Continent: # Mountain_ridge+Plain
    'Mountain_ridge+Plain'
    image = ImageTk.PhotoImage(Image.open(path_elements+'continent.png'))

    def __add__(self, other):
        if isinstance(other, Ocean):
            return Planet()
 
class Lake: # Water+Water
    'Water+Water'
    image = ImageTk.PhotoImage(Image.open(path_elements+'lake.png'))

    def __add__(self, other):
        if isinstance(other, Peat):
            return Swamp()
        elif isinstance(other, Lake):
            return Sea()

class Sea: # Lake+Lake
    'Lake+Lake'
    image = ImageTk.PhotoImage(Image.open(path_elements+'sea.png'))
    
    def __add__(self, other):
        if isinstance(other, Fire):
            return Salt()
        elif isinstance(other, Sea):
            return Ocean()

class Ocean: # Sea+Sea
    'Sea+Sea'
    image = ImageTk.PhotoImage(Image.open(path_elements+'ocean.png'))
    
    def __add__(self, other):
        if isinstance(other, Continent):
            return Planet()

class Planet: # Continent+Ocean
    'Continent+Ocean'
    image = ImageTk.PhotoImage(Image.open(path_elements+'planet.png'))

    def __add__(self, other):
        pass
 
class Peat: # Fire+Earth
    'Fire+Earth'
    image = ImageTk.PhotoImage(Image.open(path_elements+'peat.png'))

    def __add__(self, other):
        if isinstance(other, Lake):
            return Swamp()
 
class Swamp: # Lake+Peat
    'Lake+Peat'
    image = ImageTk.PhotoImage(Image.open(path_elements+'swamp.png'))

    def __add__(self, other):
        pass
 
class Salt: # Fire+Sea
    'Fire+Sea'
    image = ImageTk.PhotoImage(Image.open(path_elements+'salt.png'))

    def __add__(self, other):
        pass

class Clay: # Water+Sand
    'Water+Sand'
    image = ImageTk.PhotoImage(Image.open(path_elements+'clay.png'))

    def __add__(self, other):
        if isinstance(other, Fire):
            return Brick()

class Brick: # Clay+Fire
    'Clay+Fire'
    image = ImageTk.PhotoImage(Image.open(path_elements+'brick.png'))

    def __add__(self, other):
        if isinstance(other, Brick):
            return Wall()

class Wall: # Brick+Brick
    'Brick+Brick'
    image = ImageTk.PhotoImage(Image.open(path_elements+'wall.png'))

    def __add__(self, other):
        pass

class Volcano: # Lava+Mountain
    'Lava+Mountain'
    image = ImageTk.PhotoImage(Image.open(path_elements+'volcano.png'))

    def __add__(self, other):
        pass

class Steam: # Fire+Water
    'Fire+Water'
    image = ImageTk.PhotoImage(Image.open(path_elements+'steam.png'))

    def __add__(self, other):
        pass

