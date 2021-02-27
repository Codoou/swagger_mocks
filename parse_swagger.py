from flask import Flask
import flask
from string import Template
import json

app = Flask(__name__)
end_points = {}
models = {}
data = None

def get_models(data):
    ''''''
    definitions = data.get('definitions')
    for definition in definitions:
        models[definition] = {}

        # May have to do an initial type check here, but we only
        # have an object type at this point, so moving along
        for property in definitions[definition]:

            if property == "properties":
                for field in definitions[definition][property]:
                    if field not in models[definition]:
                        models[definition][field] = {}

                    for field_property in definitions[definition][property][field]:
                        if field_property == "type":
                            models[definition][field][field_property] = definitions[definition][property][field][field_property]

                    

            # Deal with after all the properties are initialized
            if property == "required":
                for required_field in definitions[definition][property]:
                    if required_field not in models[definition]:
                        models[definition][required_field] = {}
                    models[definition][required_field]["required"] = True


    print(models)





def get_paths(data):
    ''''''
    paths = data.get('paths')
    for path in paths:
        end_points[path] = {}
        for response_type in data['paths'][path]:
            end_points[path][response_type] = {}
            for property in data['paths'][path][response_type]:
                if property == "responses":
                    for response in data['paths'][path][response_type][property]:
                        if int(response) < 300 > 199:
                            end_points[path][response_type]["success_response"] = int(response)

                            for response_props in data['paths'][path][response_type][property][response]:
                                if response_props == "schema":
                                    for schema_defs in data['paths'][path][response_type][property][response][response_props]:
                                        if schema_defs == "$ref":
                                            # print(data['paths'][path][response_type][property][response][response_props][schema_defs])
                                            ref = data['paths'][path][response_type][property][response][response_props][schema_defs].rsplit('/', 1)[-1]
                                            # print(ref)
                                            end_points[path][response_type]['model'] = models[ref]
                                            # models[ref]

                                        if schema_defs == "items":
                                            for item in data['paths'][path][response_type][property][response][response_props][schema_defs]:
                                                if item == "$ref":
                                                    items_ref = data['paths'][path][response_type][property][response][response_props][schema_defs][item].rsplit('/', 1)[-1]
                                                    end_points[path][response_type]['model'] = [models[ref]]




                


        #Pull apart the data

    print(end_points)

def set_up():
    with open('swagger.json') as f:
        data = json.load(f)

    get_models(data)
    get_paths(data)

@app.route('/')
def homepage():
    return """<h1>Testing World</h1>"""



@app.route('/<some_place>/')
def some_place_page(some_place):

    some_place = f"/{some_place}/"
    if some_place in end_points.keys():
        if str(flask.request.method).lower() in end_points[some_place].keys():
            return({"success":"true"})
        return json.dumps({"test":"frank"})
    return json.dumps({"error":"unknown url"})

if __name__ == '__main__':
    set_up()
    app.run(debug=True, use_reloader=True)