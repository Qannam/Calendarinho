from django.db import models
import datetime
from collections import namedtuple


class Employee(models.Model):
    EmpName = models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.EmpName


    def getAllLeaves(self):
        event_arr = []
        all_leaves = Leave.objects.filter(emp_id = self.id)
        colors = ["#2C3E50","#2980B9"]
        for i in all_leaves:
            event_sub_arr = {}
            event_sub_arr['empName'] = self.EmpName
            event_sub_arr['title'] = i.Note + " -- " +i.LeaveType
            start_date = datetime.datetime.strptime(str(i.StartDate), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(i.EndDate), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_sub_arr['end'] = end_date
            event_sub_arr['id'] = i.id
            event_sub_arr['color'] = colors[0] if i.LeaveType == "Vacation" else colors[1]
            event_arr.append(event_sub_arr)
        return event_arr

    def getAllEngagements(self):
        event_arr = []
        all_engagements = self.Engagements.all()
        colors = ["#BD4932"]
        for i in all_engagements:
            event_sub_arr = {}
            event_sub_arr['name'] = i.EngName
            start_date = datetime.datetime.strptime(str(i.StartDate), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(i.EndDate), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['startDate'] = start_date
            event_sub_arr['endDate'] = end_date
            event_sub_arr['engID'] = i.id
            event_sub_arr['color'] = colors[0]
            event_sub_arr['serviceType'] = i.ServiceType
            event_sub_arr['clientName'] = i.CliName
            event_arr.append(event_sub_arr)
        return event_arr


    def overlapCheck(self, StartDate, EndDate): #This method check if employee is availabile at a range of date
        engs = Engagement.objects.filter(Employees = self.id)
        leaves = Leave.objects.filter(emp_id = self.id)
        Range = namedtuple('Range', ['start', 'end'])
        start_date1 = datetime.datetime.strptime(str(StartDate), "%Y-%m-%d")
        end_date1 = datetime.datetime.strptime(str(EndDate), "%Y-%m-%d")
        Range1 = Range(start=start_date1, end=end_date1)
        event_dates= {"start_date":[],"end_date":[]}
        for eng in engs:
            event_dates["start_date"].append(eng.StartDate)
            event_dates["end_date"].append(eng.EndDate)

        for lev in leaves:
            event_dates["start_date"].append(lev.StartDate)
            event_dates["end_date"].append(lev.EndDate)

        for i in range(len(event_dates["start_date"])):
            start_date2 = datetime.datetime.strptime(str(event_dates["start_date"][i]), "%Y-%m-%d")
            end_date2 = datetime.datetime.strptime(str(event_dates["end_date"][i]), "%Y-%m-%d")
            latestStart = max(start_date1,start_date2)
            earliestEnd = min(end_date1, end_date2)
            delta = (earliestEnd - latestStart).days + 1
            overlapDays = max(0, delta)
            if (overlapDays != 0):
                return True
        
    def dateInRange(self, date, fromDate, toDate):
        if fromDate <= datetime.date(date.year, date.month, date.day) <= toDate:
            return True
        else:
            return False


    def currentStatus(self):
        todayDate = datetime.datetime.now()
        leaves = Leave.objects.filter(emp_id = self.id)
        for lev in leaves:
            if (self.dateInRange(todayDate,lev.StartDate,lev.EndDate)):
                return [lev.LeaveType,lev.__str__(),lev.EndDate]

        engs = Engagement.objects.filter(Employees = self.id)
        for eng in engs:
            if (self.dateInRange(todayDate,eng.StartDate,eng.EndDate)):
                return ["Engaged",eng.__str__(),eng.EndDate]
    
        return ["Available","","-"]


    def nextEvent(self):
        eng = Engagement.objects.filter(Employees = self.id).filter(StartDate__gt=datetime.datetime.now().strftime("%Y-%m-%d")).order_by("StartDate").first()
        lev = Leave.objects.filter(emp_id = self.id).filter(StartDate__gt=datetime.datetime.now().strftime("%Y-%m-%d")).order_by("StartDate").first()
        try:
            if(eng.StartDate > lev.StartDate):
                return [lev.__str__(),lev.StartDate]
            else:
                return [eng.__str__(),eng.StartDate]
        except:
            if(eng == None and lev == None):
                return["None","-"]
            elif(eng == None):
                return [lev.__str__(),lev.StartDate]
            else:
                return [eng.__str__(),eng.StartDate]
                
class Client(models.Model):
    CliName = models.CharField(max_length=200)
    CliShort = models.CharField(max_length=10)
    def __str__(self):
        return str(self.CliName)


class Engagement(models.Model):
    EngName = models.CharField(max_length=200)
    CliName = models.ForeignKey(Client, on_delete=models.PROTECT)
    Employees = models.ManyToManyField("Employee", blank=True, related_name="Engagements")
    services = (("Non","--"),("WVA","Web Vulnerability Asseessment"),("WPT","Web Penetration Testing"), ("SCR","Source Code Review"), ("NVA","Network Vulnerability Asseessment"), ("NPT","Network Penetration Testing"))
    ServiceType = models.CharField(max_length=3, choices=services, default="Non")
    StartDate = models.DateField('Start Date')
    EndDate = models.DateField('End Date')

    def getAllEngs():
        event_arr = []
        all_events = Engagement.objects.all() 
        colors = ["#277D9C","#09ADA9","#461AAD","#9E0034","#B7410E","#446600"]
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.EngName + " -- " +i.ServiceType
            start_date = datetime.datetime.strptime(str(i.StartDate), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(i.EndDate), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_sub_arr['end'] = end_date
            event_sub_arr['id'] = i.id
            event_sub_arr['color'] = colors[i.id%len(colors)]
            event_arr.append(event_sub_arr)
        return event_arr

    def __str__(self):
        return str(self.EngName + " - " + self.ServiceType)


    def daysLeft(self):
        todayDatetiem = datetime.date.today()
        todayDate = datetime.date(todayDatetiem.year, todayDatetiem.month, todayDatetiem.day)
        if (todayDate >= self.StartDate and todayDate <= self.EndDate):
            daysLeft = todayDate - self.EndDate
            totalDays = self.EndDate - self.StartDate
            precent = (daysLeft / totalDays) * 100
            return int("{:2.0f}".format(precent+100))
        
        return "Nope" #Return False if the engagement didn't start or has finished.

        



class Leave(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE) 
    Note = models.CharField(max_length=200)
    StartDate = models.DateField('Start Date')
    EndDate = models.DateField('End Date')
    Types = (("Training","Training"),("Vacation","Vacation"))
    LeaveType = models.CharField(max_length=8, choices=Types, default="Vacation")

    def __str__(self):
        return str(self.LeaveType) + " -- " + str(self.Note)

