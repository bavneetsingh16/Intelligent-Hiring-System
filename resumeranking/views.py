from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django import template
from django.template import *
from django.core.files.storage import FileSystemStorage
#import twitter_streaming as ts
#import retreive as ret
import json
import requests
from django.core.files import File
#from django.views.decorators.csrf import csrf_protect
#@csrf_protect
from django.views.decorators.csrf import csrf_exempt


l1=[]
cs=[]
finance=[]
arts=[]
management=[]
programming=[]
engineering=[]
l1=[]
scorelist=[]
final=[]
setl2=[]


@csrf_exempt


#host='https://search-twitterdata-7pjdmgnouvfgjif4lryzj3pgdi.us-east-1.es.amazonaws.com/twitter/_search'

def index(request):
    import boto3
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    table = dynamodb.Table('users')
    #return render(request,'upload.html')
    if request.method == 'GET':
        return render(request,'index.html')
    if request.method == 'POST':

         name2 = request.POST['login']
         name3=str(name2)
         signup='signup'
         login='login'
         if(name2==login):
             email = request.POST.get('username','')
             password = request.POST.get('password','')
             print ("username is ", email, "password is ", password)
             email=str(email)
             password=str(password)
             s=''
             s=email+password
             response = table.get_item(
                    Key={
                        'userid': email
                    }
                )
             if(len(response)==2): 
                item = response['Item']['password']
                if(password==item):
                    return render(request,"upload.html")
                else:
                    print("Invalid password")
                    return render(request,'index.html',{'s':["invalid password",'0']})
             else:
                print("Invalid Username")
                s1="invalid username"
                return render(request,'index.html',{'s':["invalid username",'0']})
             #return render(request,"value.html",{'s':s})
         if(name2==signup):
             first_name=request.POST.get('first','')
             last_name=request.POST.get('last','')
             email = request.POST.get('newemail','')
             password = request.POST.get('newpassword','')
             print ("first name is ", first_name, "last name is ", last_name)
             table.put_item(
                   Item={
                        'userid': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'password': password,
                    }
                )
             #s=''
             #s=first_name+last_name
             #c={}
             #c.update(csrf(request))
             #return render(request,"value.html",{'s':s})
             #return render(request,"form.html")
             return render(request,"upload.html")

@csrf_exempt
def index2(request):
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
    import boto3 
    import boto
    import sys, os
    import zipfile
    s3 = boto3.resource('s3',region_name='us-east-1')
    myfile = request.FILES['file']
    file_name=myfile.name
    fs = FileSystemStorage(location='resumeranking/ResumeZip/')
    filename = fs.save(myfile.name, myfile)
    s3.meta.client.upload_file('resumeranking/ResumeZip/Archive.zip', 'resumezipbucket2', 'Archive.zip')
    LOCAL_PATH = 'resumeranking/FromS3/'
    conn = S3Connection('','')
    bucket = conn.get_bucket('resumezipbucket2')
    l = []
    bucket_list = bucket.list()
    for l in bucket_list:
        keyString = str(l.key)
        if not os.path.exists(LOCAL_PATH + keyString):
            l.get_contents_to_filename(LOCAL_PATH + keyString)
    zip_ref = zipfile.ZipFile(LOCAL_PATH+'/'+file_name, 'r')
    zip_ref.extractall('resumeranking/ResumeSamples/')
    zip_ref.close()
    return render(request,"choose.html")
    #return render(request,"upload.html")
    #return render_template('upload.html', field='_all')
    

@csrf_exempt
def choices(request):
    global finance
    global arts
    global programming
    global management
    global cs
    global engineering
    global l1

    finance=request.POST.getlist('finance2')
    arts=request.POST.getlist('arts')
    programming=request.POST.getlist('Programming')
    management=request.POST.getlist('management')
    cs=request.POST.getlist('cs')
    engineering=request.POST.getlist('engineering')
    degree=['ba']
    print("cs****",cs)
    l1.append(programming)
    l1.append(cs)
    l1.append(engineering)
    l1.append(finance)
    l1.append(management)
    l1.append(arts)
    l1.append(degree)
    
    print("finance:",request.POST.getlist('finance2'))
    print("arts:",request.POST.getlist('arts'))
    print("programming:",request.POST.getlist('Programming'))
    print("management:",request.POST.getlist('management'))
    print("cs:",request.POST.getlist('cs'))
    print("engineering:",request.POST.getlist('engineering'))
    
    import pdfquery
    from io import StringIO
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
      # for Python 2.5 and 2.6
    import urllib
    # import PyPDF2
    import re, collections
    import boto3

    #from tex import latex2pdf
    import os
    import difflib
    import subprocess
    cs=0
    eng=0
    fin=0
    man=0
    art=0
    def convert(fname, pages=None):
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)

        infile = open(fname, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
        return text

    #print(convert("results.pdf"))

    def init():
        ############################################################
        ### Convert pdf to txt with pdf miner and start a write file
        ############################################################

        # input the file name
        filename = "resumeranking/ResumeSamples/"
        print(filename)
        global finance
        global arts
        global programming
        global management
        global cs
        global engineering
        global l1
        print("cs.....",cs)
        degree=['ba']
        #l1.append(programming)
        #l1.append(cs)
        #l1.append(engineering)
        #l1.append(finance)
        #l1.append(management)
        #l1.append(arts)
        #l1.append(degree)
        #print(l1)
        cats=l1[:]

        # creates an empty tex file with the results in it
        fout = open("results.tex", "w")
        fout.write("\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\
        \\title{Results}\n\\begin{document}\n\n")
        fout.close()

        # need this to work in case no input
        if filename == " ":
            print("zero")
            return ("", "")
        elif os.path.isdir(filename):
            resumes = []
            l = []
            l.append(os.listdir("resumeranking/ResumeSamples/"))
            #print(l)
            l1 = l[0]
            l1 = l1[1:]
            #print(l1)
            #resumes=l1[:]
            filename="resumeranking/ResumeSamples/"
            for i in l1:
                #print(i)
                j=filename+" "+i
                resume = convert(os.path.join(filename, i))
                #print("resume",resume)
                resumes.append(resume)
            #for doc in os.listdir(filename):
               # if doc.endswith(".pdf"):
               #     resume = convert(os.path.join(filename, doc))
               #     print("resume",resume)
               #     resumes.append(resume)
               # else:
               #     resume = readFile(os.path.join(filename, doc)).lower()
                #    resumes.append(resume)
            #print(resumes)
            return (resumes, cats)
        # is .pdf; need to convert to .txt
        elif filename.endswith(".pdf"):
            resume = convert(filename)
        else:
            resume = readFile(filename).lower()
        # return resume as a string with different sections

        return (resume, cats)

    def programmingScore1(resume, progWords=None):
        fout = open("results.tex", "a")
        fout.write("\\textbf{Programming Languages:} \\\\\n")

        if (progWords == None):
            return 0
        else:
            programming = progWords
        programmingTotal = 0

        for i in range(len(programming)):
            if programming[i].lower() in resume.lower() != -1:
                programmingTotal += 1
                #if not ("#" in programming[i]):
                    #fout.write(programming[i] + ", ")

        fout.close()

        progScore = min((programmingTotal) / (len(progWords)), 1.0) * 5.0
        print("progscore",progScore)

        return progScore


    def softwareScore(resume, csWords=None):
        print(csWords)
        if (csWords == None):
            return 0
        else:
            csKeyWords = csWords

        csWordScore = []
        for i in range(len(csKeyWords)):
            csWordScore.append(0)
            if csKeyWords[i].lower() in (resume.lower()) != -1:
                (csWordScore[i]) += 1

        print("wordscore",csWordScore)
        print(len(csKeyWords))
        print((float)(sum(csWordScore) + 10) / (len(csKeyWords)))
        csScore = min((float)(sum(csWordScore)) / (len(csKeyWords)), 1.0) * 25.0
        #csScore = (float)(25.0/((float)(sum(csWordScore) + 10) / (len(csKeyWords))))
        print(csScore)
        return csScore


    def engineeringScore(resume, engWords=None):
        if (engWords == None):
            return 0
        else:
            engineeringKeyWords = engWords

        engWordScore = []
        for i in range(len(engineeringKeyWords)):
            engWordScore.append(0)
            if engineeringKeyWords[i].lower() in (resume.lower()) != -1:
                (engWordScore[i]) += 1

        engScore = min((float)(sum(engWordScore)) / len(engineeringKeyWords), 1.0) * 25.0

        return engScore


    def financeScore(resume, finWords=None):
        if finWords == None:
            return 0
        else:
            financeKeyWords = finWords

        finWordScore = []
        for i in range(len(financeKeyWords)):
            finWordScore.append(0)
            if financeKeyWords[i].lower() in (resume.lower()) != -1:
                (finWordScore[i]) += 1

        finScore = min((float)(sum(finWordScore)) / len(financeKeyWords), 1.0) * 25.0

        return finScore


    def managementScore(resume, manWords=None):
        if manWords == None:
            return 0
        else:
            managementKeyWords = manWords

        manWordScore = []
        for i in range(len(managementKeyWords)):
            manWordScore.append(0)
            if managementKeyWords[i].lower() in (resume.lower()) != -1:
                (manWordScore[i]) += 1

        manScore = min((float)(sum(manWordScore)) / len(managementKeyWords), 1.0) * 25.0

        return manScore


    def artsScore(resume, artWords=None):
        if artWords == None:
            return 0
        else:
            artsKeyWords = artWords

        artsWordScore = []
        for i in range(len(artsKeyWords)):
            artsWordScore.append(0)
            if artsKeyWords[i].lower() in (resume.lower()) != -1:
                (artsWordScore[i]) += 1

        artsScore = min((float)(sum(artsWordScore)) / len(artsKeyWords), 1.0) * 25.0

        return artsScore


    def mainCategoryAndScore(resume, progWords=None, csWords=None, engWords=None, finWords=None, manWords=None,
                             artWords=None):
        global cs
        global eng
        global fin
        global man
        global art
        cs = softwareScore(resume, csWords)
        eng = engineeringScore(resume, engWords)
        fin = financeScore(resume, finWords)
        man = managementScore(resume, manWords)
        art = artsScore(resume, artWords)
        global final
        final = []
        final.append('Software score: '+str(cs))
        final.append('Engineering Score: '+str(eng))
        final.append('Financial Score: '+str(fin))
        final.append('Management Score: '+str(man))
        final.append('Arts Score: '+str(art))
        average = getCategoriesAverage(resume)
        final.append('Avergae Score: '+str(average))
        oall=overall(resume)
        final.append('Overall Score: '+str(oall))
        final.append('Programming Score: '+str(programmingScore1(resume,progWords)))

        fout = open("results.tex", "a")
        fout.write("\\textbf{Software:} " + str(cs) + " (out of 25)\\\\\n\
    \\textbf{Engineering: } " + str(eng) + " (out of 25)\\\\\n\
    \\textbf{Finance:} " + str(fin) + " (out of 25)\\\\\n\
    \\textbf{Management Skills:} " + str(man) + " (out of 25)\\\\\n\
    \\textbf{Arts:} " + str(art) + " (out of 25)\\\\\n")

        fout.close()

        a = ["computer science", "engineering", "finance", "business management", "arts"]
        b = [cs, eng, fin, man, art]

        maxscore = b[0]
        maxindex = 0

        for x in range(len(b)):
            if (b[x]) > maxscore:
                maxindex = x
                maxScore = b[x]

        c = list(zip(a, b))

        return c[maxindex]


    def getCategoriesAverage(resume):
        global cs
        global eng
        global fin
        global man
        global art
        #cs = softwareScore(resume)
        #eng = engineeringScore(resume)
        #fin = financeScore(resume)
        #man = managementScore(resume)
        #art = artsScore(resume)

        average = (cs + eng + fin + man + art - min(cs, eng, fin, man, art)) / 4.0

        return min(1.0, average / 15.0) * 15.0


    def printAllCategoryScores(resume):
        global cs
        global eng
        global fin
        global man
        global art
        #cs = softwareScore(resume)
        #eng = engineeringScore(resume)
        #fin = financeScore(resume)
        #man = managementScore(resume)
        #art = artsScore(resume)

        a = ["computer science", "engineering", "finance", "business management", "arts"]
        b = [cs, eng, fin, man, art]

        c = zip(a, b)

        print(c)

        return


    def printCategoriesAverage(resume):
        print(getCategoriesAverage(resume))
        return

    # print(programmingScore(pdftotextmaybe.convert("sample3.pdf")))
    # printAllCategoryScores(pdftotextmaybe.convert("sample3.pdf"))
    # printCategoriesAverage(pdftotextmaybe.convert("sample3.pdf"))

    ## Nazli Uzgur

    def publish(scorelist):
        sns = boto3.resource('sns',region_name='us-east-1', aws_access_key_id='', aws_secret_access_key='')
        topic = sns.Topic('arn:aws:sns:us-east-1:727407189833:notifications')
        response = topic.publish(
            Message=str(scorelist),
            Subject='Resume Ranking'
        )







    def category(resume, progWords=None, csWords=None, engWords=None, finWords=None, manWords=None, artWords=None):
        # Return the category that appears the most
        (cat, score) = mainCategoryAndScore(resume, progWords, csWords, engWords, finWords, manWords, artWords)
        return (cat, score)


    def overall(resume):
        overall = getCategoriesAverage(resume)
        fout = open("results.tex", "a")
        fout.write("\\textbf{Average Score: } " + str(tenOverall(overall)) + "\\\\\n")
        fout.close()
        return overall


    def tenCategory(score):
        return score / 2.5


    def tenOverall(score):
        return score / 1.5


    def programmingScore(resume):
        global l1
        proScore = programmingScore1(resume,l1[0])
        print("proScore",proScore)
        fout = open("results.tex", "a")
        fout.write("score: " + str(proScore) + "\\\\\n")
        #fout.write("score: " + str(tenProgScore(proScore)) + "\\\\\n")
        fout.close()
        return proScore


    def tenProgScore(score):
        return score * 2


    def gpaScoreCalculator(gpa):
        gpa_unweighted = gpa / 4.00
        gpa_scaled = gpa_unweighted
        return gpa_scaled


    def gpaScore(word_tokens):
        score = 0

        gpaFound = False
        for token in word_tokens:
            if "gpa" in token.lower():
                index = word_tokens.index(token)
                try:
                    if "/" in word_tokens[index + 1]:
                        words = word_tokens[index + 1].split("/")
                        gpa = float(words[0])
                        score = gpaScoreCalculator(gpa)
                        gpaFound = True
                    else:
                        gpa = float(word_tokens[index + 1])
                        score = gpaScoreCalculator(gpa)
                        gpaFound = True
                except:
                    if "/" in word_tokens[index - 1]:
                        words = word_tokens[index - 1].split("/")
                        gpa = float(words[0])
                        score = gpaScoreCalculator(gpa)
                        gpaFound = True
                    else:
                        gpa = float(word_tokens[index - 1])
                        score = gpaScoreCalculator(gpa)
                        gpaFound = True

        # a resume with a GPA might indicate a lower GPA
        fout = open("results.tex", "a")
        if gpaFound == False:
            fout.write("\\textbf{GPA: not found}\\\\\n")
            score = gpaScoreCalculator(2.5)
        else:
            fout.write("\\textbf{GPA: " + str(gpa) + "}\\\\\n")
        fout.close()
        global final               
        final.append('GPA Score: '+str(score))
        return score


    def collegeScore(word_tokens):
        university = ["Carnegie Mellon University", "Princeton University",
                      "Harvard University", "Yale University", "Columbia University",
                      "Stanford University", "University of Chicago",
                      "Massachusetts Institute of Technology", "Duke University",
                      "University of Pennsylvania", "California Institute of Technology",
                      "Johns Hopkins University", "Dartmouth College", "Northwestern University",
                      "Brown University", "Cornell University", "Vanderbilt University",
                      "Washington University in St. Louis", "Rice University",
                      "University of Notre Dame", "University of California-Berkeley",
                      "Emory University", "Georgetown University",
                      "University of California-Los Angeles", "University of Southern California",
                      "University of Virginia", "Tufts University", "Wake Forest University",
                      "University of Michigan-Ann Arbor", "Boston College",
                      "University of North Carolina-Chapel Hill", "New York University", "University of Rochester",
                      "Brandeis University", "College of William and Mary", "Georgia Institute of Technology",
                      "Case Western Reserve University", "University of California-Santa Barbara",
                      "University of California-San Diego", "Boston University", "Rensselaer Polytechnic Institute",
                      "Tulane University", "University of California-Davis", "University of Illinois-Urbana-Champaign",
                      "University of Wisconsin-Madison", "Lehigh University", "Northeastern University",
                      "Pennsylvania State University-University Park", "University of Florida", "University of Miami",
                      "Ohio State University-Columbus", "Pepperdine University", "University of Texas-Austin",
                      "University of Washington", "Yeshiva University", "George Washington University",
                      "University of Connecticut", "University of Maryland-College Park",
                      "Worchester Polytechnic Institute", "Clemson University", "Purdue University-West Lafayette",
                      "Southern Methodist University", "Syracuse University", "University of Georgia",
                      "Brigham Young University-Provo", "Fordham University", "University of Pittsburgh",
                      "University of Minnesota-Twin Cities", "Texas A&M University-College Station", "Virginia Tech",
                      "American University", "Baylor University",
                      "Rutgers, The State University of New Jersey-New Brunswick",
                      "Clark University", "Colorado School of Mines", "Indiana University-Bloomington",
                      "Michigan State University", "Stevens Institute of Technology", "University of Delaware",
                      "University of Massachusetts-Amherst", "Miami University-Oxford", "Texas Christian University",
                      "University of California-Santa Cruz", "University of Iowa", "Marquette University",
                      "University of Denver", "University of Tulsa", "Binghamton University-SUNY",
                      "North Carolina State University-Raleigh", "Stony Brook University-SUNY",
                      "SUNY College of Environmental Science and Forestry", "University of Colorado-Boulder",
                      "University of San Diego", "University of Vermont", "Florida State University",
                      "Saint Louis University",
                      "University of Alabama", "Drexel University", "Loyola University Chicago",
                      "University at Buffalo-SUNY",
                      "Auburn University", "University of Missouri", "University of Nebraska-Lincoln",
                      "University of New Hampshire", "University of Oregon", "University of Tennessee",
                      "Illinois Institute of Technology", "Iowa State University", "University of Dayton",
                      "University of Oklahoma", "University of San Francisco", "University of South Carolina",
                      "University of the Pacific", "Clarkson University", "Duquesne University", "Temple University",
                      "University of Kansas", "University of St. Thomas", "University of Utah", "University of Arizona",
                      "University of California-Riverside", "The Catholic University of America", "DePaul University",
                      "Michigan Technological University", "Seton Hall University", "Colorado State University",
                      "New School",
                      "Arizona State University-Tempe", "Louisiana State University-Baton Rouge",
                      "University at Albany-SUNY",
                      "University of Arkansas", "University of Illinois-Chicago", "University of Kentucky",
                      "George Mason University", "Hofstra University", "Howard University", "Ohio University",
                      "Oregon State University", "New Jersey Institute of Technology",
                      "Rutgers, The State University of New Jersey-Newark", "University of Cincinnati",
                      "University of Mississippi", "University of Texas-Dallas", "Washington State University",
                      "Kansas State University", "Missouri University of Science & Technology", "St. John Fisher College",
                      "Illinois State University", "Oklahoma State University", "San Diego State University",
                      "University of Alabama-Birmingham", "Adelphi University", "Southern Illinois University-Carbondale",
                      "St. John's University", "University of Maryland-Baltimore County",
                      "University of Massachusetts-Lowell",
                      "University of South Florida", "Virginia Commonwealth University", "University of La Verne",
                      "Biola University", "Florida Institute of Technology", "Immaculata University",
                      "Maryville University of St. Louis", "Mississippi State University", "University of Hawaii-Manoa",
                      "University of Rhode Island", "Ball State University", "Texas Tech University",
                      "University of Central Florida", "University of Idaho", "University of Louisville",
                      "University of Maine",
                      "University of Wyoming", "Andrews University", "Azusa Pacific University", "Edgewood College",
                      "Kent State University", "West Virginia University", "Pace University",
                      "St. Mary's University of Minnesota", "University of New Mexico", "University of North Dakota",
                      "University of South Dakota", "Bowling Green State University", "North Dakota State University",
                      "South Dakota State University", "University of Alabama-Huntsville", "University of Houston",
                      "University of Nevada-Reno", "University of North Carolina-Greensboro", "Western Michigan University",
                      "Widener University", "Central Michigan University", "East Carolina University",
                      "South Carolina State University", "University of Missouri-Kansas City",
                      "University of North Carolina-Charlotte", "Ashland University",
                      "Indiana University-Purdue University-Indianapolis", "Louisiana Tech University",
                      "New Mexico State University", "University of Colorado-Denver"]
        short_words = ["university", "for", "and", "get", "the", "art", "ice", "town", "park", "van", "los"]
        i = 0
        global final
        fout = open("results.tex", "a")
        for college in university:
            for word in word_tokens:
                if ((word.lower() not in short_words) and (word in college) and (len(word) > 2)):
                    fout.write("\\textbf{" + college + "}")

                    i = university.index(college)
                    i = i + 1
                    break
            if (i != 0):
                break
        score = ((200 - i) / 200.0) * 15
        fout.write(" \\textbf{score:} " + str(tenUniversity(score)) + "\\\\\n")
        fout.close()
        final.append('University Score: '+str(score))
        return score


    def tenUniversity(score):
        return score / 1.5


    def wordCountScore(tokens):
        score = 10
        # number of words
        count = 0
        # word count
        for tok in tokens:
            if tok != "":
                count += 1
        # 475 words -> average amount of words on one page
        if count == 400:
            score -= 0
        # accounts for resumes too short and too long
        else:
            score -= min(abs(400 - count) / 20, 5)
        return score


    def degreeScore(word_tokens):
        score = 10
        desiredDegree = cats[6]
        desiredDegreelower=[x.lower() for x in desiredDegree]
        word_tokens_lower = [x.lower() for x in word_tokens]
        # searches for similar words
        #degree = difflib.get_close_matches(desiredDegree, word_tokens_lower)
        #close_match_fail = False
        #close_match =
        for i in range(len(desiredDegree)):
            if desiredDegreelower[i] in word_tokens_lower != -1:
                score += 10
        return score




    def sectionScore(resume):
        section_tokens = input_file_words(resume, [])
        currentIndex = -1
        wordCount = [0, 0, 0]
        for x in section_tokens:
            x = x.lower()
            if (x.strip("!@#$%^&*()_+|}{:?") in ["work experience", "employment", "experience"] and currentIndex != 0):
                currentIndex = 0
            elif (x.strip("!@#$%^&*()_+|}{:?") in ["publications", "projects", "research"] and currentIndex != 1):
                currentIndex = 1
            elif (x.strip("!@#$%^&*()_+|}{:?") in ["leadership", "leadership experience"] and currentIndex != 2):
                currentIndex = 2
            elif (x.strip("!@#$%^&*()_+|}{:?") in ["education", "activites", "skils", "interests", "extracurricular",
                                                   "honors", "references", "awards", "acheivements"]):
                currentIndex = -1
            else:
                wordCount[currentIndex] += 1

        return min(((sum(wordCount) - min(wordCount))) / 450.0, 1.0) * 10

    def input_file_lines(input_text, tokens):
        tokens = input_text.splitlines();
        return tokens

    def input_file_words(input_text, tokens):
        tokens = input_text.split();
        return tokens

    def main(resume, cats):
        # initialize variables
        # have the words as tokens in a list
        tokens = input_file_lines(resume, [])
        word_tokens = input_file_words(resume, [])
        score = 0

        # get email
        email = ""
        global final
        for token in word_tokens:
            if "@" in token:
                email = token
                final.append('Email: '+str(email))
                break

        fout = open("results.tex", "a")
        fout.write("\\section{" + email + "}\n")
        fout.close()
        # category score
        (cat, category_score) = category(resume, cats[0], cats[1], cats[2], cats[3], cats[4], cats[5])

        # overall score
        overall_score = overall(resume)

        # programming languages score
        programming_score = programmingScore(resume)

        # GPA score
        gpa_score = gpaScore(word_tokens)

        # university score
        college_score = collegeScore(word_tokens)

        # word count score
        word_count_score = wordCountScore(tokens)

        # degree score
        degree_score = degreeScore(word_tokens)

        # sectional score
        section_score = sectionScore(resume)

        print("Finished parsing.")
        score = category_score + overall_score + programming_score + \
                gpa_score + college_score + word_count_score + \
                degree_score + section_score
        global scorelist
        scorelist.append(final)
        scorelist.sort(key=lambda x:x[6],reverse=True)

        fout = open("results.tex", "a")
        fout.write("\\textbf{Best category: } " + cat + "\\\\\n\
    \\textbf{Overall Score: }" + str(score / 10.0) + " (out of 10)")
        fout.close()

        return (cat, score, email)
    def readFile(filename, mode="rt"):
        # rt = "read text"
        with open(filename, mode) as fin:
            return fin.read()

    (resume,cats) = init()

    def printlist():
        global scorelist
        j=1
        l4=[]
        s=''
        s3=''
        s1=set(scorelist[len(scorelist)-1])
        print("!!!!!!!!!!!!!!!!!!!")
        for i in scorelist:
            print(j)
            print(len(i))
            print(i)
            if(len(i)>10):
                print(i[10])
                s=s+str(i[10])+"\n"
                #l4.append[s]
                #print("l4",l4)
            for k in i:
                s3=s3+k+"\n"
            
            j=j+1
            #l4.append[i[len(i)-1]]
            s3=s3+"\n"+"\n"+"\n"
        print("!!!!!!!!!!!!!!!!!!!")
        print(s)
        publish(s)
        printlist2(s3)

    def printlist2(s3):
        with open("resumeranking/static/css/hello.txt",'a+') as f:
            f.write(s3)

    if type(resume) == list:
        for i in range(len(resume)):
            print((main(resume[i], cats)))
        fout = open("results.tex", "a")
        fout.write("\\end{document}")
        fout.close()
        #subprocess.call('/Library/TeX/texbin/pdflatex', 'results.tex', shell=False)
        #os.system("/Library/TeX/texbin/pdflatex results.tex")
        printlist()


    elif resume != "":
        print(main(resume, cats))
        fout = open("results.tex", "a")
        fout.write("\\end{document}")
        fout.close()
        #proc = subprocess.Popen(['pdflatex', 'results.tex'])
        #proc.communicate()
        #subprocess.call('/Library/TeX/texbin/pdflatex', 'results.tex')
        #os.system("/Library/TeX/texbin/pdflatex results.tex")
        printlist()

    #source="hello.txt"
    #dest="resumeranking/static/Pdf/hello.txt"
    #os.rename(source,dest)

    return render(request,"pdffile.html")
    #return render(request,"value.html",{'s':request.POST.getlist('finance2')})


@csrf_exempt
def logout(request):
    import boto3
    import os



    folder = 'resumeranking/ResumeZip'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
               
           

            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
           
    folder = 'resumeranking/ResumeSamples'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
           
               
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
           
    folder = 'resumeranking/FromS3'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
           
               
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
           
    #os.remove("resumeranking/static/css/hello.txt")
    #f=open("resumeranking/static/css/hello.txt",'r+')
    #f.truncate(f)
    #folder = 'resumeranking/static/Pdf'
    #for the_file in os.listdir(folder):
        #file_path = os.path.join(folder, the_file)
        #try:
            #if os.path.isfile(file_path):
              #  os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        #except Exception as e:
           # print(e)

    client = boto3.client('s3',region_name='us-east-1')
    client.delete_object(Bucket='resumezipbucket2', Key='Archive.zip')
    return render(request,'index.html')
