import csv
import time
import calendar
import os

def  moving_avg_short(data, start_date, end_date):
    start_epoch = date_to_epoch(start_date)
    end_epoch = date_to_epoch(end_date)
    dict = {}
    # start at the last element and calculate t,t-1,t-2
    for d in reversed(range(len(data))):
        moving_avg = 0
        row = data[d]
        time = int(row['time'])
        if (start_epoch<=time and end_epoch>=time):
            # calculate the avg with 3 timestamps
            for i in range(3):
                # check we haven't gone past 1st element
                if(d-i<0):
                    # if we have -1 from i to correct the number of days in the calc
                    i-=1
                    break
                moving_avg+=float(data[d-i]['volumeto'])/float(data[d-i]['volumefrom'])
                # divide by total number of timestamps 1<=i<=3
            moving_avg /=(i+1)
            date_string = epoch_to_date(time)
            dict[date_string] = moving_avg
    return dict

	 

def  moving_avg_long(data, start_date, end_date):
    start_epoch = date_to_epoch(start_date)
    end_epoch = date_to_epoch(end_date)
    dict = {}
    for d in reversed(range(len(data))):
        moving_avg = 0
        row = data[d]
        time = int(row['time'])
        if (start_epoch<= time and end_epoch>=time):
            # calculate the avg with 10 timestamps
            for i in range(10):
                if(d-i<0):
                    i-=1
                    break
                avg=float(data[d-i]['volumeto'])/float(data[d-i]['volumefrom'])
                moving_avg+=avg
            moving_avg /=(i+1)
            date_string = epoch_to_date(int(row['time']))
            dict[date_string] = moving_avg 
    return dict


def  find_buy_list(short_avg_dict, long_avg_dict):
    dict = {}
    date_string = ""
    # All the dates in asc order from the short_avg dict
    dates = list(reversed(short_avg_dict.keys()))
    # for each date in the short dict
    for i in range(len(dates)-1):
        # check if the date exists in the long_avg dict
        if(long_avg_dict[dates[i]]):
            # Find out the next timestamp
            next_date_epoch = date_to_epoch(dates[i]) + 3600*24
            date_string = epoch_to_date(int(next_date_epoch))
            # if the short avg <= the long avg for the current timestamp
            if short_avg_dict[dates[i]] <= long_avg_dict[dates[i]]:
                # if the short avg > the long avg for the next timestamp we have buy signal
                if(short_avg_dict[date_string]> long_avg_dict[date_string]):
                    dict[date_string] = 1
            else:
                dict[date_string] = 0  
    return dict



def  find_sell_list(short_avg_dict, long_avg_dict):
    dict = {}
    dates = list(reversed(short_avg_dict.keys()))
    for i in range(len(dates)-1):
        if(long_avg_dict[dates[i]]):
            next_date_epoch = calendar.timegm(time.strptime(dates[i], "%d/%m/%Y")) + 3600*24
            date_string = epoch_to_date(int(next_date_epoch))
            # if the short avg >= the long avg for the current timestamp
            if short_avg_dict[dates[i]] >= long_avg_dict[dates[i]]:
                # if the short avg < the long avg for the next timestamp we have sell signal
                if(short_avg_dict[date_string]< long_avg_dict[date_string]):
                    dict[date_string] = 1
            else:
                dict[date_string] = 0
    return dict




def  crossover_method(data, start_date, end_date):
    # get the dicts for the short/long avg for the date range
    short_avg = moving_avg_short(data,start_date,end_date)
    long_avg = moving_avg_long(data,start_date,end_date)
    # find out if they cross over
    buy_list =find_buy_list(short_avg,long_avg)
    sell_list = find_sell_list(short_avg,long_avg)
    return [buy_list,sell_list]


def date_to_epoch(date):
    return calendar.timegm(time.strptime(date, "%d/%m/%Y")) 


# function to convert epoch to date string
def epoch_to_date(epoch):
    dt = time.gmtime(int(epoch))
    date_string = time.strftime("%d/%m/%Y", dt) 
    return date_string
  

if __name__ == "__main__":
    data = []
    with open(os.path.join(os.path.dirname(__file__), "../cryptocompare_btc.csv"),"r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
    pass
    test = [["01/05/2017", "12/06/2017"],["05/09/2018","27/09/2018"],["03/11/2019","14/11/2019"]]
    for test in test:
        out = (crossover_method(data, test[0], test[1]))
        buy_list = [k for k,v in out[0].items() if v ==1]
        sell_list = [k for k,v in out[1].items() if v ==1]
        print(f"buy list: {buy_list}, sell list: {sell_list}")
