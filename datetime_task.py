from datetime import datetime, date, timedelta

today = datetime.now()
delta_1day = timedelta(days=1)
yesterday = today - delta_1day

delta_30days = timedelta(days=30)

day_a_month_ago = today - delta_30days

date_string = '01/01/17 12:10:03.234567'
date_dt = datetime.strptime(date_string, '%d/%m/%y %H:%M:%S.%f')
print(today.strftime('%d/%m/%Y'),
    yesterday.strftime('%d/%m/%Y'),
    day_a_month_ago.strftime('%d/%m/%Y'), date_dt)
