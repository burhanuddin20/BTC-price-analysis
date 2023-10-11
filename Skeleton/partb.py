import csv
import time 
import calendar
import sys
import os

class MyException(Exception):  
    #Exception message set by value 
    def __init__(self, value):  
        self.parameter = value  
     
    #Exception message to be printed 
    def __str__(self):  
        return self.parameter

def  highest_price(data, start_date, end_date):
    try:
        start_epoch = date_to_epoch(start_date) 
        end_epoch = date_to_epoch(end_date) 
        # function to validate the date formate and range
        date_validation(data,start_epoch, end_epoch)
        highest_price = float(-sys.maxsize - 1)
        for d in range(len(data)):
            row = data[d]
            if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
                if(float(row['high'])>  (highest_price)):
                    highest_price = float(row['high'])
        return highest_price
    except KeyError:
        print("Error: requested column is missing from dataset")
        sys.exit()
    except ValueError:
        print("Error: invalid date value")
        sys.exit()
    except MyException as e:
        print(e)
        sys.exit()


def  lowest_price(data, start_date, end_date):
    try:
        start_epoch = date_to_epoch(start_date) 
        end_epoch = date_to_epoch(end_date) 
        date_validation(data,start_epoch, end_epoch)
        lowest_price = float(sys.maxsize)
        for d in range(len(data)-1):
            row = data[d]
            if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
                if(float(row['low'])< lowest_price):
                    lowest_price = float(row['low'])
        return lowest_price
    except KeyError:
        print("Error: requested column is missing from dataset")
        sys.exit()
    except ValueError:
        print("Error: invalid date value")
        sys.exit()
    except MyException as e:
        print(e)
        sys.exit()


def  max_volume(data, start_date, end_date):
    try:
        start_epoch = date_to_epoch(start_date) 
        end_epoch = date_to_epoch(end_date) 
        date_validation(data,start_epoch, end_epoch)
        max_volume = float(-sys.maxsize - 1)
        for d in range(len(data)):
            row = data[d]
            if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
                # volume from is the daily amount exchanged in BTC 
                if(float(row['volumefrom'])> max_volume):
                    max_volume = float(row['volumefrom'])
        return max_volume
    except KeyError:
        print("Error: requested column is missing from dataset")
        sys.exit()
    except ValueError:
        print("Error: invalid date value")
        sys.exit()
    except MyException as e:
        print(e)
        sys.exit()

	 

def  best_avg_price(data, start_date, end_date):
    try:
        start_epoch = date_to_epoch(start_date) 
        end_epoch = date_to_epoch(end_date)
        date_validation(data,start_epoch, end_epoch)
        best_avg_price = float(-sys.maxsize -1)
        for d in range(len(data)-1):
            row = data[d]
            if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
                daily_avg = float(row['volumeto'])/float(row['volumefrom'])
                if(daily_avg>best_avg_price):
                    best_avg_price = daily_avg
        return best_avg_price
    except KeyError:
        print("Error: requested column is missing from dataset")
        sys.exit()
    except ValueError:
        print("Error: invalid date value")
        sys.exit()
    except MyException as e:
        print(e)
        sys.exit()


def  moving_average(data, start_date, end_date):
    try:
        start_epoch = date_to_epoch(start_date) 
        end_epoch = date_to_epoch(end_date)
        date_validation(data,start_epoch, end_epoch)
        moving_avg = 0 
        for d in range(len(data)-1):
            row = data[d]
            if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
                daily_avg = float(row['volumeto'])/float(row['volumefrom'])
                moving_avg += daily_avg
            number_of_days = (end_epoch - start_epoch)/(60*60*24) +1
        return float("{:.2f}".format(moving_avg/number_of_days))
    except KeyError:
        print("Error: requested column is missing from dataset")
        sys.exit()
    except ValueError:
        print("Error: invalid date value")
        sys.exit()
    except MyException as e:
        print(e)
        sys.exit()

#function to convert date to a epoch time
def date_to_epoch(date):
    try:
        return calendar.timegm(time.strptime(date, "%d/%m/%Y")) 
    except: TypeError
    raise ValueError
    
    
def date_validation(data,start_epoch,end_epoch):
    # if start date/ end date don't fall within range or invalid format return an error
    if(start_epoch<int(data[0]['time']) or end_epoch>int(data[len(data)-1]['time'])):
        raise MyException("Error: date value is out of range")
    if(start_epoch>end_epoch):
        raise MyException("Error: end date must be larger than start date")
    


if __name__ == "__main__":    
    data = []
    try:
        with open(os.path.join(os.path.dirname(__file__), "../cryptocompare_btc.csv"),"r") as f:
            reader = csv.DictReader(f)
            data = [r for r in reader]
        pass
        test_data = [["01/01/2016","31/01/2016",462.92],['01/02/2016','28/02/2016',447.61],['01/12/2016','31/12/2016',982.57]]    
        for test in test_data:
            print((highest_price(data,test[0],test[1])))
            
            print()
            test_data = [['01/01/2016','31/01/2016',350.39],['01/02/2016','28/02/2016',365.27],['01/12/2016','31/12/2016',741.08]]
            for test in test_data:
                print((lowest_price(data,test[0],test[1])))
                

            print()
            test_data = [['01/01/2016','31/12/2016',268141.73 ],['01/02/2016','28/02/2016',111626.76 ],['01/12/2016','31/12/2016',102224.08 ]]
            for test in test_data:
                print((max_volume(data,test[0],test[1])))


            
            print()
            test_data = [['01/01/2016','31/12/2016',455.5523025617217  ],['01/02/2016','28/02/2016',439.0143960593451],['01/12/2016','31/12/2016',968.9494656981099]]
            for test in test_data:
                print((best_avg_price(data,test[0],test[1])))
                

            print()
            test_data = [['01/10/2020','01/11/2020',411.89],['01/02/2016','28/02/2016',402.73],['01/12/2016','31/12/2016',824.83]]
            for test in test_data:
                print((moving_average(data,test[0],test[1])))
    except FileNotFoundError:
        print("“Error: dataset not found")

