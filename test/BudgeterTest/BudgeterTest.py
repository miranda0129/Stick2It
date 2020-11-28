import unittest

def calculateSummary(fixed_cost_str, expected_income_str):

    temp_costs = fixed_cost_str.replace(' ', '')
    temp_income = expected_income_str.replace(' ', '')

    if len(temp_costs) > 0:
        costs = temp_costs.split(",")
        # returns sum of the fixed costs, accepts list of numbers or name: value pairs
        total_cost = sum([float(cost.split(":")[-1]) for cost in costs])
    else:
        total_cost = 0

    if len(temp_income) > 0:
        incomes = temp_income.split(",")
        total_income = sum([float(income.split(":")[-1]) for income in incomes])
    else:
        total_income = 0

    summary_str = "Total Income: ${:.2f}, Total Cost: ${:.2f}".format(total_income, total_cost)

    return summary_str


class BudgetTest(unittest.TestCase):

    def test_case1(self): #basic test case

        fixed_cost = "Gas: 50, 20, groceries: 100"
        expected_income = "50, babysitting: 100, yardwork: 50"

        summary = calculateSummary(fixed_cost, expected_income)

        self.assertEqual(summary, "Total Income: $200.00, Total Cost: $170.00")

    def test_case2(self): #test case with no spaces

        fixed_cost = "spotify:9.99,:100,salary:500"
        expected_income = "TeachingAssistant:2000,20,stocks:100,allowance:5,foundchange:.5"

        summary = calculateSummary(fixed_cost, expected_income)

        self.assertEqual(summary, "Total Income: $2125.50, Total Cost: $609.99")


    def test_case3(self): #no name no space

        fixed_cost = "50,100,50"
        expected_income = "50,20,100,90,300,400"


        summary = calculateSummary(fixed_cost, expected_income)

        self.assertEqual(summary, "Total Income: $960.00, Total Cost: $200.00")


    def test_case4(self): #mixed spacing, mixed name, mixed value

        fixed_cost = "Gas: 50, :20,groceries: 100, water-Billzqqz:150,electricity: 120, 40"
        expected_income = "500, bursary:250,scholarship: 50,90, :55.50, .75"


        summary = calculateSummary(fixed_cost, expected_income)

        self.assertEqual(summary, "Total Income: $946.25, Total Cost: $480.00")

if __name__ == '__main__':
    unittest.main()
