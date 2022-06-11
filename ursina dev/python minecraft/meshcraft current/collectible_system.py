"""
June 11 2022
Collectible pick-ups system (CPS).

We'll pass the subject, or rather, the inventory
through to this system?

Well, it makes sense to have the inventory system
speak to this system.

We'll want to add an inventory item to hotbar
when picked up by subject. That means
instantiating a new item and placing it near hotbar.
In Minecraft, stacking behaviour would kick in here:
if an item of same type that is not fully stacked,
i.e., is less than 64 items high, then add to this stack.
"""