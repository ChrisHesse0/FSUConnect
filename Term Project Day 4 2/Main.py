from flask import Flask, render_template, request, redirect
app = Flask(__name__)
import sqlite3
import Setup
import random

user = ""
viewing = []
already_seen = []


#Function used to Encrypt the username and password with a viginere cipher
def Encrypt(inp):
    keyLower = "briancooperchrisdylanbriancooperchrisdylanbriancooperchrisdylanbriancooperchrisdylan"
    keyUpper = keyLower.upper()
    encrypted = ""
    i = 0
    for j in range(len(inp)):
        if inp[j] == ' ':
            encrypted += ' '
        else:
            if inp[j].isalpha():
                if inp[j].islower():
                    if (ord(inp[j]) % 97) + (ord(keyLower[i]) % 97) >= 26:
                        encrypted += chr(((ord(inp[j]) % 97) + (ord(keyLower[i]) % 97)) + 97 - 26)
                    else:
                        encrypted += chr(((ord(inp[j]) % 97) + (ord(keyLower[i]) % 97)) + 97)
                if inp[j].isupper():
                    if (ord(inp[j]) % 65) + (ord(keyUpper[i]) % 65) >= 26:
                        encrypted += chr(((ord(inp[j]) % 65) + (ord(keyUpper[i]) % 65)) + 65 - 26)
                    else:
                        encrypted += chr(((ord(inp[j]) % 65) + (ord(keyUpper[i]) % 65)) + 65)
                i += 1
            else:
                encrypted += inp[j]
    return encrypted

#Function used to decrypt username and password with a viginere cipher
def Decrypt(encrypted):
    keyLower = "briancooperchrisdylanbriancooperchrisdylanbriancooperchrisdylanbriancooperchrisdylan"
    keyUpper = keyLower.upper()
    decrypted = ""
    i = 0
    for j in range(len(encrypted)):
        if encrypted[j] == ' ':
            decrypted += ' '
        else:
            if encrypted[j].isalpha():
                if encrypted[j].islower():
                    if (ord(encrypted[j]) % 97) - (ord(keyLower[i]) % 97) < 0:
                        decrypted += chr(((ord(encrypted[j]) % 97) - (ord(keyLower[i]) % 97)) + 97 + 26)
                    else:
                        decrypted += chr(((ord(encrypted[j]) % 97) - (ord(keyLower[i]) % 97)) + 97)
                if encrypted[j].isupper():
                    if (ord(encrypted[j]) % 65) - (ord(keyUpper[i]) % 65) < 0:
                        decrypted += chr(((ord(encrypted[j]) % 65) - (ord(keyUpper[i]) % 65)) + 65 + 26)
                    else:
                        decrypted += chr(((ord(encrypted[j]) % 65) - (ord(keyUpper[i]) % 65)) + 65)
                i += 1
            else:
                decrypted += encrypted[j]
    return decrypted

def getPersonByID(obj, member_name, member_value):
    if hasattr(obj, member_name) and getattr(obj, member_name) == member_value:
        return obj
    return None

#Route to home page
@app.route('/', methods = ['POST', 'GET'])
def index():
    user = ""
    already_seen = []
    return render_template('LoginScreen.html')

#Route to sign up page
@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    return render_template('SignUp.html')

#Route to upgrade page
@app.route('/upgrade', methods = ['POST', 'GET'])
def upgrade():
    return render_template('Upgrade.html')

#Route to page to purchase the silver package
@app.route('/purchaseSilver', methods = ['POST', 'GET'])
def purchSilv():
    return render_template('PurchaseSilver.html')

#Route to page to check if the card entered is valid for purchasing the gold package        
@app.route('/checkCardGold', methods = ['POST', 'GET'])
def checkCardGold():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == "POST":
        try: 
            validCard = True
            cardNumber = request.form['CardNum']
            if(len(cardNumber) == 16):
                for i in range(len(cardNumber)):
                    if not (cardNumber[i].isdigit()):
                        validCard = False
            else:
                validCard = False
            if(validCard):
                cursor.execute('UPDATE Login SET Status = ? WHERE FSUID = ?', ('Gold', already_seen[0]))
                conn.commit()
                return render_template("ValidCard.html")
            else:
                return render_template("InvalidCard.html")
        except:
            return render_template('LoginScreen.html')
        finally:
            conn.close()
 
 #Same as above but for silver       
@app.route('/checkCardSilver', methods = ['POST', 'GET'])
def checkCardSilver():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == "POST":
        try: 
            validCard = True
            cardNumber = request.form['CardNum']
            if(len(cardNumber) == 16):
                for i in range(len(cardNumber)):
                    if not (cardNumber[i].isdigit()):
                        validCard = False
            else:
                validCard = False
            if(validCard):
                cursor.execute('UPDATE Login SET Status = ? WHERE FSUID = ?', ('Silver', already_seen[0]))
                conn.commit()
                return render_template("ValidCard.html")
            else:
                return render_template("InvalidCard.html")
        except:
            return render_template('LoginScreen.html')
        finally:
            conn.close()

#Route to page to purchase the gold package
@app.route('/purchaseGold', methods = ['POST', 'GET'])
def purchGold():
    return render_template('PurchaseGold.html')

#Route to login screen
@app.route('/welcome', methods = ['POST', 'GET'])
def welcome():
    if request.method == "POST":
        try: 
            username = request.form['Username']
            password = request.form['Password']

            username = Encrypt(username)
            password = Encrypt(password)

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT FSUID FROM Login WHERE Username = ? AND Password = ?", (username,password))

            rows = cursor.fetchall()
            if len(rows) == 0:
                return render_template("NoMatchingUser.html")
            user = rows[0][0]
            already_seen.append(user)
            return redirect('/view')
        except:
            return redirect("/")
        finally:
            conn.close()

#Page to add sign up information into the database
@app.route('/signupvalid', methods = ['POST', 'GET'])
def signupvalid():
    if request.method == "POST":
        try: 
            first = request.form['First']
            last = request.form['Last']
            fsuid = request.form['Fsuid']
            gender = request.form['Gender']
            username = request.form['Username']
            password = request.form['Password']
            major = request.form['Major']
            confirmPass = request.form['ConfirmPassword']
            gpa = request.form['GPA']
            summary = request.form['Summary']
            user = username
            already_seen = [username]
            
            #Add username and password encryption here
            username = Encrypt(username)
            password2 = Encrypt(password)

            con = sqlite3.connect('database.db')
            
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                if(password == confirmPass):
                    
                    status = 'bronze'
                    cur.execute("INSERT INTO Login (Username,Password,First,Last,Gender,FSUID,Major,Description,GPA,Status) VALUES (?,?,?,?,?,?,?,?,?,?)", (username, password2, first, last, gender, fsuid, major, summary, gpa, status))
            return redirect("/")
        except:
            
            con.rollback()
            user = ""
            return render_template('Error.html')
        finally:
            con.close()

#Route to 'view' page to display a user's information and whether or not you want to like them
@app.route('/view', methods = ['POST', 'GET'])
def view():
    # retrieve amount of users from database\
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    s = ""
    for fsuid in already_seen:
        s += "\'" + str(fsuid) + "\',"
    # cursor.execute("SELECT FSUID FROM Login WHERE FSUID NOT IN ({})", (s,))
    cursor.execute("SELECT FSUID FROM Login")
    rows = cursor.fetchall()

    #get person based off their id
    randid = random.choice(rows)
    while randid[0] in already_seen:
        if len(already_seen) == len(rows):
            return render_template('NoMorePeople.html')
        randid = random.choice(rows)
    # select random user to display depending on preferences
    cursor.execute("SELECT * FROM Login WHERE FSUID = ?", (randid))
    row = cursor.fetchall()
    if row == []:
        return render_template('NoMorePeople.html')
    # use rows and setter functions to set the member data of p
    viewing.clear()
    viewing.append(row[0][9])
    return render_template('View.html', name=row[0][2], major=row[0][5], gpa=row[0][6], description=row[0][4])

#Sign out of profile and reset already seen list
@app.route('/signout', methods = ['POST', 'GET'])
def signout():
    already_seen.clear()
    return redirect("/")

# Like function gets called when a user clicks on the like button
# Adds this data to the database
@app.route('/like', methods = ['POST', 'GET'])
def like():
    if request.method == 'POST':
        try:
            already_seen.append(viewing[0])

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Likes (LikeFrom,LikeTo) VALUES (?,?)", (already_seen[0], viewing[0]))
            conn.commit()
        except:
            conn.rollback()
            return render_template('Error.html')
        finally:    
            conn.close()
            
    return redirect("/view")

# Dislike function gets called when a user clicks on the dislike button
# Adds user to the global variable, which is not needed to be stored permenantly
@app.route('/dislike', methods = ['POST', 'GET'])
def dislike():
    already_seen.append(viewing[0])
    return redirect("/view")
# Takes user to page showing who likes them
@app.route('/yourlikes', methods =['GET','POST'])
def yourlikes():
    likes = []
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT LikeFrom FROM Likes WHERE LikeTo = ?", (already_seen[0],))
    ids = cursor.fetchall()
    for id in ids:
        cursor.execute("SELECT * FROM Login WHERE FSUID = ?", (id[0],))
        likes.append(cursor.fetchall())
    
    
    return render_template("ViewLikes.html", likes=likes)

# Takes user to page showing the messages they have
@app.route('/yourmessages', methods = ['POST','GET'])
def viewMessages():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Status FROM Login WHERE FSUID = ?", (already_seen[0],))
    rows = cursor.fetchall()
    if rows[0][0] == "bronze" or rows[0][0] == "Silver":
        return render_template('NotAllowed.html')
    messagesWith = set()
    cursor.execute("SELECT SentFrom, SentTo FROM Messages WHERE SentFrom = ? OR SentTo = ?", (already_seen[0], already_seen[0]))
    rows = cursor.fetchall()
    if rows == []:
        return render_template("NoMessagesYet.html")
    for row in rows:
        if row[0] != already_seen[0]:
            messagesWith.add(row[0])
        elif row[1] != already_seen[0]:
            messagesWith.add(row[1])
    return render_template("MessagesWith.html", people=messagesWith)

# The page displays an individual message with a person
@app.route('/personalmessages', methods = ['POST','GET'])
def personalMessages():
    if request.method == 'POST':
        try:
            fsuid = request.form["fsuid"]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Status FROM Login WHERE FSUID = ?", (already_seen[0],))
            rows = cursor.fetchall()
            if rows[0][0] == "bronze" or rows[0][0] == "Silver":
                return render_template('NotAllowed.html')
            
            cursor.execute("SELECT SentFrom, Message FROM Messages WHERE (SentFrom = ? AND SentTo = ?) OR (SentFrom = ? AND SentTo = ?) ORDER BY Ind ASC", (already_seen[0], fsuid, fsuid, already_seen[0]))
            messages = cursor.fetchall()
            
            return render_template("ViewMessages.html", messages=messages, person=fsuid)
        except:
            return render_template('Error.html')

# This method gets called when a message gets sent
@app.route('/sendmessages', methods = ['POST','GET'])
def sendMessages():
    if request.method == 'POST':
        try:
            sentTo = request.form["sentTo"]
            message = request.form["message"]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(Ind) FROM Messages WHERE (SentFrom = ? AND SentTo = ?) OR (SentFrom = ? AND SentTo = ?)", (already_seen[0], sentTo, sentTo, already_seen[0]))
            result = cursor.fetchone()
            
            if(result[0] == None):
                result= (0,)
            i = int(result[0]) + 1
            cursor.execute("INSERT INTO Messages (SentFrom,SentTo,Message,Ind) VALUES (?,?,?,?)", (already_seen[0], sentTo, message, i))
            conn.commit()
            cursor.execute("SELECT SentFrom, Message FROM Messages WHERE (SentFrom = ? AND SentTo = ?) OR (SentFrom = ? AND SentTo = ?) ORDER BY Ind ASC", (already_seen[0], sentTo, sentTo, already_seen[0]))
            messages = cursor.fetchall()
            return render_template("ViewMessages.html", messages=messages, person=sentTo)

        except:
            conn.rollback()
            return render_template('Error.html')

# This shows the comments that have been added to your profile
@app.route('/yourcomments', methods = ['POST', 'GET'])
def viewComments():
    try:
        comments = []
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Comments WHERE FSUID = ?", (already_seen[0],))
        comments = cursor.fetchall()

        return render_template('Comments.html',comments=comments)
    except:
        return render_template('Error.html')

# Shows someone else's comments on their profile
@app.route('/profilecomments', methods = ['POST','GET'])
def profilecomments():
    if request.method == 'POST':
        try:
            fsuid = request.form["page"]
            comments = []
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Comments WHERE FSUID = ?", (fsuid,))
            comments = cursor.fetchall()
            return render_template('Comments.html',comments=comments)
        except:
            return render_template('Error.html')

# Gets called when you want to add a comment to someone else's page
@app.route('/addcomment', methods= ['POST','GET'])
def addComment():
    profile = request.form["prof"]
    return render_template('AddComments.html', profile=profile)

# Method that adds the writen comment to the database
@app.route('/writeComment', methods= ['POST','GET'])
def writeComment():
    if request.method == 'POST':
        try:
            comment = request.form["Comment"]
            prof = request.form['prof']
            comments = []
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Comments (FSUID,Commenter,Comment) VALUES (?,?,?)", (prof, already_seen[0], comment))
            conn.commit()
            cursor.execute("SELECT * FROM Comments WHERE FSUID = ?", (prof,))

            comments = cursor.fetchall()

            return render_template('Comments.html',comments=comments)
        except:
            conn.rollback()
            return render_template('Error.html')

# Routes to someone profile when they get clicked on by another user
@app.route('/profile', methods = ['POST','GET'])
def profile():
    if request.method == "POST":
        try: 
            FSUID = request.form['like']
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Status FROM Login WHERE FSUID = ?", (already_seen[0],))
            rows = cursor.fetchall()
            if(rows[0][0] == "bronze"):
                return render_template('NotAllowed.html')
            cursor.execute("SELECT * FROM Login WHERE FSUID=?", (FSUID,))
            person = cursor.fetchall()
            return render_template("Profile.html", person=person)
        except:
            return render_template('Error.html')


from Person import Person
if __name__ == "__main__":
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.close()
    app.run()
