from cowin_api import CoWinAPI
import datetime
import subprocess
district_id = '303'
cowin = CoWinAPI()
x = datetime.datetime.now()
date = str(x.strftime("%d-%m-%Y"))
#print(date)
min_age_limit = 18  # Optional. By default returns centers without filtering by min_age_l
flag = 0

for j in range(5):
    x = datetime.datetime.now() + datetime.timedelta(days=j)
    date = str(x.strftime("%d-%m-%Y"))
    print(' [ + ] Date: '+date)
    available_centers = cowin.get_availability_by_district(district_id, date, min_age_limit)
    #print(available_centers['centers'])
    #flag = 0
    for i in available_centers['centers']:
        if (i.get('sessions')[0].get('available_capacity_dose1') > 0):
            flag = 1
        print(' Hospital: ' + i.get('name') + ' pincode: ' + str(i.get('pincode')) + '\n\t Minimmum age limit = ' + str(i.get('sessions')[0].get('min_age_limit')) + '\n\t vaccine name: '+ str(i.get(
'sessions')[0].get('vaccine')) + '\n\t Dose1 left: ' + str(i.get('sessions')[0].get('available_capacity_dose1')) + '\n\t Dose2 left: ' + str(i.get('sessions')[0].get('available_capacity_dose2'))
)


#if(flag == 1):
#    subprocess.run(['notify-send', 'slots empty!! Go get it!'])
