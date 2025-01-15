# this file handles the main flow of the program

import pandas as pd
from datetime import datetime
import csv
from data_entry import get_amount,get_category,get_date,get_description
import matplotlib.pyplot as plt

class CSV:

    CSV_FILE = 'finance.csv'
    COLUMNS =['Date', 'Amount', 'Category','Description']
    FORMAT = '%d-%m-%Y' # %y - 24 , %Y-2024

    # class method to initialise the csv file
    @classmethod # here, method is bound to the class and not to an instance of the class. As a result, the method receives the class (cls) as its first argument, rather than an instance (self)
    def initialise_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    # class method to add a new entry to the csv file
    @classmethod
    def add_entry_to_csv(cls,Date,Amount,Category,Description):
        new_entry = {
            'Date' : Date,
            'Amount' : Amount,
            'Category' : Category,
            'Description' : Description
        }
        with open(cls.CSV_FILE,'a',newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print('Entry added successfully!')

    # class method to show the transaction summary to the user
    @classmethod
    def get_transactions(cls,start_date,end_date):
             
        df = pd.read_csv(cls.CSV_FILE)
        print(df)
        df['Date'] = pd.to_datetime(df['Date'],format=cls.FORMAT) # converting the date  from str into datetime
        start_date = datetime.strptime(start_date,cls.FORMAT) # converting the date from str into datetime
        end_date = datetime.strptime(end_date,cls.FORMAT) # converting the date from str into datetime

        mask = (df['Date'] >= start_date) & (df['Date'] <=end_date) # mask is of Bool type , filters the rows in df which satifies the condition
        print(mask)

        filtered_df = df.loc[mask] # locating the rows with mask 

        if filtered_df.empty:
            print('No Transactions found in the given time range')
        else:
            print(f"Transactions from {start_date.strftime(format=CSV.FORMAT)} and {end_date.strftime(format=CSV.FORMAT)}")
            print(filtered_df.to_string(index=False,formatters={'Date': lambda x : x.strftime(CSV.FORMAT)})) # conerting each row of date column using lambda function

            total_income = filtered_df[filtered_df['Category'] == 'Income']['Amount'].sum()
            total_expense = filtered_df[filtered_df['Category'] == 'Expense']['Amount'].sum()
            print('\nSummary:')
            print(f'Total Income : ${total_income:.2f}')
            print(f'Total Expense : ${total_expense:.2f}')
            print(f'Net Savings : ${(total_income - total_expense):.2f}')
        
        return filtered_df


def add():

        CSV.initialise_csv()
        date = get_date("Enter the date in dd-mm-yyyy format or press enter to choose today's date : ",True)
        amount = get_amount()
        category = get_category()
        description = get_description()
        CSV.add_entry_to_csv(date,amount,category,description)

def plot_transactions(df):

    df.set_index('Date',inplace=True) # setting 'Date' column as index

    # creating df for income and expense
    # income_df = extracting only income category rows and resampling(fills up the empty dates) on daily basis('D'), summing the different transactions on particular day and ensuring the index remains as 'Date' after applying these functions
    income_df = df[df['Category'] == 'Income'].resample('D').sum().reindex(df.index, fill_value=0)

    expense_df = df[df['Category'] == 'Expense'].resample('D').sum().reindex(df.index, fill_value=0)

    # converting the Date into datetime object so that can be sorted and plotted corretly
    income_df.index = pd.to_datetime(income_df.index, format=CSV.FORMAT)
    expense_df.index = pd.to_datetime(expense_df.index, format=CSV.FORMAT)
    income_df = income_df.sort_index()
    expense_df = expense_df.sort_index()

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df['Amount'],label ='Income',color='g')
    plt.plot(expense_df.index,expense_df['Amount'],label ='Expense',color='r')
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income and Expense over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
        
def main():
    print('\nPersonal Finance Tracker')

    while True:
        print('\n1.Add Transactions')
        print('2.View transactions and summary within a date range')
        print('3.Exit')
        choice = input('Enter your Choice (1-3) : ')

        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date('Enter the start date(dd-mm-yyyy) : ')
            end_date = get_date('Enter the end date(dd-mm-yyyy) : ')
            df = CSV.get_transactions(start_date,end_date)
           
            if input('Do you want to visualise your income and expense (y/n) : ').lower() == 'y':
                plot_transactions(df)

        elif choice == '3':
            print('Exiting...')
            break
        else:
            print('Invalid choice! Choose 1, 2 or 3')

if __name__=='__main__':
    main()

