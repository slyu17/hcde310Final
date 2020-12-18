from flask import Flask, render_template, request
import urllib.parse, urllib.request, urllib.error, json, logging

app = Flask(__name__)

def getSafe(url):
    try:
        return json.load(urllib.request.urlopen(url))
    except urllib.error.HTTPError as e:
        print("Error trying to retrieve data:", e)
    except urllib.error.URLError as e:
        print("Error trying to retrieve data:", e)
    return None

def getData(food, baseurl = "https://api.nal.usda.gov/fdc/v1/foods/search", key = "K5r0QiVxrRbgRoCdcaf45ErnGc8HI9Ay1mdTsrs4",
            params = {},pageSize = 5,sortBy = "dataType.keyword", sortOrder = "asc"):
    params["api_key"] = key
    params["query"] = food
    params["pageSize"] = pageSize
    params["sortBy"] = sortBy
    params["sortOrder"] = sortOrder
    url = baseurl + "?" + urllib.parse.urlencode(params)
    return getSafe(url)

@app.route('/')
def search():
    app.logger.info("In Search Form")
    return render_template('search.html')

@app.route('/results')
def result():
    food = request.args.get('food')
    app.logger.info(food)
    nutrients = {}
    name = getData(food)["foods"][0]["description"]
    if food:
        for food in getData(food)["foods"]:
            title = "Brand Owner: " + food["brandOwner"]
            nutrients[title] = {}
            for items in food["foodNutrients"]:
                nutrients[title][items["nutrientName"]] = "%s"%items["value"] + items["unitName"]
        return render_template('index.html', name=name, brand=title, nutrients=nutrients)
    else:
        return render_template("search.html", prompt="Please enter a valid food name.")


if __name__ == '__main__':
    app.run(host='localhost',port=8080,debug=True)
