import csv
from textblob import TextBlob
from datetime import datetime, timedelta


def dataframe_from_csv(raw_data_file):
    infile = open(raw_data_file, 'r')
    reader = csv.reader(infile)
    a = []
    for row in reader:
        a.append(row)
    infile.close()
    return a


def mental_health_dataframe():
    raw_data_file = 'data/mental-health.csv'
    return dataframe_from_csv(raw_data_file)


def adjustments_dataframe():
    raw_data_file = 'data/adjustments.csv'
    return dataframe_from_csv(raw_data_file)


def organisational_culture_dataframe():
    raw_data_file = 'data/organisational-culture.csv'
    return dataframe_from_csv(raw_data_file)


def work_self_confidence_dataframe():
    raw_data_file = 'data/work-self-confidence.csv'
    return dataframe_from_csv(raw_data_file)


class AnswerMappings:
    mental_health = {
        'Did not apply to me at all': 0,
        'Applied to me to some degree': 1,
        'Applied to me to a considerable degree, or a good part of the time': 2,
        'Applied to me a good part of the time': 2,
        'Applied to me to a considerable degree': 2,
        'Applied to me very much, or most of the time': 3,
        'Applied to me very much': 3,
    }

    organisational_culture = {
        'Strongly disagree': 0,
        'Somewhat disagree': 1,
        'Somewhat agree': 2,
        'Strongly agree': 3,
    }

    work_self_confidence = {
        'Not confident at all': 1,
        'A little': 2,
        'Moderate': 3,
        'A lot': 4,
        'Completely confident': 5,
    }


mental_health_questions = {
    1: "I found it hard to wind down",
    2: "I was aware of dryness of my mouth",
    3: "I couldn't seem to experience any postive feelings at all",
    4: "I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion)",
    5: "I found it difficult to work up the initiative to do things",
    6: "I tended to over-react to situations",
    7: "I experienced trembling (e.g. in the hands)",
    8: "I felt that I was using a lot of nervous energy",
    9: "I was worried about situations in which I might panic and make a fool of myself",
    10: "I felt that I had nothing to look forward to",
    11: "I found myself getting agitated",
    12: "I found it difficult to relax",
    13: "I felt down-hearted and blue",
    14: "I was intolerant of anything that kept me from getting on with what I was doing",
    15: "I felt I was close to panic",
    16: "I was unable to become enthusiastic about anything",
    17: "I felt I wasn't worth much as a person",
    18: "I felt that I was rather touchy",
    19: "I was aware of the actions of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat)",
    20: "I felt scared without any good reason",
    21: "I felt that life was meaningless",
}

def get_adjustments_sentiments_summary(rows, id):
    summary = []
    headers = rows[0]
    for row in rows[1:]:
        if row[headers.index('Username')] == id:
            timestamp = row[headers.index('Date')]
            questions = []
            for i in range(2, len(row)):
                question = headers[i]
                response = row[i]

                # polarity score is a float within the range [-1.0, 1.0]
                # negative value => negative text, positive value i=> text is positive.

                # subjectivity is a float within the range [0.0, 1.0] where
                # 0.0 is very objective and 1.0 is very subjective.

                response_blob = TextBlob(response)
                sentiment = {
                    'polarity'      : response_blob.sentiment.polarity,
                    'subjectivity'  : response_blob.sentiment.subjectivity,
                    'word_count'    : len(response_blob.words),
                }

                questions.append({
                    'question'  :question,
                    'sentiment' :sentiment,
                })
            summary.append({
                'date'      :  timestamp,
                'questions' :  questions,
            })
    return summary

def fix_broken_data(x):
   return int(x) if x else 0


# Depression = (sum of questions 3, 5, 10, 16, 17, 21) x 2
# Anxiety = (sum of questions 2, 4, 7, 9, 15, 19, 20) x 2
# Stress = (sum of questions 1, 6, 8, 11, 12, 14, 18) x 2


def get_mental_health_summary(rows, id):
    summary = []
    headers = rows[0]
    for row in rows[1:]:
        if row[headers.index('Username')] == id:
            d = dict()
            # d["date"] = row[headers.index('Date')].replace('th ',' ').replace('st ',' ').replace('nd ',' ').replace('Augu','August')
            d["date"] = row[2]
            depression = ((fix_broken_data(row[5]) + fix_broken_data(row[7]) + fix_broken_data(row[12]) +
                           fix_broken_data(row[18]) + fix_broken_data(row[19]) + fix_broken_data(row[23])) * 2)

            anxiety = ((fix_broken_data(row[4]) + fix_broken_data(row[6]) + fix_broken_data(row[9]) +
                           fix_broken_data(row[11]) + fix_broken_data(row[17]) + fix_broken_data(row[21]) +
                             fix_broken_data(row[22])) * 2)

            stress  = ((fix_broken_data(row[3]) + fix_broken_data(row[8]) + fix_broken_data(row[10]) +
                           fix_broken_data(row[13]) + fix_broken_data(row[14]) + fix_broken_data(row[16]) +
                             fix_broken_data(row[20])) * 2)
            d["depression"] = depression
            d["anxiety"]    = anxiety
            d["stress"]     = stress
            d["depression_severity"] = get_severity('depression',depression)
            d["anxiety_severity"]    = get_severity('anxiety'   ,anxiety)
            d["stress_severity"]     = get_severity('stress'    ,stress)
            summary.append(d)
    return summary

# Severity ratings
# Severity  Depression  Anxiety   Stress
# --------|-----------|----------|---------|
# Normal    0-9         0-7       0-14
# Mild      10-13       8-9       15-18
# Moderate  14-20       10-14     19-25
# Severity  21-27       15-19     26-33
# Extremely 28+         20+       34+
# ...Severe

def get_severity(attribute, value):
    if (value < 0):
        return ('Invalid value: ' + str(value))
    if (attribute  == 'depression'):
        if(value >= 28):
            return 'Extremely Severe'
        if(value >= 21):
            return 'Severe'  
        if(value >= 14):
            return 'Moderate' 
        if(value >= 10):
            return 'Mild' 
        if(value >= 0):
            return 'Normal'   
    if (attribute  == 'anxiety'):
        if(value >= 20):
            return 'Extremely Severe'
        if(value >= 15):
            return 'Severe'  
        if(value >= 10):
            return 'Moderate' 
        if(value >= 8):
            return 'Mild' 
        if(value >= 0):
            return 'Normal' 

    if (attribute  == 'stress'):
        if(value >= 34):
            return 'Extremely Severe'
        if(value >= 26):
            return 'Severe'  
        if(value >= 19):
            return 'Moderate' 
        if(value >= 15):
            return 'Mild' 
        if(value >= 0):
            return 'Normal'  

    return ('Unknown attribute: ' + str(attribute))

def get_work_self_confidence_summary(rows, id):
    summary = []
    headers = rows[0]
    for row in rows[1:]:
        if row[headers.index('Username')] == id:
            learning = (fix_broken_data(row[7]) + fix_broken_data(row[15]) + fix_broken_data(row[25]) + fix_broken_data(row[28]))/4
            problem_solving = (fix_broken_data(row[12]) + fix_broken_data(row[17]) + fix_broken_data(row[18]) + fix_broken_data(row[19]) + fix_broken_data(row[24]) + fix_broken_data(row[26]))/6
            pressure = (fix_broken_data(row[8]) + fix_broken_data(row[13]) + fix_broken_data(row[22]) + fix_broken_data(row[30]))/4
            role_expectations = (fix_broken_data(row[3]) + fix_broken_data(row[5]) + fix_broken_data(row[11]) + fix_broken_data(row[23]))/4
            teamwork = (fix_broken_data(row[4]) + fix_broken_data(row[10]) + fix_broken_data(row[16]) + fix_broken_data(row[27]))/4
            sensitivity = (fix_broken_data(row[10]) + fix_broken_data(row[29]) + fix_broken_data(row[31]) + fix_broken_data(row[32]))/4
            work_politics = (fix_broken_data(row[6]) + fix_broken_data(row[9]) + fix_broken_data(row[14]) + fix_broken_data(row[21]))/4

            summary.append({
                "date": row[headers.index('Date')].replace('th ',' ').replace('st ',' ').replace('nd ',' ').replace('Augu','August'),
                "learning": learning,
                "problem_solving": problem_solving,
                "pressure": pressure,
                "role_expectations": role_expectations,
                "teamwork": teamwork,
                "sensitivity": sensitivity,
                "work_politics": work_politics
            })
    
    return summary


# admin overviews


def get_admin_mental_health_summary(rows):
    # for each week, get max, min, avg
    # date format: 29th October 2019 11:54 am
    weeks = {}

    for row in rows[1:]:
        d = dict()

        # get week start for grouping
        date = row[2].replace('th ',' ').replace('st ',' ').replace('nd ',' ').replace('Augu','August')
        dt = datetime.strptime(date, '%d %B %Y %I:%M %p')
        week_start = dt - timedelta(days=dt.weekday())
        date = week_start.strftime('%d %B %Y %I:%M %p')

        d["date"] = date

        depression = ((fix_broken_data(row[5]) + fix_broken_data(row[7]) + fix_broken_data(row[12]) +
                        fix_broken_data(row[18]) + fix_broken_data(row[19]) + fix_broken_data(row[23])) * 2)

        anxiety = ((fix_broken_data(row[4]) + fix_broken_data(row[6]) + fix_broken_data(row[9]) +
                        fix_broken_data(row[11]) + fix_broken_data(row[17]) + fix_broken_data(row[21]) +
                            fix_broken_data(row[22])) * 2)

        stress  = ((fix_broken_data(row[3]) + fix_broken_data(row[8]) + fix_broken_data(row[10]) +
                        fix_broken_data(row[13]) + fix_broken_data(row[14]) + fix_broken_data(row[16]) +
                            fix_broken_data(row[20])) * 2)

        d["depression"] = depression
        d["anxiety"]    = anxiety
        d["stress"]     = stress
        d["depression_severity"] = get_severity('depression',depression)
        d["anxiety_severity"]    = get_severity('anxiety'   ,anxiety)
        d["stress_severity"]     = get_severity('stress'    ,stress)


        if date in weeks:
            weeks[date].append(d)
        else:
            weeks[date] = [d]

    # TODO : calculate avgs from all data
    return [weeks]
