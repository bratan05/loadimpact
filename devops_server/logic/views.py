from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import json

import numpy as np


@csrf_exempt
def process(request):
    """
    API endpoint used for request processing.
    POST request is accepted with JSON body of the following form:
    {
    "DM_capacity": 4,
    "DE_capacity": 1,
    "data_centers": [
       {"name": "City",
       "servers": 1},
       {"name": "City2",
       "servers": 2},
       ...
       ]
    }
    where DM_capacity and DE_capacity are number of servers DM or DE can handle,
    data_centers is a list of cities and servers in them.

    The endpoint returns a JSON with number of DE's required and the best city to place DM:
    {"DE": 6, "DM_data_center": "City4"}
    When a failure occurs, it returns either 404 or 400
    """

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

    # data_centers must be a list
    if type(body["data_centers"]) != list:
        raise ValueError("Expecting a list of data centers, "
                         "instead got value {data_centers} instead".format(
                          data_centers=body["data_centers"]))

    data_centers_fields_set = {"name", "servers"}
    for data_center in body['data_centers']:
        # data_centers list entries must have two fields
        if set(data_center) != data_centers_fields_set:
            raise ValueError("Got unexpected set of data_centers fields "
                             "{data_center} instead of "
                             "{expected} for entry {entry}".format(
                              data_center=set(data_center.keys()),
                              expected=data_centers_fields_set,
                              entry=data_center))
        # name field is a string
        if type(data_center["name"]) != str:
            raise ValueError("Data center name must be str, got "
                             "{data_center} for entry {entry}".format(
                              data_center=data_center["name"],
                              entry=data_center))
        # servers field is an int
        if type(data_center["servers"]) != int:
            raise ValueError("Number of servers must be int, got "
                             "{servers} for entry {entry}".format(
                              servers=data_center["servers"],
                              entry=data_center))
        # servers field is defined on [1, Inf)
        if data_center["servers"] < 1:
            raise ValueError("Numeric value for servers {value} "
                             "is smaller than 1 for entry {entry}".format(
                              value=data_center["servers"],
                              entry=data_center))

    capacity = ["DM_capacity", "DE_capacity"]
    for key in capacity:
        # capacities are integer
        if type(body[key]) != int:
            raise ValueError("Numeric value for key {key} "
                             "is not integer: {value}".format(key=key, value=body[key]))
        # capacities are defined on [1, Inf)
        if body[key] < 1:
            raise ValueError("Numeric value for key {key} "
                             "is smaller than 1: {value}".format(key=key, value=body[key]))


def solve_problem(body: dict):
    """
    Solves the problem of distributing DM and DE's over cities.

    The algorithm works as follows:
       1 Take the first datacenter, place DM there: subtract his capacity from number
         of servers at that datacenter
       2 Distribute remaining servers to DE's
       3 Append the resulting configuration to the solutions list
       4 Repeat 1-3 for all datacenters
       5 Find the configuration with minimum number of DE's
    In a nutshell, the algorithm directly constructs solution space and then finds
    the optimal solution

    :param body: JSON object according to process(request) function requirements
    :return: optimal solution
    """
    solutions = []
    for DM_position in body['data_centers']:
        DE_count = 0
        for s in body['data_centers']:
            if s['name'] == DM_position['name']:
                # delta is the number of DE's required to cover what's left after
                # putting DM to the given datacenter
                delta = int(np.ceil((s['servers']-body['DM_capacity'])/body['DE_capacity']))
                # when DM capacity is larger than number of servers,
                # delta is negative or zero. It means that there is no need
                # to add DE's to that datacenter, because DM covers it
                # completely
                if delta > 0:
                    DE_count += delta
            else:
                DE_count += int(np.ceil(s['servers']/body['DE_capacity']))
        solutions.append({"DE": DE_count, "DM_data_center": DM_position['name']})
    solutions_sorted = sorted(solutions, key=lambda k: k['DE'])
    return solutions_sorted[0]


def dict_raise_on_duplicates(ordered_pairs: dict):
    """
    Reject duplicate keys for json.loads() function
    """
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError("duplicate key: %r" % (k,))
        else:
            d[k] = v
    return d
