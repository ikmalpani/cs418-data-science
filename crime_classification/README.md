Query 2:

Download the crimes dataset from: https://drive.google.com/file/d/11psZu0BDaX_7xZnDBb_DW7xsOhUOG_Qi/view?usp=sharing and save it in this directory.

Ensure that there is 'Community area and zip code equivalency - Community area and zip code equ.csv' is present in the directory.

1. On the command line/terminal run: python crime_predictions.py

2. Ensure models have been generated and stored in models folder as pickle files

3. On the command line/terminal run: python multiple_addresses.py with command line args. See instructions below.

4. Check the 'address_op_crime.csv' for the output

Run the multiple_addresses.py file as:

> python multiple_addresses.py "1333 W Flournoy St, Chicago Illinois 60607" 17 26 "Thu"

Here the arguments are:
first argument: Address as a string
second argument: Hour as a number in 24 hour format
third argument: Minute as a number
fourth argument: Day of the week as a string.

To run multiple addresses together use the same format.

Ex:
> python multiple_addresses.py "1333 W Flournoy St, Chicago Illinois 60607" 12 22 "Thu" "801 S Morgan St, Chicago Illinois 60607" 17 42 "Sat" "1333 W Flournoy St, Chicago Illinois 60607" 12 22 "Thu" "801 S Morgan St, Chicago Illinois 60607" 17 42 "Sat"

If you run into any trouble(or it takes too long) while running the code, move to the folder notebooks and look at the iPython Notebooks with the results.
