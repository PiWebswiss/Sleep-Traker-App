import re
import datetime
import csv
import flask
app = flask.Flask("server")


""" Get html page """
def get_html(page_name):
    html = open(page_name + ".html")
    content = html.read()
    html.close()
    return content


""" Create text file """
def write_username(name):
    file = open("database/username.txt", "w")
    file.write(name.lower())
    file.close()
    

""" Read username stored in the text file """
def read_username():
    with open("database/username.txt", "r") as f:
        reader = f.read()
        return reader


""" Pluralize word """
def pluralize(string, number):
    if number == 1:
        return string
    else:
        return string + "s"


""" Check if date already exists in csv if yes we change the value """
def check_if_exists(date, time):
    date_row = str(date)
    with open("database/" + read_username() + ".csv") as csvfile:
        content = csvfile.read()
        if content.find(date_row) != -1:
            """ Replace old hours by new hours using regex """
            """ .1 call the function re.sub() """   
            """ .2 r = The r means that the string is to be treated as a raw string, which means all escape codes will be ignored. """
            """ .3 () is a capture group  """
            """ .4 \d+ will match any digit from 0 to 9 in a target string with a min of 1 or maximum any number of digits. """
            """ .5 After the comma "," we set the value to change  """
            """ .6 r'\1,' is the first capture group; second argument is the target string """
            new_content = re.sub(r'(' + date_row + '),\d+', r'\1,' + str(time), content)
            with open("database/" + read_username()  + ".csv", "w", newline = "") as csvfile:
                csvfile.write(new_content)
            return True
    return False      


""" Write to csv """
def write_time(date, time):
    try:
        open("database/" + read_username() + ".csv")
        file = ""
    except:
        file = "No"
        with open("database/" + read_username()  + ".csv", "w", newline = "") as csvfile:
            fieldnames = ["Date", "Hours"]
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerow({"Date": date, "Hours": time})
    if file != "No":
        """ Check if date already exists """
        if check_if_exists(date, time) != True:
            with open("database/" + read_username()  + ".csv", "a", newline = "") as csvfile:
                fieldnames = ["Date", "Hours"]
                writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
                writer.writerow({"Date": date, "Hours": time})

""" DateUtility class definition """
class DateUtility: 
    def __init__(self):
        self.weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        self.class_dict = {
            1: "Mo",
            2: "Tu",
            3: "We",
            4: "Th",
            5: "Fr",
            6: "Sa",
            7: "Su"
        }

    """ Get date of today """
    def today_date(self):
        return datetime.date.today()
    
    """ Get today's number; example 1 = Tuesday """
    def today_number(self):
        return datetime.date.weekday(datetime.date.today())
    
    """ Get current week's Monday's date """
    def monday_date(self):
        return self.today_date() - datetime.timedelta(self.today_number())
    
    """ Get the date of a day in a week by index """   
    def week_date(self, number):
        return str(self.monday_date() + datetime.timedelta(int(number)))

    """ Get dates of the week """   
    def date_dict(self):
        dict_date = {
            1: str(self.monday_date()),
            2: self.week_date(1),
            3: self.week_date(2),
            4: self.week_date(3),
            5: self.week_date(4),
            6: self.week_date(5),
            7: self.week_date(6),
            8: self.week_date(7)
        }
        return dict_date


""" Graph class definition """
class Graph():
    """ Read the csv dictionary """
    def read_csv(self):
        try:
            with open("database/" + read_username() + ".csv") as csvfile:
                content = csv.DictReader(csvfile)
                values = ""
                for row in content:
                    values += row["Date"] + "," + row["Hours"] + " "
                return values[: -1].split(" ")

        except: return "no"

    """ Generate graph & insert into html """
    def set_data(self):
        html = get_html("index")
        du = DateUtility()
        """ Get calendar date """
        week_dates = du.date_dict()
        first_date = week_dates[1]
        last_date = week_dates[8]
        monday = du.weekday[0] + " "
        calendar_date_start = datetime.datetime.strptime(first_date, "%Y-%m-%d").strftime("%d-%m") 
        calendar_date = "Week " + monday + calendar_date_start + " to " + monday + datetime.datetime.strptime(last_date,"%Y-%m-%d").strftime("%d-%m-%Y")
        """ Check if csv file exists, if none return html with default values """
        if self.read_csv() == "no":
            """ Replace content in html  """
            html = html.replace("$$DATE$$", calendar_date)
            html = html.replace("$$AVERAGE$$", "0")
            html = html.replace("$$TRACKE$$", "-")
            return html
        else:
            list_length = len(self.read_csv())
            number_of_hours = 0
            for row in self.read_csv():
                key = 0
                """ Save csv values for statistics """
                values = row.split(",")
                number_of_hours += int(values[1])
                for line in range(7):
                    key += 1
                    """ Search for correlated week date   """
                    if row.find(week_dates[key]) != -1:
                        number = 0
                        content = row.split(",")
                        hours = int(content[1])
                        for day in range(hours):
                            number += 1 
                            """ Get week day abbreviation """
                            day = du.class_dict[key] + str(number).zfill(2)
                            """ Highlight active cells in graph """
                            html = html.replace(day, "box-green")              
            """ Split the element to find the date and hours  """
            data = row.split(",")
            """ Date """
            d = data[0]
            """ Hours """
            h = data.pop(1)
            """ Find the day name by its number example: Monday = 0 """
            day_num = datetime.datetime.strptime(d, "%Y-%m-%d").weekday()
            """ Search the day name using the day number  """
            day_name = du.weekday[day_num]
            """ Change date format into "%d-%m-%Y" """
            date_of_last_element = datetime.datetime.strptime(d,"%Y-%m-%d").strftime("%d-%m-%Y")
            """ Reformat date """
            last_element_date = day_name + " " + str(date_of_last_element) + " " + h + pluralize(" hour", int(h))
            """ Calculate average sleeping time """
            average_hours = round(number_of_hours  / list_length)
            average = str(average_hours) + pluralize(" hour", average_hours)
            """ Replace content in html """
            html = html.replace("$$DATE$$", calendar_date)
            html = html.replace("$$AVERAGE$$", average if average else "0")
            html = html.replace("$$TRACKE$$", last_element_date if last_element_date else "-")
        
            return html     
                

""" Initialize Graph class """
calendar = Graph()

""" Handle index.html """
@app.route("/")
def get_index():
    return calendar.set_data()

""" Handle login """
@app.route("/getuser", methods = ["POST"])
def get_form():
    user_name = flask.request.form["username"]
    if user_name is None or user_name == "":
        return calendar.set_data()
    write_username(user_name)
    return calendar.set_data()

""" Handle post form data  """
@app.route("/save", methods = ["POST"])
def save_date():
    """ Get the input of the user """
    date_one = flask.request.form["dateOne"]
    date_two = flask.request.form["dateTwo"]
    time_bed = flask.request.form["timeBed"]
    time_up = flask.request.form["timeUp"]
    """ Addition date + time"""
    t1 = date_one + " " + time_bed
    t2 = date_two + " " + time_up
    """ Convert string to date object """
    """  module   class    method
        datetime.datetime.strptime(date, "%Y-%m-%d") """
    h1 = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M")
    h2 = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M")
    """ Variable hours is the number of hours the user slept """
    time = str(h2 - h1)
    """ Convert date to  date + time; handle if hours > 24h & if hours < 24h  """
    d = 0
    time_index = 0
    data_d = time.replace("days", "day").split("day, ")
    if len(data_d) == 2:
        """ abs() return absolute value """
        d = abs(int(data_d[0])) * 24
        time_index = 1    
    """ Convert hours into decimal numbers; remove seconds using [: - 3] """
    data = data_d[time_index][: - 3].split(":")
    h = data[0]
    m = data[1]
    hours_number = d + int(h) + (int(m) / 60)
    """ Round to the nearest integer """
    hours_slept = round(hours_number)
    write_time(date_one, hours_slept)
    return calendar.set_data()