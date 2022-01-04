from Request import Request
c=""
print("welcome   !!")
while c!='!qa':
    c=input("\n -----------> to leave press [!qa],to see available stations press [s]\nto see the plot of last station press [p],to see wordcloud press [w]\notherwise press any other key to continue : ")
    if c== "s" :
        print(Request.stations())
    elif c== "w":
        req.wordCloud()
    elif c=='p':
        req.plot()
    elif c!='!qa':
        station=input("please type the station : ")
        date=input("please enter the date in following format YYYY-mm-dd : ")
        try:
            req=Request(station,date)
        except Exception as e:
            print(e)
            continue
        req.printData()
        print("to use web version go to http://127.0.0.1:5000/home?station="+req.station+"&date="+req.date)
    



