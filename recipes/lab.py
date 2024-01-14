"""
6.101 Lab 6:
Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    output = {}
    for ingredient in recipes:
        if ingredient[0] == "compound" and ingredient[1] not in output:
            output[ingredient[1]] = [ingredient[2]]
        elif ingredient[1] in output:
            output[ingredient[1]].append(ingredient[2])
    return output


def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    output = {}
    for ingredient in recipes:
        if ingredient[0] == "atomic":
            output[ingredient[1]] = ingredient[2]
    return output


def rec_lowest_cost(atomic_dict, compound_dict, ingredient_lists, recipes):
    """
    Given the atomic_dict and compound_dict ingredients dictionaries, the ingredient_list from
    lowest_cost, and the recipes, recursively returns the minimum cost needed to make an item.
    """
    if not ingredient_lists:
        return None

    min_cost = float("inf")
    for recipe in ingredient_lists:
        sum_cost = 0
        for item in recipe:
            if item[0] in compound_dict:
                if list(compound_dict.keys()).count(item[0]) > 1:
                    sum_cost += lowest_cost(recipes, item[0])
                else:
                    low = rec_lowest_cost(
                        atomic_dict, compound_dict, compound_dict[item[0]], recipes)
                    if low is None:
                        sum_cost = float("inf")
                    else:
                        sum_cost += item[1] * low
            elif item[0] in atomic_dict:
                sum_cost += item[1] * atomic_dict[item[0]]
            else:
                sum_cost = float("inf")
        if sum_cost < min_cost:
            min_cost = sum_cost
    if min_cost == float("inf"):
        min_cost = None
    return min_cost


def lowest_cost(recipes, food_item, forbidden=()):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item. Any item in forbidden should not be
    used in the final calculation.
    """
    if food_item in forbidden:
        return None

    atomic = make_atomic_costs(recipes)
    compound = make_recipe_book(recipes)
    if food_item in atomic:
        return atomic[food_item]

    for item in forbidden:
        if item in atomic:
            atomic.pop(item)
        if item in compound:
            compound.pop(item)

    ingredient_lists = []
    for tup in recipes:
        if tup[1] == food_item:
            ingredient_lists.append(tup[2])
    return rec_lowest_cost(atomic, compound, ingredient_lists, recipes)


def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    ingredients = {}
    for ingredient in flat_recipe:
        ingredients[ingredient] = flat_recipe[ingredient] * n

    return ingredients


def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    ingredients = {}
    for recipe in flat_recipes:
        for ingredient in recipe:
            if ingredient not in ingredients:
                ingredients[ingredient] = recipe[ingredient]
            elif ingredient in ingredients:
                ingredients[ingredient] += recipe[ingredient]

    return ingredients


def get_min_cost(flat_recipes, atomic):
    """
    Given list flat_recipes and dict atomic, finds the least costly recipe in
    flat_recipes. 
    """
    min_dict = None
    min_cost = float("inf")
    for flat_recipe in flat_recipes:
        sum_cost = 0
        for ingredient in flat_recipe:
            sum_cost += flat_recipe[ingredient] * atomic[ingredient]
        if sum_cost < min_cost:
            min_cost = sum_cost
            min_dict = flat_recipe
    return min_dict


def rec_cheapest_flat_recipe(atomic, compound, ingredient_lists, recipes):
    """ 
    Given atomic, compound, ingredient_lists, recipes, returns cheapest flat recipe
    """
    if not ingredient_lists:
        return None

    flat_recipes = []

    for recipe in ingredient_lists:
        sum_cost = 0
        flat_recipe = {}
        add = True
        for item in recipe:
            if item[0] in compound:
                flat_list = [flat_recipe]
                if list(compound.keys()).count(item[0]) > 1:
                    flat_list.append(cheapest_flat_recipe(recipes, item[0]))
                else:
                    cur = rec_cheapest_flat_recipe(
                        atomic, compound, compound[item[0]], recipes
                    )
                    if cur is None:
                        add = False
                    else:
                        flat_list.append(scale_recipe(cur, item[1]))
                flat_recipe = make_grocery_list(flat_list)
            elif item[0] in atomic:
                if item[0] not in flat_recipe:
                    flat_recipe[item[0]] = item[1]
                elif item[0] in flat_recipe:
                    flat_recipe[item[0]] += item[1]
            else:
                add = False
        if add:
            flat_recipes.append(flat_recipe)

    min_dict = get_min_cost(flat_recipes, atomic)
    return min_dict


def cheapest_flat_recipe(recipes, food_item, forbidden=None):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    if forbidden is None:
        forbidden = []
    if food_item in forbidden:
        return None

    atomic = make_atomic_costs(recipes)
    compound = make_recipe_book(recipes)
    if food_item in atomic:
        return {food_item: 1}

    for item in forbidden:
        if item in atomic:
            atomic.pop(item)
        if item in compound:
            compound.pop(item)

    ingredient_lists = []
    for tup in recipes:
        if tup[1] == food_item:
            ingredient_lists.append(tup[2])
    return rec_cheapest_flat_recipe(atomic, compound, ingredient_lists, recipes)


def combinations(first_list, second_list):
    """
    Given two lists of dictionaries, returns list of all possible combinations
    of elements in each list.
    """
    output = []
    for recipe1 in first_list:
        for recipe2 in second_list:
            if recipe1 != recipe2:
                output.append(make_grocery_list([recipe1, recipe2]))
    return output


def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes for a certain ingredient, compute and return a list of flat
    recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """
    output = []
    if not flat_recipes:
        return []
    if len(flat_recipes) == 1:
        return flat_recipes[0].copy()
    if len(flat_recipes) == 2:
        return combinations(flat_recipes[0].copy(), flat_recipes[1].copy())

    first = flat_recipes[0]
    rest = flat_recipes[1:]

    return combinations(first, ingredient_mixes(rest))


def all_flat_recipes(recipes, food_item, forbidden=None):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    if forbidden is None:
        forbidden = []

    atomic = make_atomic_costs(recipes)
    compound = make_recipe_book(recipes)

    for item in forbidden:
        if item in atomic:
            atomic.pop(item)
        if item in compound:
            compound.pop(item)

    if food_item in atomic:
        return [{food_item: 1}]

    if food_item not in compound:
        return []

    output = []
    for recipe in compound[food_item]:
        ingredients = []
        for ingredient, quantity in recipe:
            flat_ingredients = all_flat_recipes(recipes, ingredient, forbidden)
            scaled_flat = [
                scale_recipe(ingredient_recipe, quantity)
                for ingredient_recipe in flat_ingredients
            ]
            ingredients.append(scaled_flat)
        output.extend(ingredient_mixes(ingredients))

    return output


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    # you are free to add additional testing code here!
    # atomic = make_atomic_costs(example_recipes)
    # compound = make_recipe_book(example_recipes)
    # sum = 0
    # for key in atomic:
    #     sum += atomic[key]
    # print(sum)
    # total = 0
    # for key in compound:
    #     if len(compound[key]) > 1:
    #         total += 1

    # print(total)
    # dairy_recipes = [
    #     ('compound', 'milk', [('cow', 2), ('milking stool', 1)]),
    #     ('compound', 'cheese', [('milk', 1), ('time', 1)]),
    #     ('compound', 'cheese', [('cutting-edge laboratory', 11)]),
    #     ('atomic', 'milking stool', 5),
    #     ('atomic', 'cutting-edge laboratory', 1000),
    #     ('atomic', 'time', 10000)
    # ]
    # print(lowest_cost(dairy_recipes, 'cheese'))
    # cookie_recipes = [
    #     ('compound', 'cookie sandwich', [
    #      ('cookie', 2), ('ice cream scoop', 3)]),
    #     ('compound', 'cookie', [('chocolate chips', 3)]),
    #     ('compound', 'cookie', [('sugar', 10)]),
    #     ('atomic', 'chocolate chips', 200),
    #     ('atomic', 'sugar', 5),
    #     ('compound', 'ice cream scoop', [('vanilla ice cream', 1)]),
    #     ('compound', 'ice cream scoop', [('chocolate ice cream', 1)]),
    #     ('atomic', 'vanilla ice cream', 20),
    #     ('atomic', 'chocolate ice cream', 30),
    # ]
    # print(lowest_cost(cookie_recipes, 'cookie sandwich'))
    # soup = {"carrots": 5, "celery": 3, "broth": 2,
    #         "noodles": 1, "chicken": 3, "salt": 10}
    # carrot_cake = {"carrots": 5, "flour": 8,
    #                "sugar": 10, "oil": 5, "eggs": 4, "salt": 3}
    # bread = {"flour": 10, "sugar": 3, "oil": 3, "yeast": 15, "salt": 5}
    # grocery_list = [soup, carrot_cake, bread]
    # print(make_grocery_list(grocery_list))
    cookie_recipes = [
        ("compound", "cookie sandwich", [
         ("cookie", 2), ("ice cream scoop", 3)]),
        ("compound", "cookie", [("chocolate chips", 3)]),
        ("compound", "cookie", [("sugar", 10)]),
        ("atomic", "chocolate chips", 200),
        ("atomic", "sugar", 5),
        ("compound", "ice cream scoop", [("vanilla ice cream", 1)]),
        ("compound", "ice cream scoop", [("chocolate ice cream", 1)]),
        ("atomic", "vanilla ice cream", 20),
        ("atomic", "chocolate ice cream", 30),
    ]
    print(all_flat_recipes(cookie_recipes, 'cookie sandwich', ('cookie',)))
