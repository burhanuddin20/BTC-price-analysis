import csv
import time 
import calendar
import sys
import os

def  highest_price(data, start_date, end_date):
    start_epoch = date_to_epoch(start_date) 
    end_epoch = date_to_epoch(end_date) 
    # set an initial value to smallest negative number to compare with
    highest_price = float(-sys.maxsize - 1)
    for d in range(len(data)):
        row = data[d]
        if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
            if(float(row['high'])>  (highest_price)):
                highest_price = float(row['high'])
    return highest_price



def  lowest_price(data, start_date, end_date):
    start_epoch = date_to_epoch(start_date) 
    end_epoch = date_to_epoch(end_date)
    # set an initial value to largest positive number to compare with
    lowest_price = float(sys.maxsize)
    for d in range(len(data)-1):
        row = data[d]
        if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
            if(float(row['low'])< lowest_price):
                lowest_price = float(row['low'])
    return lowest_price




def  max_volume(data, start_date, end_date):
    start_epoch = date_to_epoch(start_date) 
    end_epoch = date_to_epoch(end_date)  
    max_volume = float(-sys.maxsize - 1)
    for d in range(len(data)):
        row = data[d]
        if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
            # volume from is the daily amount exchanged in BTC 
            if(float(row['volumefrom'])> max_volume):
                max_volume = float(row['volumefrom'])
    return max_volume
	 

def  best_avg_price(data, start_date, end_date):
    start_epoch = date_to_epoch(start_date) 
    end_epoch = date_to_epoch(end_date)  
    best_avg_price = float(-sys.maxsize -1)
    for d in range(len(data)-1):
        row = data[d]
        if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
            daily_avg = float(row['volumeto'])/float(row['volumefrom'])
            if(daily_avg>best_avg_price):
                best_avg_price = daily_avg
    return best_avg_price


def  moving_average(data, start_date, end_date):
    start_epoch = date_to_epoch(start_date) 
    end_epoch = date_to_epoch(end_date) 
    moving_avg = 0 
    for d in range(len(data)-1):
        row = data[d]
        if (start_epoch<= int(row['time']) and end_epoch>=int(row['time'])):
            daily_avg = float(row['volumeto'])/float(row['volumefrom'])
            moving_avg += daily_avg
        # find the number of days in seconds and add 24hrs to be inclusive
        number_of_days = (end_epoch - start_epoch)/(60*60*24) +1
    return float("{:.2f}".format(moving_avg/number_of_days))

#function to convert date to a epoch time
def date_to_epoch(date):
    return calendar.timegm(time.strptime(date, "%d/%m/%Y")) 
    

if __name__ == "__main__":
    
    data = []
    data_dir = '/Users/burhanuddin/Downloads/'
    with open(os.path.join(os.path.dirname(__file__), "../cryptocompare_btc.csv"),"r") as f:
            reader = csv.DictReader(f)
            data = [r for r in reader]


    test_data = [['01/01/2016','31/01/2016',462.92],['01/02/2016','28/02/2016',447.61],['01/12/2016','31/12/2016',982.57]]    
    for test in test_data:
        print((highest_price(data,test[0],test[1])))
  

    print()
    test_data = [['01/01/2016','31/01/2016',350.39],['01/02/2016','28/02/2016',365.27],['01/12/2016','31/12/2016',741.08]]
    for test in test_data:
        print((lowest_price(data,test[0],test[1])))
        

    print()
    test_data = [['01/01/2016','31/01/2016',268141.73 ],['01/02/2016','28/02/2016',111626.76 ],['01/12/2016','31/12/2016',102224.08 ]]
    for test in test_data:
        print((max_volume(data,test[0],test[1])))


    
    print()
    test_data = [['01/01/2016','31/01/2016',455.5523025617217  ],['01/02/2016','28/02/2016',439.0143960593451],['01/12/2016','31/12/2016',968.9494656981099]]
    for test in test_data:
        print((best_avg_price(data,test[0],test[1])))
        

    print()
    test_data = [['01/01/2016','31/01/2016',411.89],['01/02/2016','28/02/2016',402.73],['01/12/2016','31/12/2016',824.83]]
    for test in test_data:
        print((moving_average(data,test[0],test[1])))
