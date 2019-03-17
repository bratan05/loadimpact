from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import json

import numpy as np


@csrf_exempt
def process(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body, encoding="utf-8", object_pairs_hook=dict_raise_on_duplicates)
            validate_body(body)
        except ValueError as err:
            return HttpResponseBadRequest("Input validation failed, {err}".format(err=err))
        result = solve_problem(body)
        return JsonResponse(result)

    else:
        return HttpResponseNotFound("Do a POST request to that endpoint: other methods are not supported")


def validate_body(body: dict):
    """
    Validates the request body, checking the following:
    1. All required fields are present
    2. Only required fields are present
    3. Numerical values are within allowed range [1,+Inf)

    :param body: request body to validate
    :return: raises ValueError on failed validation
    """
    # Checking if all required fields are present
    fields_set = {"DM_capacity", "DE_capacity", "data_centers"}
    body_fields_set = set(body.keys())
    if fields_set != body_fields_set:
        raise ValueError("Got unexpected set of fields {body} "
                         "instead of {expected}".format(
                         body=body_fields_set,
                         expected=fields_set))

    if type(body["data_centers"]) != list:
        raise ValueError("Expecting a list of data centers, "
                         "instead got value {data_centers} instead".format(
                         data_centers=body["data_centers"]))

    data_centers_fields_set = {"name", "servers"}
    for data_center in body['data_centers']:
        if set(data_center) != data_centers_fields_set:
            raise ValueError("Got unexpected set of data_centers fields "
                             "{data_center} instead of "
                             "{expected} for entry {entry}".format(
                             data_center=set(data_center.keys()),
                             expected=data_centers_fields_set,
                             entry=data_center))

        if type(data_center["name"]) != str:
            raise ValueError("Data center name must be str, got "
                             "{data_center} for entry {entry}".format(
                             data_center=data_center["name"],
                             entry=data_center))

        if type(data_center["servers"]) != int:
            raise ValueError("Number of servers must be int, got "
                             "{servers} for entry {entry}".format(
                             servers=data_center["servers"],
                             entry=data_center))

        if data_center["servers"] < 1:
            raise ValueError("Numeric value for servers {value} "
                             "is smaller than 1 for entry {entry}".format(
                             value=data_center["servers"],
                             entry=data_center))

    capacity = ["DM_capacity", "DE_capacity"]
    for key in capacity:
        if type(body[key]) != int:
            raise ValueError("Numeric value for key {key} "
                             "is not integer: {value}".format(key=key, value=body[key]))
        if body[key] < 1:
            raise ValueError("Numeric value for key {key} "
                             "is smaller than 1: {value}".format(key=key, value=body[key]))


def solve_problem(body: dict):
    solutions = []
    for DM_position in body['data_centers']:
        DE_count = 0
        for s in body['data_centers']:
            if s['name']==DM_position['name']:
                delta = int(np.ceil((s['servers']-body['DM_capacity'])/body['DE_capacity']))
                if delta > 0:
                    DE_count += delta
            else:
                DE_count += int(np.ceil(s['servers']/body['DE_capacity']))
        solutions.append({"DE":DE_count, "DM_data_center": DM_position['name']})
    solutions_sorted = sorted(solutions, key=lambda k: k['DE'])
    return solutions_sorted[0]


def dict_raise_on_duplicates(ordered_pairs: dict):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
           raise ValueError("duplicate key: %r" % (k,))
        else:
           d[k] = v
    return d