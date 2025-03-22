import pygame as pyg

class Item:
    counted = 0
    def __init__(self,name,damage,weight):
        self.name = name
        self.damage = damage
        self.weight = weight
        Item.counted +=1
    @classmethod  # @classmethod and @staticmethod not really useful
    def from_dict(cls,data):
        return cls(data["name"], data["damage"], data["weight"])
    
    @staticmethod
    def is_heavy(weight):
        return weight>10
    
    @classmethod
    def count(cls):
        return cls.counted


class Weapon(Item):
    weapon_count = 0
    def __init__(self,name, damage, weight, durability):
        super().__init__(name, damage, weight)
        self.durability = durability
        Weapon.weapon_count +=1
    @classmethod
    def weaponCount(cls):
        return cls.weapon_count
    
    
def fight(a,b):
    return a.damage > b.damage
    
sword = Weapon("sword",20,30,10)
print(sword.is_heavy(sword.weight))
print(Weapon.weaponCount())
stick = Item("stick",10,40)
print(stick.is_heavy(stick.weight))
print(Item.count())


print(f"A stick vs a Sword ; does the stick win?: {fight(stick,sword)}")
print(f"A sword vs a stick ; does the sword win?: {fight(sword, stick)}")
print(f"A stick vs a stick ; does the stick win?: {fight(stick, stick)}")
