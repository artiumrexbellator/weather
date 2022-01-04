from Request import Request
selection = ""
print("Welcome!!")
while selection != '!qa':
    selection = input("\nTo leave press [!qa] \nTo see available stations press [s] \nTo see the plot of last station press [p] \nTo see wordcloud press [w] \nOtherwise press any other key to continue : ")
    if selection == "s" :
        print(Request.stations())
    elif selection == "w":
        req.wordCloud()
    elif selection == 'p':
        req.plot()
    elif selection != '!qa':
        # station=input("please type the station : ")
        # date=input("please enter the date in following format YYYY-mm-dd : ")
        station='ROUEN-BOOS'
        date='2019-2-20'
        try:
          req=Request(station,date)
        except Exception as e:
          print(e)
          continue
        req.printData()
        print(f"\n\nTo use web version go to http://127.0.0.1:5000/home?station={req.station}&date={req.date}")
    



