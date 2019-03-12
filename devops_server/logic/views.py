from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import json

import numpy as np


@csrf_exempt
def process(request):
    if request.method == "POST":
        body = json.loads(request.body, encoding="utf-8")
        validate_body(body)
        result = solve_problem(body)
        return JsonResponse(result)

    else:
        return HttpResponseNotFound("Do a POST request to that endpoint: other methods are not supported")

def validate_body(body):
    fields = ["DM_capacity", "DE_capacity", "data_centers"]
    for field in fields:
        if field not in body:
            raise ValueError("Missing parameter in the input: "+field)


def solve_problem(body):
    print("Ready to solve the problem")
    solutions = []
    for DM_position in body['data_centers']:
        print("DM at center: ", DM_position['name'], "servers: ", DM_position['servers'])
        DE_count = 0
        for s in body['data_centers']:
            if s['name']==DM_position['name']:
                DE_count += int(np.ceil((s['servers']-body['DM_capacity'])/body['DE_capacity']))
                print(" DE total: ", int(np.ceil((s['servers']-body['DM_capacity'])/body['DE_capacity']))) 
            else:
                DE_count += int(np.ceil(s['servers']/body['DE_capacity']))
                print(" DE total: ", int(np.ceil(s['servers']/body['DE_capacity'])))
        print(" * Total DEs = "+str(DE_count))
        solutions.append({"DE":DE_count, "DM_data_center": DM_position['name']})
    solutions_sorted = sorted(solutions, key = lambda k: k['DE'])
    print(" ** sorted solutions = ", solutions_sorted)
    return solutions_sorted[0]
