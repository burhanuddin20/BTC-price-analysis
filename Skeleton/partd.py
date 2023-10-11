import csv
import calendar
import time
import os
import sys


class MyException(Exception):  
    def __init__(self, value):  
        self.parameter = value  
     
    def __str__(self):  
        return self.parameter

class Investment:
    def __init__(self,start_date,end_date,data):
        self.start_date = start_date
        self.end_date = end_date
        self.data = data

    def  highest_price(self,data = None, start_date = None, end_date = None):
        try:
            data = self.data if data is None else data
            start_date = self.start_date if start_date is None else start_date
            end_date = self.end_date if end_date is None else end_date
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

    
    def  lowest_price(self,data = None, start_date = None, end_date = None):
        try:
            data = self.data if data is None else data
            start_date = self.start_date if start_date is None else start_date
            end_date = self.end_date if end_date is None else end_date
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
    
    
    def  max_volume(self,data = None, start_date = None, end_date = None):
        try:
            data = self.data if data is None else data
            start_date = self.start_date if start_date is None else start_date
            end_date = self.end_date if end_date is None else end_date
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
    
    	 
    def  best_avg_price(self,data = None, start_date = None, end_date = None):
        try:
            data = self.data if data is None else data
            start_date = self.start_date if start_date is None else start_date
            end_date = self.end_date if end_date is None else end_date
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
    
    
    
    def  moving_average(self,data = None, start_date = None, end_date = None):
        try:
            data = self.data if data is None else data
            start_date = self.start_date if start_date is None else start_date
            end_date = self.end_date if end_date is None else end_date
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

def regression_model(self:Investment,y,data=None,start_date=None,end_date=None):
    try:
        # if parameters are not passed use the instance variables
        data  = self.data if data is None else self.data
        start_date = self.start_date if start_date is None else self.start_date
        end_date = self.end_date if end_date is None else self.end_date

        start_epoch = date_to_epoch(start_date)
        end_epoch =  date_to_epoch(end_date)
        date_validation(data,start_epoch, end_epoch)
        time_epochs = range(start_epoch,end_epoch+(3600*24),3600*24) # Gives all the time epochs
        # calcualte the X avg - same for all functions
        X_avg = sum(time_epochs)/(len(time_epochs))
        
        sum_xy = 0
        sum_x_squared = 0
        daily_avg = 0
        # if we are predicting the next days avg price
        if(y == "avg_price"):
            # Get the avg price of the range
            Y_avg = self.moving_average(data,start_date,end_date)
            for row in data:
                x = int(row['time'])
                if (start_epoch<= x and end_epoch>=x):
                    std_dev_x = int(row['time']) - X_avg
                    date_string = epoch_to_date(x)
                    # get the avg price of the day and minus from Y
                    std_dev_y = self.best_avg_price(data,date_string,date_string) - Y_avg
                    sum_xy += std_dev_x * std_dev_y
                    sum_x_squared += std_dev_x*std_dev_x

        # if we are classifying the trend
        elif(y  != "avg_price"):
            number_of_days = (end_epoch - start_epoch)/(3600*24) + 1
            # calculate the mean of daily lows / daily highs
            for row in data:
                x = int(row['time'])
                if (start_epoch<= x and end_epoch>= x):
                    daily_avg += float(row[y])
            Y_avg = daily_avg/number_of_days
            # do the calculations
            for row in data:
                x = int(row['time'])
                if (start_epoch<=x and end_epoch>=x):
                    # calculate x - X
                    std_dev_x = x - X_avg
                    # calculate y-Y
                    std_dev_y =  float(row[y])- Y_avg
                    sum_xy += std_dev_x * std_dev_y
                    sum_x_squared += std_dev_x*std_dev_x     
                    

        # return the gradient and intercept
        m = sum_xy/sum_x_squared
        b = Y_avg - (m*X_avg)
        return m,b
    except KeyError:
        print("Error: requested column is missing from dataset")
        sys.exit()
    except ValueError:
        print("Error: invalid date value")
        sys.exit()
    except MyException as e:
        print(e)
        sys.exit()



def	predict_next_average(investment:Investment):
    # call the regression function to with the specified y
    m,b  = regression_model(investment,y ="avg_price")
    end_epoch = date_to_epoch(investment.end_date)
    # calculate y_next by using the next epoch,m and b
    y_next = m*(end_epoch+86400) + b
    return y_next



def classify_trend(investment):
    m_low,b_low  = regression_model(self = investment,y ='low')
    m_high,b_high = regression_model(self = investment,y ='high')
# The gradients tell us if the lows/highs are increasing or decreasing
    if(m_high>0 and m_low<0):
        return "volatile"
    if(m_high > 0 and m_low> 0):
        return "increasing"
    if(m_high<0 and m_low < 0):
        return "decreasing"
    else: return "other"
    
    
    
    
def date_to_epoch(date):
    try:
        return calendar.timegm(time.strptime(date, "%d/%m/%Y"))
    except: TypeError
    raise ValueError


def epoch_to_date(epoch):
    try:
        dt = time.gmtime(int(epoch))
        date_string = time.strftime("%d/%m/%Y", dt) 
        return date_string
    except: TypeError
    raise ValueError
    

def date_validation(data,start_epoch,end_epoch):
    # if start date/ end date don't fall within range or invalid format return an error
    if(start_epoch<int(data[0]['time']) or end_epoch>int(data[len(data)-1]['time'])):
        raise MyException("Error: date value is out of range")
    if(start_epoch>end_epoch):
        raise MyException("Error: end date must be larger than start date")
		



if __name__ == "__main__":
    # Start the program
    data = []
    with open(os.path.join(os.path.dirname(__file__), "../cryptocompare_btc.csv"),"r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
    test1 = Investment("04/05/2015" ,"27/05/2015",data)    
    test2 = Investment("08/12/2016" ,"11/12/2016",data)
    test3 = Investment("01/02/2016" ,"28/02/2016",data)
    test_data = [test1,test2,test3]
    for test in test_data:
        print(f" next avg: {predict_next_average(test) } and classification: {classify_trend(test)}")
        print()

    test4 = Investment("01/01/2016","31/01/2016",data)
    print(test4.highest_price())
    print(test4.highest_price(start_date="15/01/2016"))
  