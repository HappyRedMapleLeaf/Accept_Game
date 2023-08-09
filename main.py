"""
June 2022
ICS3U1
An East Asian high school student from a low-income household in Canada struggles to enter their dream university program. Minigames are strewn throughout to
give the player a sense of the challenges that the character faces.
"""

#IMPORT MODULES
import pgzrun
import math
import random

#CLASSES
class vec:
    """vector: x and y pair. operations with this class are easier than using tuples"""
    
    def __init__(self, coords):
        """create a vec object"""
        self.x = coords[0]
        self.y = coords[1]
        
    def __add__(self, other):
        """overloads + operator. adds x's and y's of two vec's"""
        return vec((self.x + other.x, self.y + other.y))
        
    def __sub__(self, other):
        """overloads + operator. subtracts x's and y's of two vec's"""
        return vec((self.x - other.x, self.y - other.y))
        
    def __mul__(self, k):
        """overloads * operator. multiplies x and y by k"""
        return vec((self.x * k, self.y * k))
        
    def __truediv__(self, k):
        """overloads / operator. divides x and y by k"""
        return vec((self.x / k, self.y / k))
        
    def inverse(self):
        """returns vec with reciprocal fo x and y"""
        return vec((1 / self.x, 1 / self.y))
        
    def tuple(self):
        """returns a tuple that can be passed into pygame functions"""
        return (self.x, self.y)
        
    def length(self):
        """returns the length of the vector"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

#GLOBAL VARIABLES

#MOVEMENT
level = []                   #list of rectangles
triggers = []                #list of (rectangle, triggername)
trigger_immune = False       #prevents triggers from activating right after popup closes
player = Actor("player")
direction = 0                #radians, ccw, right is 0
move_speed = 5               #constant. pixels per frame
target = vec(player.center)  #where the player tries to go

#SCREEN, DEBUG
WIDTH = 640         #used by pygame
HEIGHT = 480        #standard 4:3 resolution
framecount = 0      #number of update()s so far
fps = 0             #updates per second

#SCENE/SCENARIO MANAGEMENT
scene = "title"     #major section of storyline
flag = ""           #minor section of storyline
sceneduration = 0   #update()s so far in the current scene/section of code
marks = []          #only really contains physics and english mark
game_time = 0       #time it takes to do a minigame

#MOUSE
mclick = False      #true for the first frame that mouse is held.
mpos = vec((0, 0))  #position of mouse

#PHYSICS VARIABLES (BALANCING GAME)
angle = math.radians(0)        #angle of bar
angle_vel = math.radians(0)    #angular velocity in radians/frame
masses = [[0, random.randrange(1, 6)]]    #list of [position from -1 to 1, mass]

#ENGLISH VARIABLES (TYPING GAME)
total_chars = 0    #total characters typed
correct_chars = 0  #correct characters typed, <= total_chars
#typing passage
passage = """Amid widespread reports of discrimination
and violence against Asian Americans during
the coronavirus outbreak, thirty two percent
of Asian adults say they have feared someone
might threaten or physically attack them.
Eighty one percent of Asian adults also
say violence against them is increasing, far
surpassing the fifty six percent of all U.S.
adults who say the same. For universities,
Asian applicants may need a stronger
applicant profile than the average admitted
student to have a genuine chance of getting
into the very best American colleges."""
# passage = "abcdefg"  #used for debug
#SOURCES:
#https://www.pewresearch.org/fact-tank/2021/04/21/one-third-of-asian-americans-fear-threats-physical-attacks-and-most-say-violence-against-them-is-rising/ 
#https://www.forbes.com/sites/evangerstmann/2019/10/01/why-the-asian-american-students-lost-their-case-against-harvard-but-should-have-won/?sh=483876f863c1

#FIGHT SCENE VARIABLES
enemykid = Actor("enemykid", (380, 150))    #actor for kid
enemyman = Actor("enemyman", (-20, 370))    #actor for old man
attacking = False                           #if player is trying to attack
playerhurt = False                          #if player is attacked
enemykidhurt = False                        #if enemy is attacked 
enemykiddirection = 1                       #if kid is moving left (-1) or right (1)
playerhp = 100                              #health of player
enemykidhp = 100                            #health of kid
#health of old man is always 100 because if he's hit then you lose

#list of (position of textbox, dialogue)
fight_speech = [
    ((350, 150), "Yo chopsticks! Do you happen to have a few dollars we can borrow?"), 
    ((270, 300), "I don't have any money on me…"), 
    ((350, 150), "Aww, well that's too bad, isn't it?"), 
    ((275, 370), "I'm sure nobody'll mind if we get rid of these poor rice farmers anyway!")
]

#BUTTON RECTS FOR DIALOGUE SELECTION
button1 = Rect(0, 380, 210, 100)
button2 = Rect(215, 380, 210, 100)
button3 = Rect(430, 380, 210, 100)

#HISTORY CLASS VARiABLES
#list of (position of textbox, dialogue)
history_speech = [
    ((220, 320), "Of course this nerd gets a 95!"), 
    ((220, 320), "What was that?"), 
    ((220, 320), "That's what I thought."), 
    ((220, 320), "What's yer broke self gonna do about it?"), 
    ((360, 320), "Hey Nick! What did you get?"), 
    ((360, 240), "Aced. but yeah, that one question wasn't too easy…"), 
    ((360, 320), "Dang. Do you actually enjoy this course, by the way?"), 
    ((360, 240), "Sure! It's nice learning about my history. I see why you don't enjoy it though... Hey, why don't you ask Ms. Z about it? She's seems chill."), 
    ((360, 320), "Hey Ms. Z, can we learn some Asian history sometime?"), 
    ((60, 0), "I'm fascinated by Asian history too, but I must follow the curriculum. At the end of the year, I could teach some though!"), 
    ((60, 0), "Alright, let's start taking up the test. For the first question…")
]

#two lists containing dialogue options at different points that the player can choose
historychoice1 = ['Laugh with him', 'Ignore', '"Yeah yeah, shut up"']
historychoice2 = ['"Nothing..."', '"Shut up."']

#list of (position of textbox, dialogue)
lunch_speech = [
    ((250, 330), "Whaddya want, kid?"),
    ((260, 140), "..."),
    ((260, 140), "I--"),
    ((360, 150), "Lemme put it in a language you can understand:"),
    ((360, 150), "Oh so sory! No chow mein here! Yoo deliva, rong place!"),
    ((260, 140), "I usually sit here, I'm just waiting for my friends."),
    ((250, 330), "So? We sit here now. Go find somewhere else."),
    ((360, 150), "Hurry up, we don't wanna catch COVID!")
]

#list containing dialogue options that the player can choose
lunchchoice = ['Walk away, offended', 'Finish your sentence unfazed']

#BACK HOME UNTIL END OF GAME VARIABLES
#list of (person speaking, dialogue)
#0 means dad is talking, 1 means player is talking
home_speech = [
    (0, "Dad: How was your day?"), 
    (1, "I almost got beat up, but I'm fine. Some guys cornered me in an alleyway."), 
    (0, "Are you sure you're ok?"), 
    (1, "Yeah."), 
    (0, "Don't go there next time, stay on major roads and come back early."), 
    (0, "I don't want to say this, but racism is real around here. This applies to your university applications too, they'll be against you."), 
    (0, "You'll have to work extra hard to have the same chances as someone else. But we considered these things before we came here."), 
    (0, "All I can say is: Work hard and hope the future will be better.")
]

#stores text printed during application scene
applic_text = ""

#rect for email location
email_rect = Rect(150, 105, 490, 40)

#text displayed if win
win_text = """You have been accepted to Loo University!
=========================================
Defying the oppression that you have faced, you have achieved the goals you have been dreaming of and working towards for your entire high school life.
You know that your friends of different racial and financial backgrounds didn't have to work nearly as hard as you, but you should cherish your accomplishment nonetheless.
You realize that life really isn't fair; but hopefully, one day it will be.

YOU WIN!"""

#text displayed if lose
lose_text = """Thanks for applying to Loo University.
Unfortunately, after careful consideration, we cannot offer you admission in this program.

GAME OVER!"""

#FUNCTIONS
def loadlvl(file):
    """Load level from a file. Sets player position, and returns a list of collision rects and a list of trigger rects."""
    #levels made with the help of this program i threw together
    #https://replit.com/join/bjllnzyjhn-evanli2
    
    global target
    #empty level and trigger lists
    lvl = []
    trigs = []

    #dump entire file into a list of strings
    with open(file) as f:
        raw = f.readlines()

    #loops through every line of text
    for line in raw:
        #splits line with commas. not including first character
        spliced = line[1:].split(", ")

        #starts with n means normal block
        if line[0] == "n":
            #left, top, width, height
            rect = Rect(int(spliced[0]), int(spliced[1]), 
                        int(spliced[2]), int(spliced[3]))
            #append to list
            lvl.append(rect)

        #starts with t means trigger
        elif line[0] == "t":
            #left, top, width, height, name
            rect = Rect(int(spliced[0]), int(spliced[1]), 
                        int(spliced[2]), int(spliced[3]))

            #appends to list along with triggername
            trigs.append((rect, spliced[4]))

        #starts with p means player start position
        elif line[0] == "p":
            #sets player position as well as target so that the player doesn't move
            player.center = (int(spliced[0]), int(spliced[1]))
            target = vec(player.center)

    #return both lists
    return lvl, trigs

def move_player():
    """changes player position based on target and resolves collissions."""
    #loosely based on this: https://www.youtube.com/watch?v=8JJ-4JgR7Dg

    #two global variables will be changed
    global direction, target

    #change target based on where the player clicks
    if mclick:
        target = mpos

    #vector between target and position
    dist_to_target = target - vec(player.center)

    #only moves if position is far enough away from player
    if dist_to_target.length() > player.width / 2:

        #calculates player direction with dist_to_target
        if dist_to_target.x == 0:
            #deal with cases where atan is undefined
            if dist_to_target.y > 0:
                direction = 270
            else:
                direction = 90
        else:
            #direction = tan-1 (y / x)
            direction = math.atan(dist_to_target.y / dist_to_target.x)
            #deals with quadrants 2 and 3
            if dist_to_target.x < 0: direction += math.pi

        #difference in player position in x and y direction
        vx = math.cos(direction) * move_speed    #cos of direction * movement speed
        vy = math.sin(direction) * move_speed    #sin of direction * movement speed

        #list of collided rect information: [nearest hit position, whether collision is on x edge]
        #nearest hit position is normalized where 0 is layer position and 1 is destination (player position + vx and vy)
        hitrects = []

        #loop through every rectangle
        for rect in level:
            #expand rect by half the dimensions of the player so that I can collide using the center of the player
            expanded = Rect(rect.left - player.width / 2, rect.top - player.height / 2, rect.width + player.width, rect.height + player.height)

            #calculate near and far intersections of x and y velocities
            if vx == 0:
                #avoid with division by 0
                xnear = -math.inf
                xfar = math.inf
            else:
                #hard to explain with text, the video does it well
                #finds two x intersections with left and right of rectangle
                xnear = (expanded.left - player.x) / vx
                xfar = (expanded.right - player.x) / vx

                if xnear > xfar:
                    #swap if near is farther and far is nearer
                    xnear, xfar = xfar, xnear

            #same for y
            if vy == 0:
                ynear = -math.inf
                yfar = math.inf
            else:
                ynear = (expanded.top - player.y) / vy
                yfar = (expanded.bottom - player.y) / vy
                if ynear > yfar:
                    #swap if near is farther and far is nearer
                    ynear, yfar = yfar, ynear

            #where the player hits is the larger between xnear and ynear
            hit = max(xnear, ynear)
            
            #check if collision with a really neat set of comparisons
            if xnear < yfar and ynear < xfar and hit >= 0 and hit <= 1:
                #add information of this collided rect
                #2nd item is true when the ray intersects on x edge
                #and false when the ray intersects on a y edge
                hitrects.append([hit, xnear > ynear])

        
        #SORT HITRECTS
        #player gets stuck if further rectangles checked first
        #selection sort is simple www.geeksforgeeks.org/insertion-sort
        for i in range(len(hitrects)):
            #find smallest element in remaining part of list
            min_index = i
            for j in range(i+1, len(hitrects)):
                if hitrects[min_index][0] > hitrects[j][0]:
                    min_index = j
                     
            #swap this minimum element with first element that isn't sorted 
            hitrects[i], hitrects[min_index] = hitrects[min_index], hitrects[i]

        #resolve collision, finally
        for rectinfo in hitrects:
            #if hit on x
            if rectinfo[1]:
                #multiply x velocity by hit, decreasing it
                vx *= rectinfo[0]
            else:
                #if hit on y, multiply y velocity by hit
                vy *= rectinfo[0]

        #change the player position by the velocity at last
        player.x += vx
        player.y += vy

def simulation():
    """updates physics simulation. the bar has no mass! wow im such a scientist"""
    global angle, angle_vel
    #total torque and moment of inertia
    nettorque = 0
    netmoment = 0

    #loops through every mass
    for item in masses:
        radius = item[0]
        mass = item[1]
        #moment of inertia = mass * radius^2
        netmoment += mass * abs(radius) ** 2

        g = 0.001
        #torque = force * distance
        #       = (mass * g * sin angle b/w lever and force) * radius
        nettorque += g * mass * -math.sin(math.pi / 2 - angle) * radius

    #angular acceleration = torques / moments of inertia
    angle_vel += nettorque / netmoment
    angle += angle_vel

    #return true if the weight has fell, or if it takes longer than ~10 seconds
    if abs(angle) > math.pi / 2 or sceneduration > 600:
        return True
    else:
        return False

def fightmechanics():
    """update fight scene"""
    #a bunch of global variables
    global attacking, playerhp, enemykidhp, playerhurt, enemykidhurt, enemykiddirection, target, scene, sceneduration

    #move kid left and right. slower if less hp
    enemykid.x += enemykidhp * 0.05 * enemykiddirection
    #change direction if kid moves too far
    if enemykid.x > 330:
        enemykiddirection = -1
    if enemykid.x < 270:
        enemykiddirection = 1

    #defaults to false
    playerhurt = False
    if player.colliderect(enemykid):
        #if player touches kid: get hurt, and get knocked back a bit
        playerhp -= random.randrange(7, 11)
        playerhurt = True
        player.y += 10
        player.x -= 3
        target = vec(player.center)
    
    if player.colliderect(enemyman):
        #if player touches adult: get hurt and get knocked back
        playerhurt = True
        playerhp -= random.randrange(3, 8)
        player.y -= 10
        target = vec(player.center)

    enemykidhurt = False
    if attacking:
        #hurts enemy if player is within a certain distance to him
        if (vec(player.center) - vec(enemykid.center)).length() < 50:
            enemykidhurt = True
            #decrease hp
            enemykidhp -= random.randrange(11, 15)
        
        if (vec(player.center) - vec(enemyman.center)).length() < 50:
            #don't hit elderly people, you will be arrested
            scene = "police_man"
            sceneduration = 0

    #police comes if kid is hurt too much
    if enemykidhp < 15:
        scene = "police_kid"
        sceneduration = 0

    #you go to the hospital if you are beat up too much
    if playerhp < 1:
        playerhp = 0
        scene = "hospital"
        sceneduration = 0

    #reset attacking to false to make sure it is only true for one frame
    attacking = False
        
def drawdebug():
    """draw debug text: fps, scene, flag, mouse position"""
    screen.draw.text(f"{round(fps, 2)}", (0, 0), fontname="normal", color="red")
    screen.draw.text(f"{scene}", (0, 20), fontname="normal", color="red")
    screen.draw.text(f"{flag}", (0, 40), fontname="normal", color="red")
    screen.draw.text(f"{mpos.x}, {mpos.y}", (0, 60), fontname="normal", color="red")

def draw():
    #clear screen every frame
    screen.clear()

    #python doesn't have switches :(
    if scene == "title":
        #print title image
        screen.blit("title", (0, 0))

    elif scene == "morningcut":
        #print cutscene text
        screen.draw.textbox("The Big Day\n8:00am", (50, 180, 530, 120), color="white", fontname="pixel")
    
    elif scene == "home1":
        screen.blit("home", (0, 0))    #draw home background
        player.draw()                  #draw player

        #draw semi-transparent white background and instructions text
        if flag == "instructions":
            screen.blit("transoverlay", (0, 0))
            screen.draw.textbox("Click around\n to move.", (50, 180, 530, 120), color="black", fontname="pixel")

        #draw transparent overlay and context text
        elif flag == "about":
            screen.blit("transoverlay", (0, 0))
            screen.draw.textbox("You, Freddie Zhang, have a big day ahead!\n\nToday, you are applying for Loo University. As an East Asian, you must especially excel in school to be accepted, and your financial situation means you have to balance school and work.",
                                (50, 50, 540, 380), color="black", fontname="normal", align="left")

        #draw transparent overlay and schedule paper image
        elif flag == "schedule":
            screen.blit("transoverlay", (0, 0))
            screen.blit("schedule", (0, 0))

    elif scene == "physicscut":
        #draw physics cutscene text
        screen.draw.textbox("9:00am:\nPhysics Class", (50, 180, 530, 120), color="white", fontname="pixel")

    elif scene == "physics":
        #draw physics background image
        screen.blit("physicsbg", (0, 0))

        #precalculating sin and cosine to reduce hard calculations
        cos = math.cos(angle)
        sin = math.sin(angle)

        #draw 3 lines representing the bar
        screen.draw.line((320 - cos * 240, 244 + sin * 240), 
                         (320 + cos * 240, 244 - sin * 240), "black")
        screen.draw.line((320 - cos * 240, 240 + sin * 240), 
                         (320 + cos * 240, 240 - sin * 240), "black")
        screen.draw.line((320 - cos * 240, 247 + sin * 240), 
                         (320 + cos * 240, 247 - sin * 240), "black")

        #draw all masses and text with mass value on each mass
        for item in masses:
            #calculate mass position using position and angle
            position = (320 + cos * 240 * item[0] - 20, 235 - sin * 240 * item[0])
            screen.blit("mass", position)
            screen.draw.text(str(item[1]), (position[0] + 14, position[1] + 30), fontsize=36)

        #display instruction text
        if flag == "instructions":
            screen.blit("transoverlay", (0, 0))
            screen.draw.textbox("Instructions:\nBalance the bar with ten masses! The longer it takes for the bar to fall, the higher your mark will be. Click to begin.",
                                (30, 300, 580, 120), color="black", fontname="normal")
        
        #Draw text telling the player which mass they are placing
        elif flag == "choosing":
            screen.draw.text(f"Place mass #{len(masses)}", (20, 20), fontsize=18, color="black", fontname="pixel")
            if len(masses) == 10:
                #"Place mass #10 and start the drop"
                screen.draw.text(f"and start the drop", (20, 60), fontsize=18, color="black", fontname="pixel")

        #draw the text "falling..." when the bar is falling
        elif flag == "simulating":
            screen.draw.text("Falling...", (20, 20), fontsize=36, color="black", fontname="pixel")

        #draw results (time, score, click to continue)
        elif flag == "results":
            screen.blit("transoverlay", (0, 0))
            screen.draw.textbox(f"Fell after {round(game_time / 60, 2)} seconds!\nPhysics mark: {marks[0]}\nClick to continue.", (30, 150, 580, 150), color="black", fontname="normal")

    #history cutscene text
    elif scene == "historycut":
        screen.draw.textbox("10:15am\nHistory Class", (50, 180, 530, 120), color="white", fontname="pixel")

    elif scene == "history":
        screen.blit("history", (0, 0))  #history class bg
        player.draw()                   #draw player
        
        if flag == "sit":
            #tell player where to go
            screen.blit("alerticon", (330, 390))
            
        if flag == "seated":
            #tell player to click
            screen.draw.textbox("(click)", (30, 300, 150, 30), color="black", fontname="normal")
            
            #display teacher's speech
            screen.blit("textbox2", (60, 0))
            textbox = Rect(110, 5, 210, 90)
            screen.draw.textbox("Good afternoon everyone! I've finally marked your tests… First I'll take them up, then we will move on and start the next unit.", textbox, color="black", fontname="normal")
        
        elif flag == "getmark":
            #display test paper at teacher's desk
            screen.blit("paper", (180, 150))
            
        elif flag == "reading":
            #show player mark
            screen.blit("transoverlay", (0, 0))
            screen.draw.textbox("Your Mark:\n95%", (50, 180, 530, 120), color="black", fontname="pixel")
        
        elif flag == "choice1":
            #draw choice buttons and choice text
            screen.blit("button", button1.topleft)
            screen.blit("button", button2.topleft)
            screen.blit("button", button3.topleft)
            screen.draw.textbox(historychoice1[0], button1, color="black")
            screen.draw.textbox(historychoice1[1], button2, color="black")
            screen.draw.textbox(historychoice1[2], button3, color="black")
        
        elif flag == "choice2":
            #same as above, but only 2 choices
            screen.blit("button", button1.topleft)
            screen.blit("button", button3.topleft)
            screen.draw.textbox(historychoice2[0], button1, color="black")
            screen.draw.textbox(historychoice2[1], button3, color="black")
        
        elif "dialogue" in flag:
            #draw dialogue based on history_speech list
            screen.draw.textbox("(click)", (30, 300, 150, 30), color="black", fontname="normal")
            index = int(flag[8:])    #get last number of flag
            
            #calculate speech box position and draw
            imgpos = history_speech[index][0]
            screen.blit("textbox2", imgpos)
            textbox = Rect(imgpos[0] + 50, imgpos[1] + 5, 210, 90)
            screen.draw.textbox(history_speech[index][1], textbox, color="black", fontname="normal")

    elif scene == "lunchcut":
        #lunch cutscene text
        screen.draw.textbox("11:30am\nLunch", (50, 180, 530, 120), color="white", fontname="pixel")
    
    elif scene == "lunch":
        screen.blit("cafeteria", (0, 0))    #cafeteria bg
        player.draw()                       #draw player
        
        if flag == "sit":
            #tell player where to go
            screen.blit("alerticon", (220, 220))
            
        if flag == "choice":
            #draw choices
            screen.blit("button", button1.topleft)
            screen.blit("button", button3.topleft)
            screen.draw.textbox(lunchchoice[0], button1, color="black")
            screen.draw.textbox(lunchchoice[1], button3, color="black")
        
        elif "dialogue" in flag:
            #similar to history class; draw the dialogue
            if flag != "dialogue7":
                screen.draw.textbox("(click)", (30, 300, 150, 30), color="black", fontname="normal")
            index = int(flag[8:])
            imgpos = lunch_speech[index][0]
            screen.blit("textbox2", imgpos)
            textbox = Rect(imgpos[0] + 50, imgpos[1] + 5, 210, 90)
            screen.draw.textbox(lunch_speech[index][1], textbox, color="black", fontname="normal")
    
    elif scene == "englishcut":
        #english cutscene text
        screen.draw.textbox("12:30pm\nEnglish Class", (50, 180, 530, 120), color="white", fontname="pixel")
        
    elif scene == "english": 
        #draw background monitor
        screen.blit("monitor", (0, 0))

        #draw base text (black)
        screen.draw.text(passage, (50, 40), fontsize=24, color="black", fontname="normal", align="left")
        #draw every character as red
        screen.draw.text(passage[:total_chars], (50, 40), fontsize=24, color="red", fontname="normal", align="left")
        #draw correct characters on top as green
        screen.draw.text(passage[:correct_chars], (50, 40), fontsize=24, color="green", fontname="normal", align="left")
        
        if flag == "instructions":
            #display typing instructions
            screen.blit("transoverlay", (0, 0))
            screen.blit("transoverlay", (0, 0))
            screen.draw.textbox("Instructions:\nType the passage as fast as you can! Letter case doesn't matter. Click to begin timing.",
                                (30, 100, 580, 150), color="black", fontname="normal")
        elif flag == "results":
            #print time and score
            screen.blit("transoverlay", (0, 0))
            screen.draw.textbox(f"Finished typing in {round(game_time / 60, 2)} seconds!\nEnglish mark: {marks[1]}\nClick to continue.", (30, 150, 580, 150), color="black", fontname="normal")

    elif scene == "calccut":
        #calculus cusxcene text
        screen.draw.textbox("1:45pm\nCalculus Class", (50, 180, 530, 100), color="white", fontname="pixel")
    
    elif scene == "calc":
        #nothing happens in calculus, just print some text
        screen.fill("white")
        screen.draw.textbox("This is your favorite class; your teacher and classmates are all very supportive here, and the subject is challenging enough but not too difficult. The time in this class passes in the blink of an eye.\n\nClick to continue.",
                                (50, 50, 540, 380), color="black", fontname="normal", align="left")
    
    elif scene == "fightcut":
        #walking to work cutscene text
        screen.draw.textbox("3:00pm\nAfter School\nWalking to Work", (50, 180, 530, 120), color="white", fontname="pixel")
        
    elif scene == "fight":
        #draw dark shadow alley if walking, light shadow alley if cutscene starts
        if flag == "walk":
            screen.blit("alley1", (0, 0))
        else:
            screen.blit("alley2", (0, 0))

        #draw player
        player.draw()

        if flag == "dialogue1":
            #dialogue1 is really just people walking. draw everyone
            enemyman.draw()
            enemykid.draw()
        elif "dialogue" in flag:
            #draw "(click)", people, and dialogues with textboxes. again, similar to above
            screen.draw.textbox("(click)", (200, 180, 150, 30), color="white", fontname="normal")
            enemyman.draw()
            enemykid.draw()
            
            index = int(flag[8]) - 2
            imgpos = fight_speech[index][0]
            screen.blit("textbox", imgpos)
            textbox = Rect(imgpos[0] + 50, imgpos[1] + 5, 210, 90)
            screen.draw.textbox(fight_speech[index][1], textbox, color="black", fontname="normal")
        
        elif flag == "action":
            #tell player how to attack people
            screen.draw.textbox("Press SPACE to attack.", (370, 200, 250, 50), color="black", fontname="normal")

            #draw player healthbar, which is red if hurt
            screen.draw.text("You", (20, 390), fontsize=18, color="white", fontname="normal")
            if playerhurt:
                screen.draw.filled_rect(Rect(70, 390, playerhp, 18), "red")
            else:
                screen.draw.filled_rect(Rect(70, 390, playerhp, 18), "green")
           
            #draw kid healthbar
            screen.draw.text("Kid", (20, 420), fontsize=18, color="white", fontname="normal")
            if enemykidhurt:
                screen.draw.filled_rect(Rect(70, 420, enemykidhp, 18), "red")
            else:
                screen.draw.filled_rect(Rect(70, 420, enemykidhp, 18), "green")
            
            #draw old man healthbar, always at 100
            screen.draw.text("Man", (20, 450), fontsize=18, color="white", fontname="normal")
            screen.draw.filled_rect(Rect(70, 450, 100, 18), "green")

            #draw enemykid sprite (a different sprite if hurt)
            if enemykidhurt:
                enemykid.image = ("hurt")
            else:
                enemykid.image = ("enemykid")

            #draw enemies
            enemyman.draw()
            enemykid.draw()

            #draw red overlay if the player is hurt
            if playerhurt:
                screen.blit("hurtoverlay", (0, 0))
    
    elif scene == "police_man":
        #draw text for when police come after attacking old man
        screen.fill("white")
        screen.draw.textbox("The police appear and stop the fight. Because you hit the old man, they accuse you of starting it. You've now missed a day of work, enraging your manager, who lowered your wage. With these new circumstances, it is nearly impossible to afford university.",
                                (50, 50, 540, 380), color="black", fontname="normal", align="left")
    elif scene == "police_kid":
        #draw text for when police come after knocking out kid
        screen.fill("white")
        screen.draw.textbox("The police appear and stop the fight. Because the kid is more badly hurt, they accuse you of starting it. You've now missed a day of work, enraging your manager, who lowered your wage. With these new circumstances, it is nearly impossible to afford university.",
                                (50, 50, 540, 380), color="black", fontname="normal", align="left")
    
    elif scene == "hospital":
        #draw text for when player gets hurt
        screen.fill("white")
        screen.draw.textbox("After taking so many hits, you suddenly pass out.\nYou wake up in the hospital the next day, and realize that you've missed the university application deadline.",
                                (50, 50, 540, 380), color="black", 
                            fontname="normal", align="left")
    
    elif scene == "lose":
        #game lose screen
        screen.blit("lose", (0, 0))

    elif scene == "homecut":
        #back at home cutscene text
        screen.draw.textbox("3:00pm\nAfter Work\nBack Home", (50, 180, 530, 120), color="white", fontname="pixel")
    
    elif scene == "home2":
        #draw player and background image
        screen.blit("home2", (0, 0))
        player.draw()
        
        if "dialogue" in flag:
            #draw dialogues similar to the previous examples
            screen.draw.textbox("(click)", (50, 200, 150, 30), color="black", fontname="normal")
            index = int(flag[8:])

            #only difference is that the dialogues are stored a bit differently
            #when dad is talking, speech is at the corner
            if home_speech[index][0] == 0:
                screen.blit("textbox", (-20, 50))
                textbox = Rect(30, 55, 210, 90)
                screen.draw.textbox(home_speech[index][1], textbox, color="black", fontname="normal")
            #when player is talking, speech is beside the player
            else:
                screen.blit("textbox2", (player.x, player.y - 100))
                textbox = Rect(player.x + 50, player.y - 95, 210, 90)
                screen.draw.textbox(home_speech[index][1], textbox, color="black", fontname="normal")

    elif scene == "applicationcut":
        #draw application cutscene text
        screen.draw.textbox("8:00pm\nApplication", (50, 180, 530, 120), color="white", fontname="pixel")
        
        #set up application text for next scene
        global applic_text
        applic_text = f"""Submitted marks:
Physics: {marks[0]}
History: 95
English: {marks[1]}
Calculus: 96
Functions: 98
Chemistry: 96
Computer Science: 99

Click to submit!"""
    
    elif scene == "application":
        #draw monitor background
        screen.blit("monitor", (0, 0))

        #draw applic_text characters one by one
        #once everything is printed, just print the full string
        if sceneduration < len(applic_text):
            screen.draw.text(applic_text[:sceneduration], (180, 50), fontname="normal", fontsize=30, color="black")
        else:
            screen.draw.text(applic_text, (180, 50), fontname="normal", fontsize=30, color="black")

    elif scene == "sleep":
        #draw sleep cutscene text and fade out
        screen.draw.textbox("12:30am\nYou go to bed.", (50, 180, 530, 120), color="white", fontname="pixel")
        
        #fade is accomplished by layering semi-transparent dark rectangles
        if sceneduration > 140:
            for i in range(sceneduration - 140):
                screen.blit("darkoverlay", (0, 0))

    elif scene == "bigcut":
        #draw six months later cutscene text and unfade the darkness
        screen.draw.textbox("SIX MONTHS LATER", (50, 180, 530, 120), color="white", fontname="pixel")
        if sceneduration < 40:
            for i in range(40 - sceneduration):
                screen.blit("darkoverlay", (0, 0))

    elif scene == "email":
        #draw inbox image
        screen.blit("mail", (0, 0))

    elif scene == "win":
        #draw monitor, and similar to application, print characters one by one, like above with application text
        screen.blit("monitor", (0, 0))
        if sceneduration < len(win_text):
            screen.draw.text(win_text[:sceneduration], (60, 50), width=520, fontname="normal", fontsize=20, color="black")
        else:
            screen.draw.text(win_text, (60, 50), width=520, fontname="normal", fontsize=20, color="black")

    elif scene == "lose2":
        #draw monitor and lose text one character at a time, like above
        screen.blit("monitor", (0, 0))
        if sceneduration < len(lose_text):
            screen.draw.text(lose_text[:sceneduration], (60, 50), width=520, fontname="normal", fontsize=30, color="black")
        else:
            screen.draw.text(lose_text, (60, 50), width=520, fontname="normal", fontsize=30, color="black")

    #drawdebug()

def update(dt):
    global fps, framecount, sceneduration            #counting variables
    global scene, flag, mclick                       #general variables
    global trigger_immune, level, triggers, target   #movement variables
    global game_time                                 #for minigames

    #increment sceneduration and framecount, and update fps once per 10 frames
    sceneduration += 1
    framecount += 1
    if framecount % 10 == 0:
        fps = 1 / dt

    if scene == "title" and mclick:
        #go to next scene and reset sceneduration
        scene = "morningcut"
        sceneduration = 0
            
    elif scene == "morningcut" and sceneduration > 120:
        #go to next scene and load level after 2 seconds
        scene = "home1"
        flag = "instructions"
        level, triggers = loadlvl("levels/home.txt")
            
    elif scene == "home1":
        move_player()

        #check for collision with trigger
        #triggerimmune checks prevent player from activating triggers when it should'nt
        index = 0
        while index < len(triggers) + 1:
            #loops when index is within the range of triggers
            if index == len(triggers):
                #turn off immune if there are no collisions
                trigger_immune = False
                
            elif player.colliderect(triggers[index][0]):
                if not trigger_immune:
                    flag = triggers[index][1].strip()
                    trigger_immune = True
                break
            #increment index to check
            index += 1

        #remove flags (therefore removing popups) if mouse is clicked
        if mclick: flag = ""

        #if the trigger changes flag to physicscut then change the scene and reset sceneduration
        if flag == "physicscut":
            scene = "physicscut"
            sceneduration = 0
            
    #change to next scene if the scene has run for 2 seconds
    elif scene == "physicscut":
        if sceneduration > 120:
            scene = "physics"
            flag = "instructions"

    elif scene == "physics":
        if flag == "instructions" and mclick:
            #change flag is the player clicks the instructions
            flag = "choosing"
                
        elif flag == "choosing":
            #choosing masses

            #moving the mass location based on mouse x
            masses[len(masses) - 1][0] = mpos.x / (WIDTH / 2) - 1

            #place the mass if mouse is clicked
            if mclick:
                if len(masses) < 10:
                    #randomly generate next mass
                    masses.append([mpos.x / (WIDTH / 2) - 1, random.randrange(1, 6)])
                else:
                    #once all masses are placed, move to simulation
                    flag = "simulating"
                    sceneduration = 0
        
        elif flag == "simulating":
            #run simulation and get result
            if simulation():
                #if the simulation is done, then set game time (for drawing) and add mark
                game_time = sceneduration
                mark = 90 + math.floor((max(min(game_time, 350), 50) - 50) / 30)
                marks.append(mark)
                #change the flag to results so that the player can see how they did
                flag = "results"
                
        elif flag == "results" and mclick:
            #if player clicks on results, go to history cutscene
            scene = "historycut"
            sceneduration = 0

    #change to next scene if the scene has run for 3 seconds
    elif scene == "historycut":
        if sceneduration > 180:
            scene = "history"
            flag = "sit"
            sceneduration = 0
            #load history classroom
            level, triggers = loadlvl("levels/history.txt")

    elif scene == "history":
        
        if flag == "sit":
            #move the player until hitting the seat trigger
            move_player()
            if player.colliderect(triggers[1][0]):
                #change flag
                flag = "seated"
                sceneduration = 0
                #set player position to be centered on the seat
                player.center = (360, 420)
        
        elif flag == "seated":
            #go to next flag after 4 seconds or on mouse click
            if sceneduration > 240 or mclick:
                flag = "getmark"
            
        elif flag == "getmark":
            #move the player tiltil they reach the test trigger in front of the teacher
            move_player()
            if player.colliderect(triggers[0][0]):
                flag = "reading"
        
        elif flag == "reading" and mclick:
            #start dialogue on mouseclick and move player back to seat
            sceneduration = 0
            player.center = (360, 420)
            flag = "dialogue0"
        
        elif flag == "dialogue0" and mclick:
            #go to first choice after clicking past dialogue0
            flag = "choice1"
            
        elif flag == "choice1" and mclick:
            #go to different dialogues if the mouse position intersects with a button and the mouse is clicked
            if button3.collidepoint(mpos.tuple()):
                flag = "dialogue1"
            elif button1.collidepoint(mpos.tuple()) or button2.collidepoint(mpos.tuple()):
                flag = "dialogue4"

        #after dialogue1, there is another choice
        elif flag == "dialogue1" and mclick:
            flag = "choice2"

        elif flag == "choice2" and mclick:
            #same as above, go to dialogue points based on selection
            if button1.collidepoint(mpos.tuple()):
                flag = "dialogue2"
            elif button3.collidepoint(mpos.tuple()):
                flag = "dialogue3"
        
        elif (flag == "dialogue2" or flag == "dialogue3") and mclick:
            #both of these paths end up advancing to dialogue4 on click
            flag = "dialogue4"
        
        elif "dialogue" in flag and mclick:
            if flag == "dialogue10":
                #after dialogue10, go to next scene
                scene = "lunchcut"
                sceneduration = 0
            else:
                #in all other cases, increase flag's number by one
                flag = f"dialogue{int(flag[8:]) + 1}"        
            
    #change to next scene if the scene has run for 2 seconds
    elif scene == "lunchcut":
        if sceneduration > 120:
            scene = "lunch"
            flag = "sit"
            sceneduration = 0
            #load cafeteria level
            level, triggers = loadlvl("levels/cafeteria.txt")

    elif scene == "lunch":
        if flag == "sit":
            #move the player until hitting the seat trigger
            move_player()
            if player.colliderect(triggers[0][0]):
                flag = "dialogue0"
                #freezing the player so that textbox matches up with player location
                player.center = (245, 245)
                target = vec(player.center)

        #once dialogue is finished, move the player off the screen and go to next scene
        elif flag == "dialogue7":
            mclick = False
            target = vec((-30, -30))
            move_player()
            #once the player is off the screen (takes 2s), go to next scene
            if sceneduration > 120:
                scene = "englishcut"

        #at dialogue4, the player has a choice
        elif flag == "dialogue4" and mclick:
            flag = "choice"

        #advance dialogue on mouseclick
        elif "dialogue" in flag and mclick:
            flag = f"dialogue{int(flag[8:]) + 1}"  
            sceneduration = 0

        #go to different sections of dialogue depending on which choice is clicked
        elif flag == "choice" and mclick:
            #button1 skips some dialogue
            if button1.collidepoint(mpos.tuple()):
                flag = "dialogue7"
                sceneduration = 0

            #button2 goes to dialogue5
            elif button3.collidepoint(mpos.tuple()):
                flag = "dialogue5"
            
    #change to next scene after 3 seconds
    elif scene == "englishcut":
        if sceneduration > 180:
            flag = "instructions"
            scene = "english"
            
    elif scene == "english":
        if flag == "instructions":
            #go to next flag if instructions clicked
            if mclick:
                flag = "typing"
                sceneduration = 0
        
        elif flag == "typing":
            #on_key_down handles most things.
            #however a completion check is necessary here
            if correct_chars == len(passage):
                #add mark, set game_time for display in draw(), and change flag
                flag = "results"
                game_time = sceneduration
                marks.append(110 - min(max(game_time / 600, 10), 20))

        #go to next scene if results clicked
        elif flag == "results":
            if mclick:
                scene = "calccut"
                sceneduration = 0

    #change to next scene after 2 seconds
    elif scene == "calccut":
        if sceneduration > 120:
            scene = "calc"

    #change to next scene on mouseclick
    elif scene == "calc":
        if mclick:
            scene = "fightcut"
            sceneduration = 0
    
    #change to next scene after 3 seconds
    elif scene == "fightcut":
        if sceneduration > 180:
            flag = "walk"
            scene = "fight"
            #load alley level
            level, triggers = loadlvl("levels/alley.txt")

    elif scene == "fight":

        if flag == "walk":
            #move the player normally
            move_player()

            #if the player gets to the middle of the alleyway, then change flag to dialogue1
            for trigger in triggers:
                if player.colliderect(trigger[0]):
                    flag = trigger[1].strip()
                    sceneduration = 0
                    #freeze player by setting target to current position
                    target = vec(player.center)
                    break

        elif flag == "dialogue1":
            #disable player movement by removing click detection
            mclick = False
            move_player()

            #move the enemykid out of the shadows
            if sceneduration < 10:
                enemykid.x -= 5

            #move the player back to try to run backwards
            if sceneduration == 40: 
                target = vec((270, 320))

            #move the old man so that he blocks he player
            if sceneduration > 20 and sceneduration < 80:
                enemyman.x += 5

            #move the player back up a bit and  start the actual dialogue
            if sceneduration == 100:
                target = vec((270, 230))
                flag = "dialogue2"
                
        elif "dialogue" in flag:
            #advance dialogue on mouseclick
            if mclick:
                if flag == "dialogue5":
                    #start fight if the dialogue finishes
                    flag = "action"
                else:
                    #otherwise, change the flag to the next dialogue number
                    flag = f"dialogue{int(flag[8:]) + 1}"
                    
        elif flag == "action":
            #move the player and call fightmechanics
            move_player()
            fightmechanics()

            #set the flag if the player collides with the escape trigger at the top
            if player.colliderect(triggers[1][0]):
                flag = triggers[1][1]

        #if the flag is "escaped", then change to next scene
        #strip is necessary because the trigger names have some white space around them for some reason
        elif flag.strip() == "escaped":
            scene = "homecut"
            sceneduration = 0
    
    #change to next scene after around 10 seconds or if the mouse is clicked
    #these scenes just show text
    elif scene == "police_man" or scene == "police_kid" or scene == "hospital":
        if sceneduration > 620 or mclick:
            scene = "lose"

    #change to next scene after 3 seconds
    elif scene == "homecut":
        if sceneduration > 180:
            scene = "home2"
            flag = "wait"
            sceneduration = 0
            #load the home level again
            level, triggers = loadlvl("levels/home.txt")

    elif scene == "home2":
        #move the player, although movement isn't really required
        move_player()

        #the dialogue only starts after the first click, so the scene starts with a "wait" flag
        if flag == "wait" and mclick:
            flag = "dialogue0"

        #advance dialogue if clock
        elif "dialogue" in flag and mclick:
            if flag == "dialogue7":
                #once dialogue is done, go to next scene
                scene = "applicationcut"
                sceneduration = 0
            else:
                #otherwise, change the flag to the next dialogue number
                flag = f"dialogue{int(flag[8:]) + 1}"

    #change to next scene after mouse click
    elif scene == "applicationcut":
        if sceneduration > 180:
            scene = "application"
            sceneduration = 0

    #change to next scene after mouse click
    elif scene == "application":
        if mclick:
            scene = "sleep"
            sceneduration = 0
    
    #change to next scene after 3 seconds
    elif scene == "sleep":
        #layer darkness for fade to black
        if sceneduration > 180:
            scene = "bigcut"
            sceneduration = 0

    #change to next scene after 3 seconds
    elif scene == "bigcut":
        if sceneduration > 180:
            scene = "email"
            sceneduration = 0

    elif scene == "email":
        #if the player clicks on the email
        if mclick and email_rect.collidepoint(mpos.tuple()):
            #if the player got an average of at least 98, they are accepted.
            if sum(marks) >= 196:
                #change scene to win and reset sceneduration
                scene = "win"
                sceneduration = 0
            else:
                #change scene to lose2 and reset sceneduration
                scene = "lose2"
                sceneduration = 0

    #set mclick to false every frame so that it's only true for the first frame that the mouse is down
    mclick = False

def on_mouse_down(button):
    #make mclick true if left mouse clicked
    #it's set back to false at the end of update() so that
    #it's only True for one frame
    if button == mouse.LEFT:
        global mclick
        mclick = True

def on_mouse_move(pos):
    #update mouse position
    global mpos
    mpos = vec((pos))

def on_key_down(key):
    #run code based on the scene
    if scene == "english" and flag == "typing":
        global total_chars, correct_chars

        #converting presssed key to a string by getting the key and value pairs of the key enumueration
        keystring = list(vars(keys).keys())[list(vars(keys).values()).index(key)]
        #special cases
        if keystring == "SPACE": keystring = " "
        elif keystring == "COMMA": keystring = ","
        elif keystring == "PERIOD": keystring = "."
        
        if keystring == "BACKSPACE":
            #remove a character
            if total_chars > 0: total_chars -= 1

            #decrease correct chars only if required
            if correct_chars > total_chars:
                correct_chars -= 1
                
        elif len(keystring) == 1:    #discounts all special characters because their keycode lengths are more than 1
            #checks if the tpyed character is correct and increases correct_chars
            if correct_chars == total_chars and (passage[total_chars].upper() == keystring or (passage[total_chars] == "\n" and keystring == " ")):
                correct_chars += 1

            #increases total_chars regardless
            total_chars += 1

    #set attacking to true if in fight and space is pressed
    elif scene == "fight" and flag == "action":
        if key == keys.SPACE:
            global attacking
            attacking = True

#start pygame program
pgzrun.go()