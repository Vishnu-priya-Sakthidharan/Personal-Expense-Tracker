# This file collects the input from the user and validates that data.

from datetime import datetime

date_format = '%d-%m-%Y'
Categories = {
    'I' : 'Income',
    'E' : 'Expense'
    }

# function to get the date from user
def get_date(prompt,allow_default = False):

    date_str = input(prompt)

    # if user clicks on enter or doesn't enter any date, it chooses today's date
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str,date_format) # 'strptime converts string format to date-time object'
        return valid_date.strftime(date_format) # 'strftime converts date and time objects to their string representation'
    
    except ValueError:
        print('Invalid date format. Please enter the date in the format dd-mm-yy')
        return get_date(prompt,allow_default) # Recursive function - calls the same method until user enters the valid date or choose today's date
    
# function to get the date from user
def get_amount():

    try:
        amount = float(input('Enter the amount: '))
        if amount <=0:
            raise ValueError('Amount must be non negative non zero value.')
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

# function to get the category from user
def get_category():
    category = input("Enter the category  'I' for Income or 'E' for Expense : ").upper()

    if category in Categories:
        return Categories[category]
    
    print("Invalid Category! Please enter 'I' for income or 'E' for Expense")
    return get_category()

# function to get the description from user
def get_description():
    description = input('Enter the description(optional):')
    return description


