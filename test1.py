import csv

from datetime import timedelta, datetime, tzinfo, time

#mmsi;date_time_utc;lon;lat;sog;cog;true_heading;nav_status;message_nr
filename = '/Volumes/IBES_LynchLab/AIS/2011/20110101-20110601/ais_20110101.csv'
filepath = '/Volumes/IBES_LynchLab/AIS/2011/20110101-20110601/ais_20110101.csv'

def _timeRange(a, b, c, d): 
    print("{} {} {} {} {}".format(cnt, a, b, c, d))
    start = datetime.strptime(c, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    diff = end-start
    print("")
    print('******************')
    print(start)
    print(end)
    print(diff)
    print(diff.seconds)
    print(diff.days)
    print('******************')
    print(type(diff).__dict__['min'].__get__(diff, type(diff)))
    print(diff.__dict__)
    print("") 

with open(filename) as f:
    reader = csv.DictReader(f, delimiter=';')
    try:
        _t   = []
        _sid = []
        for cnt, row in enumerate(reader):
            _sid.append(row['mmsi'])
            _t.append(row['date_time_utc'])
            _a = _sid[0]; _b = _sid[cnt]
            _c = _t[0]; _d = _t[cnt]
            _timeRange(_a,_b,_c,_d)

    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

