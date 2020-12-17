from flask import Flask, render_template, request
import urllib.parse, urllib.request, urllib.error, json

app = Flask(__name__)

### Cocktail website code

# Gets the specific drink's dictionary
def calling(name=None):
    baseurl = 'https://www.thecocktaildb.com/api/json/v1/1/search.php'
    dict = {'s': name}
    par = urllib.parse.urlencode(dict)
    request = baseurl + "?" + par
    requeststr = urllib.request.urlopen(request).read()
    data = json.loads(requeststr)
    return data

# Gets the name of the drink that is being shown
def get_name(name=None):
    data = calling(name=name)
    return data['drinks'][0]['strDrink']

# Displays the ingredients and the amount of each ingredients
def ingredients (name=None):
    data = calling(name=name)
    lst = []
    eat = []
    measure = []
    num = 0
    for i in range(1, 15):
        ingred = "strIngredient%s" % i
        amount = "strMeasure%s" % i
        for food in data['drinks'][0]:
            if amount in food:
                if data['drinks'][0][food] is not None:
                    num = num + 1
                    measure.append(data['drinks'][0][food])
            if ingred in food:
                if data['drinks'][0][food] is not None:
                    eat.append(data['drinks'][0][food])
    for x in range(0, num):
        combine = (measure[x] + " " + eat[x])
        lst.append(combine)
    tog_list = ", ".join(lst)
    return "Ingredients: " + tog_list

# Displays the instructions on how to make the drink
def instructions (name=None):
    data = calling(name=name)
    return "Instruction: %s" % (data['drinks'][0]["strInstructions"])

# Gives me the url for the image of the drink
def give_image(name=None):
    data = calling(name=name)
    base = data['drinks'][0]['strDrinkThumb']
    picture = base + "/preview"
    return picture

# Filters out all the drinks that has the specific ingredient
def all_ingredients(ingred=None):
    baseurl = "https://www.thecocktaildb.com/api/json/v1/1/filter.php"
    dict = {'i': ingred}
    par = urllib.parse.urlencode(dict)
    request = baseurl + "?" + par
    requeststr = urllib.request.urlopen(request).read()
    data = json.loads(requeststr)
    return data

# Creates a list of drinks with the specific ingredient
def name_lst_drinks(ingred=None):
    lst = []
    data = all_ingredients(ingred=ingred)
    for i in range(len(data['drinks'])):
        lst.append(data['drinks'][i]['strDrink'])
    return lst

### App code

# Main page asking for drink
@app.route("/")
def main_handler():
    return render_template('request.txt', page_title="Drink Form")

# Response page which displays all the info to create the drink
@app.route("/gresponse")
def check():
    drink = request.args.get('cocktail')
    try:
        if drink:
            return render_template('drink_list.txt',
                drink=get_name(name=drink),
                page_title="Drink instructions",
                images=give_image(name=drink),
                ingred=ingredients(name=drink),
                instruct=instructions(name=drink))
        else:
            return render_template('request.txt',
                page_title="No Drink Entered",
                prompt="Please enter a drink name and we will give you the ingredients and instructions")
    except Exception:
        return render_template('request.txt',
            page_title="Not in database",
            prompt="Your drink was not in the database. Try again.")

# Gives me a list of drinks with the specific ingredient
@app.route("/gresponseingred")
def check_ingred():
    try:
        ingred = request.args.get('ingredient')
        lst = name_lst_drinks(ingred=ingred)
        images = [give_image(drink) for drink in lst]
        if ingred:
            return render_template('ingredient_drink_list.txt',
                ingred=ingred,
                len=len(lst),
                lst=lst,
                images=images,
                page_title="List of drinks with " + ingred)
    except Exception:
        return render_template('request.txt',
            page_title="Not in database",
            promptingr="Your ingredient was not in the database. Try again.")

if __name__ == '__main__':
   app.run(host="localhost", port=8081, debug=True)