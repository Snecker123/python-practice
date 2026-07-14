def exercise_1():
    """
    Select all even numbers from the np  array [1, 2, 3, 4, 5, 6, 7, 8].
    Output: [2, 4, 6, 8]
    """
    pass


def exercise_2():
    """
    Compute the mean, sum, and standard deviation of a random array of 100 numbers.
    Generate the array using np random module.
    """
    pass


def exercise_3():
    """
    Generate an 1D array with 12 elements. Reshape it into a 3x4 2D array.
    Example: in - [0 ,1 ,2, 3, 4, 5, 6, 7, 8, 9 , 10 , 11]
            out - [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]
    """
    pass


def exercise_4():
    """
    Find the index of the maximum element in a 2D array.
    Example: in - [[3, 5, 10], [9, 2, 8]]
            out - (0, 2)
    """
    pass


def exercise_5():
    """
    Create two 2x2 matrices. Perform the element-wise multiplication and the matrix multiplication (dot product).
    Example: in - [[1, 2], [3, 4]]
                  [[5, 6], [7, 8]]
            out - [[5, 12], [21, 32]]
                  [[19, 22], [43, 50]]
    """
    pass


# Pandas Exercises
"""
 Import the dataset from the week6_dataset folder in different dataframes.
 (sales, targets, product, salesperson, region)
 Using this data respond to the next questions:

 1. Which is the most profitable month on average?
    # clean sales data (remove $ and covert 'Sales', 'Cost' to float)
    # compute 'Margin' column = 'Sales' - 'Cost'
    # convert 'OrderDate' to datetime and extract month to 'OrderMonth' (dt.month)
    # group by 'OrderMonth' compute mean for 'Margin' column
    # find the month with the highest value of mean

 2. Show names of top 5 best performing employees by total order value in 2020.
    # convert 'OrderDate' to datetime and extract year to 'Year' (dt.year)
    # filter sales by 'Year'
    # merge with salesperson by 'EmployeeKey'
    # group by 'Salesperson' to find the highest value for the sum of 'Sales'

 3. How many products were sold in 2020 grouped by product category?
    # filter sales by 'Year'
    # merge product with sales on 'ProductKey'
    # count the 'ProductKey' values grouped by 'Category'

 4. Find revenue margin, and target for each year.
    # clean target data (remove $ and covert 'Target' to float) and use also sales data
    # convert 'TargetMonth' to datetime and extract year to 'Year' (dt.year)
    # convert 'OrderDate' to datetime and extract year to 'Year' (dt.year)
    # revenue margin = group sales by 'Year' and compute the sum for 'Sales' and 'Margin' columns (from Q1)
    # target = group targets by 'Year' and compute the sum of 'Target' column
    # merge revenue margin with target on 'Year'

 5. Which product category made the most profit by year?
    # merge product with sales on 'ProductKey'
    # profit it's the sum of margin column grouped by 'Year' and 'Category'
    # find the category with the highest value 'Margin'

 6. Find the region with largest revenue the most profitable region.

 7. Which country is the least profitable?
    # merge sales with region by 'SalesTerritoryKey'
    # group by 'Country' to find the min 'Margin' value

 8. How many employees missed their target in 2020? By how much?

 9. Create a matrix showing total sales by Year and Category.

 10. For every sale, calculate how much larger or smaller it is than the average sale of its category.

 11. Create a chart showing yearly revenue.

"""