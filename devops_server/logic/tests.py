from django.test import TestCase, Client
from django.urls import reverse

from .views import solve_problem

client = Client()


class GetSolutionTest(TestCase):
    """
    Tests the API endpoint output by making a POST request with valid and invalid payloads,
    and by making a GET request expecting 404.
    """
    def setUp(self):
        self.valid_payloads = [
            {
                "DM_capacity": 20,
                "DE_capacity": 8,
                "data_centers": [
                    {"name": "Paris",
                     "servers": 20},
                    {"name": "Stockholm",
                     "servers": 62}
                ]
            },
            {
                "DM_capacity": 13,
                "DE_capacity": 2,
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 2,
                "DE_capacity": 1,
                "data_centers": [
                    {"name": "City",
                     "servers": 1}
                ]
            },
            {
                "DM_capacity": 2,
                "DE_capacity": 1,
                "data_centers": [
                    {"name": "City",
                     "servers": 1},

                    {"name": "City2",
                     "servers": 1},

                    {"name": "City3",
                     "servers": 1},

                    {"name": "City4",
                     "servers": 1}
                ]
            }
        ]
        self.invalid_payloads = [
            {
                "DM_capacity": "",
                "DE_capacity": 2,
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 13,
                "DE_capacity": 2,
                "data_centers": [
                    {"name": 10,
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 13,
                "DE_capacity": "string",
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 13,
                "DE_capacity": 2,
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": 20,
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 13,
                "DE_capacity": 2,
                "data_centers": 4
            },
            {
                "DE_capacity": 2,
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 13,
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 13,
                "DE_capacity": 2
            },
            {
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": "wrong",
                "DE_capacity": "",
                "data": [
                    {"wrong_field": "Paris",
                     "servers": "servers"},
                    {"name": "Stockholm",
                     "servers": "nope"}
                ]
            },
            {
                "DM_capacity": 0,
                "DE_capacity": 2,
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 13,
                "DE_capacity": 0,
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 13,
                "DE_capacity": 2,
                "data_centers": [
                    {"name": "City",
                     "servers": 0},
                    {"name": "Another city",
                     "servers": 89}
                ]
            },
            {
                "DM_capacity": 13,
                "DE_capacity": 2,
                "data_centers": [
                    {"name": "City",
                     "servers": 34},
                    {"name": "Another city",
                     "servers": 0}
                ]
            },
        ]

    def test_get_request(self):
        response = client.get(reverse("process_input"))
        self.assertEquals(response.status_code, 404)

    def test_valid_post_request(self):
        for valid_payload in self.valid_payloads:
            response = client.post(reverse("process_input"),
                                   data=valid_payload,
                                   content_type="application/json")
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, "DE")
            self.assertContains(response, "DM_data_center")

    def test_invalid_post_request(self):
        for invalid_payload in self.invalid_payloads:
            response = client.post(reverse("process_input"),
                                   data=invalid_payload,
                                   content_type="application/json")
            self.assertEquals(response.status_code, 400)


class SolveProblemTests(TestCase):
    """
    Tests the solve_problem function from views with
    standard inputs and outputs. Verifies the logic.
    """
    def test_standard_inputs(self):
        standard_inputs = [
            {
                "DM_capacity": 20,
                "DE_capacity": 8,
                "data_centers": [
                    {"name": "Paris",
                     "servers": 20},
                    {"name": "Stockholm",
                     "servers": 62}
                ]
            },
            {
                "DM_capacity": 6,
                "DE_capacity": 10,
                "data_centers": [
                    {"name": "Paris",
                     "servers": 30},
                    {"name": "Stockholm",
                     "servers": 66}
                ]
            },
            {
                "DM_capacity": 12,
                "DE_capacity": 7,
                "data_centers": [
                    {"name": "Berlin",
                     "servers": 11},
                    {"name": "Stockholm",
                     "servers": 21}
                ]
            },
            {
                "DM_capacity": 2,
                "DE_capacity": 1,
                "data_centers": [
                    {"name": "City",
                     "servers": 1},

                    {"name": "City2",
                     "servers": 1},

                    {"name": "City3",
                     "servers": 1},

                    {"name": "City4",
                     "servers": 1}
                ]
            },
            {
                "DM_capacity": 1,
                "DE_capacity": 4,
                "data_centers": [
                    {"name": "City",
                     "servers": 1},

                    {"name": "City2",
                     "servers": 1},

                    {"name": "City3",
                     "servers": 1},

                    {"name": "City4",
                     "servers": 1}
                ]
            },
            {
                "DM_capacity": 4,
                "DE_capacity": 1,
                "data_centers": [
                    {"name": "City",
                     "servers": 1},

                    {"name": "City2",
                     "servers": 2},

                    {"name": "City3",
                     "servers": 3},

                    {"name": "City4",
                     "servers": 4}
                ]
            }
        ]
        standard_outputs = [
            {
                "DE": 8,
                "DM_data_center": "Paris"
            },
            {
                "DE": 9,
                "DM_data_center": "Stockholm"
            },
            {
                "DE": 3,
                "DM_data_center": "Berlin"
            },
            {
                "DE": 3,
                "DM_data_center": "City"
            },
            {
                "DE": 3,
                "DM_data_center": "City"
            },
            {
                "DE": 6,
                "DM_data_center": "City4"
            },
        ]

        for standard_input, standard_output in zip(standard_inputs, standard_outputs):
            output = solve_problem(standard_input)
            self.assertEquals(output, standard_output)
