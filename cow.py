from cowin_api import CoWinAPI

district_id = '303'
import datetime

x = datetime.datetime.now()
date = str(x.strftime("%d-%m-%Y"))
print(date)

min_age_limit = 18  # Optional. By default returns centers without filtering by min_age_l


cowin = CoWinAPI()
available_centers = cowin.get_availability_by_district(district_id, date, min_age_limit)
print(available_centers[centers])
#for i in available_centers:
 #   print(i)
