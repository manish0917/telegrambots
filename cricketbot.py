#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.x
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import time
import random
import logging
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    DictPersistence,
    Filters,
    MessageHandler
)



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Writing to sample.json
user_data_dict={}
try:
    with open("user.json", "r") as outfile:
        user_data_dict = json.loads(outfile.read())
except:
    user_data_dict = json.loads("user.json")

# Persistence object 
user_persistence = DictPersistence()



"""Run the bot."""
# Create the Updater and pass it your bot's token.
updater = Updater("5249768026:AAG_wdL5BWNEKSyZAPb8htNylH90UyEylqg", persistence=user_persistence, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher



# Stages
FIRST, SECOND, THIRD = range(3)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN = range(10)

#Start Command
def start(update: Update, context: CallbackContext):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    #Add group Inline Keyboard
    keyboard = [
        [
            InlineKeyboardButton("Add to Group!", url="https://telegram.me/crick_test_bot?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    hello_msg="Hello "+user.first_name+", I am CrickBot.\n A Guessing Game to Guess other Player's Moves.\n Add me to Your Group to have Fun\n"
    menu_msg="/playwithbot - To Play with Bot\n/challenge - To play with Friends."
    msg=hello_msg+menu_msg
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_markup)

    return ConversationHandler.END
    

def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    return FIRST

#mystats command
def mystats(update: Update, context: CallbackContext):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    user = update.message.from_user
    if str(user.id) in user_data_dict["users"]:
        Played=str(user_data_dict["users"][str(user.id)]["Matches"]["Played"])
        Won=str(user_data_dict["users"][str(user.id)]["Matches"]["Won"])
        Lost=str(user_data_dict["users"][str(user.id)]["Matches"]["Lost"])
        msg="Stats for -"+str(user.first_name)+"\n\nMatches:-\n"+"Played: "+Played+"\nWon: "+Won+"\nLost: "+Lost
    else:
        msg="Stats for -"+str(user.first_name)+"\n\nMatches:-\n"+"Played: 0\nWon: 0\nLost: 0"
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    
    return ConversationHandler.END


#playwithbot command
def playwithbot(update: Update, context: CallbackContext) -> int:
    
    if update.message:
        user = update.message.from_user
        logger.info("User %s challenge to bot", user.first_name)

    context.user_data[update.message.from_user.id] = [0,0,0,0,0,0,0]
    #print(context.user_data)
    keyboard = [
        [
            InlineKeyboardButton("Normal", callback_data=str(ONE)),
            InlineKeyboardButton("Hard", callback_data=str(TWO)),
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg="Are you challenging me?!\nWell then choose a Difficulty Level."

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_markup)
    query = update.callback_query
    
    
    return FIRST


def normal(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()


    keyboard = [
        [
            InlineKeyboardButton("Heads", callback_data=str(FOUR)),
            InlineKeyboardButton("Tails", callback_data=str(FIVE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg1="Player: "+update.callback_query.from_user.first_name+"\n"
    msg2="Against: Cricket Bot\n"
    msg3="It's time for Toss, Choose your Side."
    msg_markup=msg1+msg2+msg3 
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )
    return FIRST



def heads(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #print(update.callback_query.from_user.id)

    choice = ['heads', 'tails']
    rand_choice = random.choice(choice)
    logger.info(rand_choice)

    #context.user_data[update.callback_query.from_user.id] = [0,0,0,0,0,0,0,update.callback_query.from_user.id]
    #1- score 0-batting/bowling 2-bowls 3-inning  4-New score 5-bot score 6- new bot score
    #(compare(1,6)or compare(5,4))
    if rand_choice=='heads':
        keyboard = [
            [
                InlineKeyboardButton("Batting", callback_data=str(SEVEN)),
                InlineKeyboardButton("Bowling", callback_data=str(EIGHT)),
            ]

        ]
        msg_markup="You Won!\nWhat will you choose?"
    else:
        keyboard = [
            [
                InlineKeyboardButton("Start", callback_data=str(SIX)),
            ]
        ]
        msg_markup="You Lost!\nBot chose Bowling,\nPress Start to Start the Match!"
        context.user_data[update.callback_query.from_user.id][0]=1 #Batting
        context.user_data[update.callback_query.from_user.id][1]=0 #score
    

    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
     
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )



    return FIRST


def tails(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    choice = ['heads', 'tails']
    rand_choice = random.choice(choice)

    #context.user_data[update.callback_query.from_user.id] = [0,0,0,0,0,0,0,update.callback_query.from_user.id]

    if rand_choice=='tails':
        keyboard = [
            [
                InlineKeyboardButton("Batting", callback_data=str(SEVEN)),
                InlineKeyboardButton("Bowling", callback_data=str(EIGHT)),
            ]

        ]
        msg_markup="You Won!\nWhat will you choose?"

    else:
        keyboard = [
            [
                InlineKeyboardButton("Start", callback_data=str(SIX)),
            ]
        ]
        msg_markup="You Lost!\nBot chose Bowling,\nPress Start to Start the Match!"
        context.user_data[update.callback_query.from_user.id][0]=1 #Batting
        context.user_data[update.callback_query.from_user.id][1]=0 #score
    

    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
     
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )



    return FIRST


def play(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="11"),
            InlineKeyboardButton("2", callback_data="12"),
            InlineKeyboardButton("3", callback_data="13"),
            InlineKeyboardButton("4", callback_data="14"),
            InlineKeyboardButton("5", callback_data="15"),
            InlineKeyboardButton("6", callback_data="16"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if context.user_data[update.callback_query.from_user.id][0]==0:
        msg="1st Inning Starts\nYou are Bowling Right now\n"
        context.user_data[update.callback_query.from_user.id][2]+=1
        msg1="Bowl: "+str(context.user_data[update.callback_query.from_user.id][2])
    else:
        msg="1st Inning Starts\nYou are Batting Right now\n"
        msg1="Your Score: "+str(context.user_data[update.callback_query.from_user.id][1])
    
    msg2="\n"
    msg3="Choose Your Move:-"
    msg_markup=msg+msg1+msg2+msg3
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    return FIRST

def batting(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Start", callback_data=str(NINE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_markup="You chose Batting,\nPress Start to Start the Match!"
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )


    context.user_data[update.callback_query.from_user.id][0]=1

    return FIRST

def bowling(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Start", callback_data=str(TEN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_markup="You chose Bowling,\nPress Start to Start the Match!"
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    context.user_data[update.callback_query.from_user.id][0]=0

    return FIRST


def playbatting(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="11"),
            InlineKeyboardButton("2", callback_data="12"),
            InlineKeyboardButton("3", callback_data="13"),
            InlineKeyboardButton("4", callback_data="14"),
            InlineKeyboardButton("5", callback_data="15"),
            InlineKeyboardButton("6", callback_data="16"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg1="1st Inning Starts\n\n"
    msg2="Player: "+"\n"
    msg3="You are Batting Right now\n Choose Your Move:-"
    msg_markup=msg1+msg2+msg3
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    context.user_data[update.callback_query.from_user.id][0]=1



    return FIRST


def playbowling(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="11"),
            InlineKeyboardButton("2", callback_data="12"),
            InlineKeyboardButton("3", callback_data="13"),
            InlineKeyboardButton("4", callback_data="14"),
            InlineKeyboardButton("5", callback_data="15"),
            InlineKeyboardButton("6", callback_data="16"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg1="1st Inning Starts\n\n"
    msg2="Player: "+"\n"
    msg3="You are Bowling Right now\n Choose Your Move:-"
    msg_markup=msg1+msg2+msg3
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    context.user_data[update.callback_query.from_user.id][0]=0
    return FIRST


#Start Playing Mode
def play1(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    choice = [1,2,3,4,5,6]
    rand_choice = random.choice(choice)
    
    query = update.callback_query
    query.answer()    
    logger.info(update.callback_query.data)


    if query.data=="11":
        moves=1
    elif query.data=="12":
        moves=2
    elif query.data=="13":
        moves=3
    elif query.data=="14":
        moves=4
    elif query.data=="15":
        moves=5
    elif query.data=="16":
        moves=6
    else:
        moves=0

    

    if rand_choice!=moves:

        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="11"),
                InlineKeyboardButton("2", callback_data="12"),
                InlineKeyboardButton("3", callback_data="13"),
                InlineKeyboardButton("4", callback_data="14"),
                InlineKeyboardButton("5", callback_data="15"),
                InlineKeyboardButton("6", callback_data="16"),
            ]

        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if context.user_data[update.callback_query.from_user.id][3]==0:
            state="1st Inning\n"
        else:
            state="2nd Inning\n"

        if context.user_data[update.callback_query.from_user.id][0]==0:
            msg="You are Bowling Right now\n"
            context.user_data[update.callback_query.from_user.id][2]+=1
            msg1="Bowl: "+str(context.user_data[update.callback_query.from_user.id][2])
            context.user_data[update.callback_query.from_user.id][5]+=rand_choice

        else:
            msg="You are Batting Right now\n"
            context.user_data[update.callback_query.from_user.id][1]+=moves
            msg1="Your Score: "+str(context.user_data[update.callback_query.from_user.id][1])
        
        msg2="\n"
        msg3="Choose Your Move:-"
        msg_markup=state+msg+msg1+msg2+msg3

        query.edit_message_text(text="Bot Move:"+str(rand_choice)+"\nYour Move: "+str(moves))

        time.sleep(2)

        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
            )



    else:
        
        """Show new choice of buttons"""        
        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="11"),
                InlineKeyboardButton("2", callback_data="12"),
                InlineKeyboardButton("3", callback_data="13"),
                InlineKeyboardButton("4", callback_data="14"),
                InlineKeyboardButton("5", callback_data="15"),
                InlineKeyboardButton("6", callback_data="16"),
            ]

        ]
        context.user_data[update.callback_query.from_user.id][3]=1
        #context.user_data[update.callback_query.from_user.id][5]=1
        #context.user_data[update.callback_query.from_user.id][4]=context.user_data[update.callback_query.from_user.id][1]
        if context.user_data[update.callback_query.from_user.id][0]==0:
            context.user_data[update.callback_query.from_user.id][0]=1
        else:
            context.user_data[update.callback_query.from_user.id][0]=0

        reply_markup = InlineKeyboardMarkup(keyboard)

        
        if context.user_data[update.callback_query.from_user.id][5]!=0:
            score=context.user_data[update.callback_query.from_user.id][5]
            tg=""
        else:
            score=context.user_data[update.callback_query.from_user.id][1]
            tg="Bot "

        
        msg_markup="2nd Inning Starts\n\n"+tg+"Target :"+str(score)+"\nYour Score: 0\nChoose your move:"

        query.edit_message_text(text="Bold!\nBot Move:"+str(rand_choice)+"\nYour Move: "+str(moves))

        time.sleep(2)

        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )
        # Transfer to conversation state `SECOND`
        return SECOND


    return FIRST

def play1_end(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    choice = [1,2,3,4,5,6]
    rand_choice = random.choice(choice)
    logger.info(rand_choice)
    query = update.callback_query
    query.answer()    

    if query.data=="11":
        moves=1
    elif query.data=="12":
        moves=2
    elif query.data=="13":
        moves=3
    elif query.data=="14":
        moves=4
    elif query.data=="15":
        moves=5
    elif query.data=="16":
        moves=6
    else:
        moves=0

    
    if rand_choice!=moves:

        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="11"),
                InlineKeyboardButton("2", callback_data="12"),
                InlineKeyboardButton("3", callback_data="13"),
                InlineKeyboardButton("4", callback_data="14"),
                InlineKeyboardButton("5", callback_data="15"),
                InlineKeyboardButton("6", callback_data="16"),
            ]

        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if context.user_data[update.callback_query.from_user.id][3]==0:
            state="1st Inning\n"
        else:
            state="2nd Inning\n"

        if context.user_data[update.callback_query.from_user.id][0]==0:
            msg="You are Bowling Right now\n"
            context.user_data[update.callback_query.from_user.id][2]+=1
            msg1="Bowl: "+str(context.user_data[update.callback_query.from_user.id][2])
            context.user_data[update.callback_query.from_user.id][6]+=rand_choice

            if context.user_data[update.callback_query.from_user.id][1]>context.user_data[update.callback_query.from_user.id][6]:
                query.edit_message_text(text="You Won! by "+str(context.user_data[update.callback_query.from_user.id][1]-context.user_data[update.callback_query.from_user.id][6]))
                Won=1
                Lost=0
                if str(update.callback_query.from_user.id) in user_data_dict["users"]:
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Played"]+=1
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Won"]+=Won
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Lost"]+=Lost
                    with open("user.json", "w") as outfile:
                        json.dump(user_data_dict, outfile)
                else:
                    new_data={str(update.callback_query.from_user.id):{"Matches":{"Played":1,"Won":Won,"Lost":Lost}}}
                    user_data_dict["users"].update(new_data)
                    #print(user_data_dict)
                    # Serializing json 
                    #json_object = json.dumps(user_data_dict, indent = 4)
                    # Writing to sample.json
                    with open("user.json", "w") as outfile:
                        json.dump(user_data_dict, outfile)

                return ConversationHandler.END

            else:
                query.edit_message_text(text="You Lose! by "+str(context.user_data[update.callback_query.from_user.id][6]-context.user_data[update.callback_query.from_user.id][1]))
                Lost=1
                Won=0
                if str(update.callback_query.from_user.id) in user_data_dict["users"]:
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Played"]+=1
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Won"]+=Won
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Lost"]+=Lost
                    with open("user.json", "w") as outfile:
                        json.dump(user_data_dict, outfile)
                else:
                    new_data={str(update.callback_query.from_user.id):{"Matches":{"Played":1,"Won":Won,"Lost":Lost}}}
                    user_data_dict["users"].update(new_data)
                    #print(user_data_dict)
                    # Serializing json 
                    #json_object = json.dumps(user_data_dict, indent = 4)
                    # Writing to sample.json
                    with open("user.json", "w") as outfile:
                        json.dump(user_data_dict, outfile)

                return ConversationHandler.END



        else:
            msg="You are Batting Right now\n"
            context.user_data[update.callback_query.from_user.id][4]+=moves
            msg1="Your Score: "+str(context.user_data[update.callback_query.from_user.id][4])
        
        msg2="\n"
        msg3="Choose Your Move:-"
        msg_markup=state+msg+msg1+msg2+msg3

        query.edit_message_text(text="Bot Move:"+str(rand_choice)+"\nYour Move: "+str(moves))

        time.sleep(2)

        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
            )

    else:
        """Returns `ConversationHandler.END`, which tells the
        ConversationHandler that the conversation is over.
        """
        Won=0
        Lost=0
        if context.user_data[update.callback_query.from_user.id][1]!=0:
            if context.user_data[update.callback_query.from_user.id][1]>context.user_data[update.callback_query.from_user.id][6]:
                query.edit_message_text(text="You Won! by "+str(context.user_data[update.callback_query.from_user.id][1]-context.user_data[update.callback_query.from_user.id][6]))
                Won=1
            elif context.user_data[update.callback_query.from_user.id][1]==context.user_data[update.callback_query.from_user.id][6]:
                query.edit_message_text(text="Match Drawn!!")
            else:
                query.edit_message_text(text="You Lose! by "+str(context.user_data[update.callback_query.from_user.id][6]-context.user_data[update.callback_query.from_user.id][1]))
                Lost=1
        elif context.user_data[update.callback_query.from_user.id][5]!=0:
            if context.user_data[update.callback_query.from_user.id][4]>context.user_data[update.callback_query.from_user.id][5]:
                query.edit_message_text(text="You Won! by "+str(context.user_data[update.callback_query.from_user.id][4]-context.user_data[update.callback_query.from_user.id][5]))
                Won=1
            elif context.user_data[update.callback_query.from_user.id][4]==context.user_data[update.callback_query.from_user.id][5]:
                query.edit_message_text(text="Match Drawn!!")
            else:
                query.edit_message_text(text="You Lose! by "+str(context.user_data[update.callback_query.from_user.id][5]-context.user_data[update.callback_query.from_user.id][4]))
                Lost=1
        else:
            query.edit_message_text(text="See you next time!")
            
        if str(update.callback_query.from_user.id) in user_data_dict["users"]:
            user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Played"]+=1
            user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Won"]+=Won
            user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Lost"]+=Lost

            #print(user_data_dict)        
            with open("user.json", "w") as outfile:
                json.dump(user_data_dict, outfile)
        else:
            # Data to be written
            new_data={str(update.callback_query.from_user.id):{
            "Matches":{
                    "Played":1,
                    "Won":Won,
                    "Lost":Lost
                        }
            }}
         
            user_data_dict["users"].update(new_data)
            #print(user_data_dict)
            # Serializing json 
            #json_object = json.dumps(user_data_dict, indent = 4)
            # Writing to sample.json
            with open("user.json", "w") as outfile:
                json.dump(user_data_dict, outfile)




        return ConversationHandler.END
        

    return SECOND


#End Playing Mode



def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END



def three(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
            InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Third CallbackQueryHandler. Do want to start over?", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SECOND

#challenge command
def challenge(update: Update, context: CallbackContext):
    """Send message on `/challenge`."""
    # Get user that sent /challenge
    user = update.message.from_user
    #Add group Inline Keyboard
    keyboard = [
        [
            InlineKeyboardButton("Add to Group!", url="https://telegram.me/crick_test_bot?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    msg="Hello "+user.first_name+"\n Please Add bot to group to challenge your Friends."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_markup)

    return ConversationHandler.END

#B person challenge command
def challenge_start(update: Update, context: CallbackContext)-> int:

    query=update.message

    if(query.reply_to_message.text=="/challenge@crick_test_bot"):
        context.chat_data[query.chat.id]={
            query.reply_to_message.from_user.id:[-1,0,0,0,0,0,0,-1],
            query.from_user.id:[0,0,0,0,0,0,0,-1],
            "players":[query.reply_to_message.from_user.first_name,query.from_user.first_name,query.reply_to_message.from_user.id,query.from_user.id],
            "moves":[-1,-1],

        }
        

        #context.user_data[update.callback_query.from_user.id] = [0,0,0,0,0,0,0,update.callback_query.from_user.id]
        #0-batting/bowling 
        #1- score  
        #2-bowls 
        #3-inning  
        #4-New score 
        #5-apponent score 
        #6- new apponent score
        # 7<-- Head/Tail
        #(compare(1,6)or compare(5,4))

        #print('chat data',context.chat_data[query.chat.id])
        #print(query.reply_to_message.from_user.id,query.reply_to_message.text)
        #print("query: ",query.from_user.id,"\ncontext.user_data",context.user_data,"\ncontext: ",context)

        keyboard = [
            [
                InlineKeyboardButton("Go for Toss", callback_data=str(ONE)),
                InlineKeyboardButton("Cancel", callback_data=str(TWO)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text="You Accepted the challenge\nTime for Toss", reply_markup=reply_markup)
        # Transfer to conversation state `THIRD`
        return FIRST
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply the message: /challenge@crick_test_bot to start the match.")
        return ConversationHandler.END


#A person challenge_group command
def challenge_group(update: Update, context: CallbackContext)-> int:

    msg="Ask your Friend to accept the challenge BY replying the message (/challenge@crick_test_bot) as /accept\n Wait till your Friend accept the challenge.\n After challenge accepted Go for Toss."
    #update.message.from_user
    keyboard = [
        [
            InlineKeyboardButton("Go for Toss", callback_data=str(ONE)),
            InlineKeyboardButton("Cancel", callback_data=str(TWO)),
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_markup)

    # Transfer to conversation state `SECOND`
    return FIRST


#A Person
def ok_group(update: Update, context: CallbackContext)-> int:
    query = update.callback_query
    query.answer()

    users=context.chat_data[query.message.chat.id]["players"]
    keyboard = [
        [
            InlineKeyboardButton("Heads", callback_data=str(FOUR)),
            InlineKeyboardButton("Tails", callback_data=str(FIVE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg1="Player: "+update.callback_query.from_user.first_name+"\n"
    msg2="Against: "+users[1]+"\n"
    msg3="It's time for Toss, Choose your Side."
    msg_markup=msg1+msg2+msg3 
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )
    return FIRST


def cancel_group(update: Update, context: CallbackContext)-> int:
    
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="See you next time!"
    )
    return ConversationHandler.END

#################################### Group Play ####################################




#B Person
def toss(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    users=context.chat_data[query.message.chat.id]["players"]
    keyboard = [
        [
            InlineKeyboardButton("Heads", callback_data=str(FOUR)),
            InlineKeyboardButton("Tails", callback_data=str(FIVE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg1="Player: "+update.callback_query.from_user.first_name+"\n"
    msg2="Against: "+users[0]+"\n"
    msg3="It's time for Toss, Choose your Side."
    msg_markup=msg1+msg2+msg3 
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )
    return FIRST

#B Person
def Gheads(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #print(update.callback_query.from_user.id)
    if update.callback_query.from_user.id in context.chat_data[query.message.chat.id]:
        #context.chat_data[query.message.chat.id][update.callback_query.from_user.id][7]=0
        users=context.chat_data[query.message.chat.id]["players"]
        context.chat_data[query.message.chat.id][users[2]][7]=0

        msg_markup= str(update.callback_query.from_user.first_name)+" : Toss done."
        keyboard = [
            [
                InlineKeyboardButton("Wait for: "+str(users[0]), callback_data="12"),
            ]

        ]

        reply_markup = InlineKeyboardMarkup(keyboard) 
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )

        return FIRST


#B Person
def GRheads(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #print(update.callback_query.from_user.id)
    if update.callback_query.from_user.id in context.chat_data[query.message.chat.id]:
        context.chat_data[query.message.chat.id][update.callback_query.from_user.id][7]=0
        users=context.chat_data[query.message.chat.id]["players"]
        
        timeout=0
        rand_choice=context.chat_data[query.message.chat.id][users[2]][7]
        
        #print("rand",rand_choice)
        if rand_choice==-1:
            while(timeout!=5 and context.chat_data[query.message.chat.id][users[2]][7]==-1):
                time.sleep(2)
                timeout+=1
                print(timeout)
        else:
            rand_choice=context.chat_data[query.message.chat.id][users[2]][7]

        #context.user_data[update.callback_query.from_user.id] = [0,0,0,0,0,0,0,update.callback_query.from_user.id]
        #1- score 0-batting/bowling 2-bowls 3-inning  4-New score 5-bot score 6- new bot score
        #(compare(1,6)or compare(5,4))
        if rand_choice==0:
            keyboard = [
                [
                    InlineKeyboardButton("Batting", callback_data=str(SEVEN)),
                    InlineKeyboardButton("Bowling", callback_data=str(EIGHT)),
                ]

            ]
            msg_markup="You Won!\nWhat will you choose?"
        elif rand_choice==1:
            keyboard = [
                [
                    InlineKeyboardButton("Next", callback_data="preplay"),
                ]
            ]
            msg_markup="You Lost! Go For Match.\n"+str(users[0])+"will choose between Batting and Bowling."
            #context.user_data[update.callback_query.from_user.id][0]=1 #Batting
            #context.user_data[update.callback_query.from_user.id][1]=0 #score
        else:
            keyboard = [
                [
                    InlineKeyboardButton("Sorry! Try next time.", callback_data=str(TWO)),
                ]
            ]
            msg_markup="Please ask your challenger to answer within 10 Sec."
            #context.user_data[update.callback_query.from_user.id][0]=1 #Batting
            #context.user_data[update.callback_query.from_user.id][1]=0 #score
        

        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
         
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )



        return FIRST


    else:
        user1=context.chat_data[query.message.chat.id]["players"][0]
        user2=context.chat_data[query.message.chat.id]["players"][1]
        keyboard = [
            [
                InlineKeyboardButton("Heads", callback_data=str(FOUR)),
                InlineKeyboardButton("Tails", callback_data=str(FIVE)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg1="Player: "+update.callback_query.from_user.first_name+"\n"
        msg2="Against: "+user1+"\n"
        msg3="It's time for Toss, Choose your Side."
        msg_markup=msg1+msg2+msg3 
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )
        return FIRST

#A Person
def Oheads(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #print(update.callback_query.from_user.id)
    if update.callback_query.from_user.id in context.chat_data[query.message.chat.id]:
        #context.chat_data[query.message.chat.id][update.callback_query.from_user.id][7]=0
        users=context.chat_data[query.message.chat.id]["players"]
        context.chat_data[query.message.chat.id][users[3]][7]=0

        msg_markup= str(update.callback_query.from_user.first_name)+" : Toss done."
        keyboard = [
            [
                InlineKeyboardButton("Wait for: "+str(users[1]), callback_data="12"),
            ]

        ]

        reply_markup = InlineKeyboardMarkup(keyboard) 
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )

        return FIRST



def ORheads(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #print(update.callback_query.from_user.id)
    if update.callback_query.from_user.id in context.chat_data[query.message.chat.id]:
        #context.chat_data[query.message.chat.id][update.callback_query.from_user.id][7]=0
        users=context.chat_data[query.message.chat.id]["players"]

        timeout=0

        rand_choice=context.chat_data[query.message.chat.id][users[3]][7]
        #print("rand",rand_choice)
        if(rand_choice==-1):
            while(timeout!=5 and context.chat_data[query.message.chat.id][users[3]][7]==-1):
                time.sleep(2)
                timeout+=1
                print(timeout)
        else:
            rand_choice=context.chat_data[query.message.chat.id][users[3]][7]

        #context.user_data[update.callback_query.from_user.id] = [0,0,0,0,0,0,0,update.callback_query.from_user.id]
        #1- score 0-batting/bowling 2-bowls 3-inning  4-New score 5-bot score 6- new bot score
        #(compare(1,6)or compare(5,4))
        if rand_choice==1:
            keyboard = [
                [
                    InlineKeyboardButton("Batting", callback_data=str(SEVEN)),
                    InlineKeyboardButton("Bowling", callback_data=str(EIGHT)),
                ]

            ]
            msg_markup="You Won!\nWhat will you choose?"
        elif rand_choice==0:
            keyboard = [
                [
                    InlineKeyboardButton("Next", callback_data="preplay"),
                ]
            ]
            msg_markup="You Lost!"+str(users[1])+"\nwill choose Batting or Bowling,\nPress Start to for Match!"
            #context.user_data[update.callback_query.from_user.id][0]=1 #Batting
            #context.user_data[update.callback_query.from_user.id][1]=0 #score
        else:
            keyboard = [
                [
                    InlineKeyboardButton("Sorry! Try next time.", callback_data=str(TWO)),
                ]
            ]
            msg_markup="Please ask your challenger to answer within 10 Sec."
            #context.user_data[update.callback_query.from_user.id][0]=1 #Batting
            #context.user_data[update.callback_query.from_user.id][1]=0 #score

        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
         
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )



        return FIRST


    else:
        user1=context.chat_data[query.message.chat.id]["players"][0]
        user2=context.chat_data[query.message.chat.id]["players"][1]
        keyboard = [
            [
                InlineKeyboardButton("Heads", callback_data=str(FOUR)),
                InlineKeyboardButton("Tails", callback_data=str(FIVE)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg1="Player: "+update.callback_query.from_user.first_name+"\n"
        msg2="Against: "+user1+"\n"
        msg3="It's time for Toss, Choose your Side."
        msg_markup=msg1+msg2+msg3 
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )
        return FIRST




# Tails 

#B Person
def Gtails(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #print(update.callback_query.from_user.id)
    if update.callback_query.from_user.id in context.chat_data[query.message.chat.id]:
        #context.chat_data[query.message.chat.id][update.callback_query.from_user.id][7]=0
        users=context.chat_data[query.message.chat.id]["players"]
        context.chat_data[query.message.chat.id][users[2]][7]=1

        msg_markup= str(update.callback_query.from_user.first_name)+" : Toss done."
        keyboard = [
            [
                InlineKeyboardButton("Wait for: "+str(users[0]), callback_data="13"),
            ]

        ]

        reply_markup = InlineKeyboardMarkup(keyboard) 
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )

        return FIRST


#B Person
def GRtails(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #print(update.callback_query.from_user.id)
    if update.callback_query.from_user.id in context.chat_data[query.message.chat.id]:
        context.chat_data[query.message.chat.id][update.callback_query.from_user.id][7]=0
        users=context.chat_data[query.message.chat.id]["players"]
        
        timeout=0
        rand_choice=context.chat_data[query.message.chat.id][users[2]][7]
        
        #print("rand",rand_choice)
        if rand_choice==-1:
            while(timeout!=5 and context.chat_data[query.message.chat.id][users[2]][7]==-1):
                time.sleep(2)
                timeout+=1
                print(timeout)
        else:
            rand_choice=context.chat_data[query.message.chat.id][users[2]][7]

        #context.user_data[update.callback_query.from_user.id] = [0,0,0,0,0,0,0,update.callback_query.from_user.id]
        #1- score 0-batting/bowling 2-bowls 3-inning  4-New score 5-bot score 6- new bot score
        #(compare(1,6)or compare(5,4))
        if rand_choice==1:
            keyboard = [
                [
                    InlineKeyboardButton("Batting", callback_data=str(SEVEN)),
                    InlineKeyboardButton("Bowling", callback_data=str(EIGHT)),
                ]

            ]
            msg_markup="You Won!\nWhat will you choose?"
        elif rand_choice==0:
            keyboard = [
                [
                    InlineKeyboardButton("Next", callback_data="preplay"),
                ]
            ]
            msg_markup="You Lost! Go For Match.\n"+str(users[0])+"will choose between Batting and Bowling."
            #context.user_data[update.callback_query.from_user.id][0]=1 #Batting
            #context.user_data[update.callback_query.from_user.id][1]=0 #score
        else:
            keyboard = [
                [
                    InlineKeyboardButton("Sorry! Try next time.", callback_data=str(TWO)),
                ]
            ]
            msg_markup="Please ask your challenger to answer within 10 Sec."
            #context.user_data[update.callback_query.from_user.id][0]=1 #Batting
            #context.user_data[update.callback_query.from_user.id][1]=0 #score
        

        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
         
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )



        return FIRST


    else:
        user1=context.chat_data[query.message.chat.id]["players"][0]
        user2=context.chat_data[query.message.chat.id]["players"][1]
        keyboard = [
            [
                InlineKeyboardButton("Heads", callback_data=str(FOUR)),
                InlineKeyboardButton("Tails", callback_data=str(FIVE)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg1="Player: "+update.callback_query.from_user.first_name+"\n"
        msg2="Against: "+user1+"\n"
        msg3="It's time for Toss, Choose your Side."
        msg_markup=msg1+msg2+msg3 
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )
        return FIRST

#A Person
def Otails(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #print(update.callback_query.from_user.id)
    if update.callback_query.from_user.id in context.chat_data[query.message.chat.id]:
        #context.chat_data[query.message.chat.id][update.callback_query.from_user.id][7]=0
        users=context.chat_data[query.message.chat.id]["players"]
        context.chat_data[query.message.chat.id][users[3]][7]=1

        msg_markup= str(update.callback_query.from_user.first_name)+" : Toss done."
        keyboard = [
            [
                InlineKeyboardButton("Wait for: "+str(users[1]), callback_data="13"),
            ]

        ]

        reply_markup = InlineKeyboardMarkup(keyboard) 
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )

        return FIRST



def ORtails(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #print(update.callback_query.from_user.id)
    if update.callback_query.from_user.id in context.chat_data[query.message.chat.id]:
        #context.chat_data[query.message.chat.id][update.callback_query.from_user.id][7]=0
        users=context.chat_data[query.message.chat.id]["players"]

        timeout=0

        rand_choice=context.chat_data[query.message.chat.id][users[3]][7]
        #print("rand",rand_choice)
        if(rand_choice==-1):
            while(timeout!=5 and context.chat_data[query.message.chat.id][users[3]][7]==-1):
                time.sleep(2)
                timeout+=1
                print(timeout)
        else:
            rand_choice=context.chat_data[query.message.chat.id][users[3]][7]

        #context.user_data[update.callback_query.from_user.id] = [0,0,0,0,0,0,0,update.callback_query.from_user.id]
        #1- score 0-batting/bowling 2-bowls 3-inning  4-New score 5-bot score 6- new bot score
        #(compare(1,6)or compare(5,4))
        if rand_choice==0:
            keyboard = [
                [
                    InlineKeyboardButton("Batting", callback_data=str(SEVEN)),
                    InlineKeyboardButton("Bowling", callback_data=str(EIGHT)),
                ]

            ]
            msg_markup="You Won!\nWhat will you choose?"
        elif rand_choice==1:
            keyboard = [
                [
                    InlineKeyboardButton("Next", callback_data="preplay"),
                ]
            ]
            msg_markup="You Lost!"+str(users[1])+"\nwill choose Batting or Bowling,\nPress Start to for Match!"
            #context.user_data[update.callback_query.from_user.id][0]=1 #Batting
            #context.user_data[update.callback_query.from_user.id][1]=0 #score
        else:
            keyboard = [
                [
                    InlineKeyboardButton("Sorry! Try next time.", callback_data=str(TWO)),
                ]
            ]
            msg_markup="Please ask your challenger to answer within 10 Sec."
            #context.user_data[update.callback_query.from_user.id][0]=1 #Batting
            #context.user_data[update.callback_query.from_user.id][1]=0 #score

        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
         
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )



        return FIRST


    else:
        user1=context.chat_data[query.message.chat.id]["players"][0]
        user2=context.chat_data[query.message.chat.id]["players"][1]
        keyboard = [
            [
                InlineKeyboardButton("Heads", callback_data=str(FOUR)),
                InlineKeyboardButton("Tails", callback_data=str(FIVE)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg1="Player: "+update.callback_query.from_user.first_name+"\n"
        msg2="Against: "+user1+"\n"
        msg3="It's time for Toss, Choose your Side."
        msg_markup=msg1+msg2+msg3 
        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )
        return FIRST


#B person
#preGplay
def preplay(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    users=context.chat_data[query.message.chat.id]["players"]

    if context.chat_data[query.message.chat.id][users[2]][0]==0:
        context.chat_data[query.message.chat.id][users[3]][0]=1
    else:
        context.chat_data[query.message.chat.id][users[3]][0]=0


    keyboard = [
        [
            InlineKeyboardButton("Start", callback_data=str(SIX)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg="Starting 1st Inning\nPress Start to start\n"+"Player: "+str(update.callback_query.from_user.first_name)+"\n\nNote: Wait till your opponent choose.."

    query.edit_message_text(
        text=msg, reply_markup=reply_markup
    )

    return FIRST

def Gplay(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    users=context.chat_data[query.message.chat.id]["players"]
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="11"),
            InlineKeyboardButton("2", callback_data="112"),
            InlineKeyboardButton("3", callback_data="113"),
            InlineKeyboardButton("4", callback_data="114"),
            InlineKeyboardButton("5", callback_data="115"),
            InlineKeyboardButton("6", callback_data="116"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if context.chat_data[query.message.chat.id][users[2]][0]==0:
        msg="1st Inning Starts\nYou are Bowling Right now\n"+"Player: "+str(update.callback_query.from_user.first_name)+"\n"
        context.chat_data[query.message.chat.id][users[2]][2]+=1
        msg1="Bowl: "+str(context.chat_data[query.message.chat.id][users[2]][2])
    else:
        msg="1st Inning Starts\nYou are Batting Right now\n"+"Player: "+str(update.callback_query.from_user.first_name)+"\n"
        msg1="Your Score: "+str(context.chat_data[query.message.chat.id][users[2]][1])
    
    msg2="\n"
    msg3="Choose Your Move:-"
    msg_markup=msg+msg1+msg2+msg3
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    return FIRST

#A person

def Oplay(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    users=context.chat_data[query.message.chat.id]["players"]
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="11"),
            InlineKeyboardButton("2", callback_data="112"),
            InlineKeyboardButton("3", callback_data="113"),
            InlineKeyboardButton("4", callback_data="114"),
            InlineKeyboardButton("5", callback_data="115"),
            InlineKeyboardButton("6", callback_data="116"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if context.chat_data[query.message.chat.id][users[3]][0]==0:
        msg="1st Inning Starts\nYou are Bowling Right now\n"+"Player: "+str(update.callback_query.from_user.first_name)+"\n"
        context.chat_data[query.message.chat.id][users[3]][2]+=1
        msg1="Bowl: "+str(context.chat_data[query.message.chat.id][users[3]][2])
    else:
        msg="1st Inning Starts\nYou are Batting Right now\n"+"Player: "+str(update.callback_query.from_user.first_name)+"\n"
        msg1="Your Score: "+str(context.chat_data[query.message.chat.id][users[3]][1])
    
    msg2="\n"
    msg3="Choose Your Move:-"
    msg_markup=msg+msg1+msg2+msg3
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    return FIRST



#B person
def Gbatting(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    users=context.chat_data[query.message.chat.id]["players"]
    keyboard = [
        [
            InlineKeyboardButton("Start", callback_data=str(NINE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_markup="You chose Batting,\nPress Start to Start the Match!"
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )


    context.chat_data[query.message.chat.id][users[2]][0]=1
    context.chat_data[query.message.chat.id][users[3]][0]=0

    return FIRST

#B person
def Gbowling(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    users=context.chat_data[query.message.chat.id]["players"]
    keyboard = [
        [
            InlineKeyboardButton("Start", callback_data=str(TEN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_markup="You chose Bowling,\nPress Start to Start the Match!"
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    context.chat_data[query.message.chat.id][users[2]][0]=0
    context.chat_data[query.message.chat.id][users[3]][0]=1

    return FIRST


#A Person

def Obatting(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    users=context.chat_data[query.message.chat.id]["players"]
    keyboard = [
        [
            InlineKeyboardButton("Start", callback_data=str(NINE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_markup="You chose Batting,\nPress Start to Start the Match!"
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    #message
    context.chat_data[query.message.chat.id][users[3]][0]=1
    context.chat_data[query.message.chat.id][users[2]][0]=0

    return FIRST


#A person
def Obowling(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    users=context.chat_data[query.message.chat.id]["players"]
    keyboard = [
        [
            InlineKeyboardButton("Start", callback_data=str(TEN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_markup="You chose Bowling,\nPress Start to Start the Match!"
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    #message
    context.chat_data[query.message.chat.id][users[3]][0]=0
    context.chat_data[query.message.chat.id][users[2]][0]=1

    return FIRST



#B Person
def Gplaybatting(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    users=context.chat_data[query.message.chat.id]["players"]

    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="11"),
            InlineKeyboardButton("2", callback_data="112"),
            InlineKeyboardButton("3", callback_data="113"),
            InlineKeyboardButton("4", callback_data="114"),
            InlineKeyboardButton("5", callback_data="115"),
            InlineKeyboardButton("6", callback_data="116"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg1="1st Inning Starts\n\n"
    msg2="Player: "+str(update.callback_query.from_user.first_name)+"\n"
    msg3="You are Batting Right now\n Choose Your Move:-"
    msg_markup=msg1+msg2+msg3
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    #context.chat_data[query.chat.id][update.callback_query.from_user.id][0]=1



    return FIRST

#B person & A Person
def Gplaybowling(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    users=context.chat_data[query.message.chat.id]["players"]
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="11"),
            InlineKeyboardButton("2", callback_data="112"),
            InlineKeyboardButton("3", callback_data="113"),
            InlineKeyboardButton("4", callback_data="114"),
            InlineKeyboardButton("5", callback_data="115"),
            InlineKeyboardButton("6", callback_data="116"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg1="1st Inning Starts\n\n"
    msg2="Player: "+str(update.callback_query.from_user.first_name)+"\n"
    msg3="You are Bowling Right now\n Choose Your Move:-"
    msg_markup=msg1+msg2+msg3
    query.edit_message_text(
        text=msg_markup, reply_markup=reply_markup
    )

    #context.chat_data[query.chat.id][update.callback_query.from_user.id][0]=0
    return FIRST



#Start Playing Mode

#B person
def Gplay1(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()    

    moves=context.chat_data[query.message.chat.id]["moves"]
    print(query.data)

    if query.data=="11":
        moves[1]=1
    elif query.data=="112":
        moves[1]=2
    elif query.data=="113":
        moves[1]=3
    elif query.data=="114":
        moves[1]=4
    elif query.data=="115":
        moves[1]=5
    elif query.data=="116":
        moves[1]=6
    else:
        moves[1]=0

    """Show new choice of buttons"""        
    keyboard = [
        [
            InlineKeyboardButton("Next", callback_data="14"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    users=context.chat_data[query.message.chat.id]["players"]
    
    query.edit_message_text(text="Wait for :"+str(users[1])+" move.", reply_markup=reply_markup)

    return FIRST


#B person
def GRplay1(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""

    
    query = update.callback_query
    query.answer()    
    logger.info(update.callback_query.data)
    
    moves=context.chat_data[query.message.chat.id]["moves"]
    users=context.chat_data[query.message.chat.id]["players"]

    rand_choice = moves[0]

    if rand_choice!=moves[1]:

        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="11"),
                InlineKeyboardButton("2", callback_data="112"),
                InlineKeyboardButton("3", callback_data="113"),
                InlineKeyboardButton("4", callback_data="114"),
                InlineKeyboardButton("5", callback_data="115"),
                InlineKeyboardButton("6", callback_data="116"),
            ]

        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if context.chat_data[query.message.chat.id][users[2]][3]==0:
            state="1st Inning\n"
        else:
            state="2nd Inning\n"

        if context.chat_data[query.message.chat.id][users[2]][0]==0:
            msg="You are Bowling Right now\n"
            context.chat_data[query.message.chat.id][users[2]][2]+=1
            msg1="Bowl: "+str(context.chat_data[query.message.chat.id][users[2]][2])
            context.chat_data[query.message.chat.id][users[2]][5]+=rand_choice

        else:
            msg="You are Batting Right now\n"
            context.chat_data[query.message.chat.id][users[2]][1]+=moves[1]
            msg1="Your Score: "+str(context.chat_data[query.message.chat.id][users[2]][1])
        
        msg2="\n"
        msg3="Choose Your Move:-"
        msg_markup=state+msg+msg1+msg2+msg3

        query.edit_message_text(text=str(users[1])+" Move:"+str(rand_choice)+"\nYour Move: "+str(moves[1]))

        time.sleep(2)

        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
            )



    else:
        
        """Show new choice of buttons"""        
        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="11"),
                InlineKeyboardButton("2", callback_data="112"),
                InlineKeyboardButton("3", callback_data="113"),
                InlineKeyboardButton("4", callback_data="114"),
                InlineKeyboardButton("5", callback_data="115"),
                InlineKeyboardButton("6", callback_data="116"),
            ]

        ]
        context.chat_data[query.message.chat.id][users[2]][3]=1
        #context.chat_data[query.message.chat.id][users[2]][5]=1
        #context.user_data[update.callback_query.from_user.id][4]=context.user_data[update.callback_query.from_user.id][1]
        if context.chat_data[query.message.chat.id][users[2]][0]==0:
            context.chat_data[query.message.chat.id][users[2]][0]=1
        else:
            context.chat_data[query.message.chat.id][users[2]][0]=0

        reply_markup = InlineKeyboardMarkup(keyboard)

        
        if context.chat_data[query.message.chat.id][users[2]][5]!=0:
            score=context.chat_data[query.message.chat.id][users[2]][5]
            tg=""
        else:
            score=context.chat_data[query.message.chat.id][users[2]][1]
            tg=str(users[1])

        
        msg_markup="2nd Inning Starts\n\n"+tg+"Target :"+str(score)+"\nChoose your move:"

        query.edit_message_text(text="Bold!\n"+str(users[1])+" Move:"+str(rand_choice)+"\nYour Move: "+str(moves[1]))
        
        time.sleep(2)

        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )
        # Transfer to conversation state `SECOND`
        return SECOND


    return FIRST




#A person
def Oplay1(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()    

    moves=context.chat_data[query.message.chat.id]["moves"]
    
    print(query.data)

    if query.data=="11":
        moves[0]=1
    elif query.data=="112":
        moves[0]=2
    elif query.data=="113":
        moves[0]=3
    elif query.data=="114":
        moves[0]=4
    elif query.data=="115":
        moves[0]=5
    elif query.data=="116":
        moves[0]=6
    else:
        moves[0]=0
    

    """Show new choice of buttons"""        
    keyboard = [
        [
            InlineKeyboardButton("Next", callback_data="14"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    users=context.chat_data[query.message.chat.id]["players"]
    
    query.edit_message_text(text="Wait for :"+str(users[0])+" move.", reply_markup=reply_markup)

    return FIRST


#A person
def ORplay1(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""

    
    query = update.callback_query
    query.answer()    
    logger.info(update.callback_query.data)
    

    moves=context.chat_data[query.message.chat.id]["moves"]
    users=context.chat_data[query.message.chat.id]["players"]

    rand_choice = moves[1]

    if rand_choice!=moves[0]:

        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="11"),
                InlineKeyboardButton("2", callback_data="112"),
                InlineKeyboardButton("3", callback_data="113"),
                InlineKeyboardButton("4", callback_data="114"),
                InlineKeyboardButton("5", callback_data="115"),
                InlineKeyboardButton("6", callback_data="116"),
            ]

        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if context.chat_data[query.message.chat.id][users[3]][3]==0:
            state="1st Inning\n"
        else:
            state="2nd Inning\n"

        if context.chat_data[query.message.chat.id][users[3]][0]==0:
            msg="You are Bowling Right now\n"
            context.chat_data[query.message.chat.id][users[3]][2]+=1
            msg1="Bowl: "+str(context.chat_data[query.message.chat.id][users[3]][2])
            context.chat_data[query.message.chat.id][users[3]][5]+=rand_choice

        else:
            msg="You are Batting Right now\n"
            context.chat_data[query.message.chat.id][users[3]][1]+=moves[0]
            msg1="Your Score: "+str(context.chat_data[query.message.chat.id][users[3]][1])
        
        msg2="\n"
        msg3="Choose Your Move:-"
        msg_markup=state+msg+msg1+msg2+msg3

        query.edit_message_text(text=str(users[0])+" Move:"+str(rand_choice)+"\nYour Move: "+str(moves[0]))

        time.sleep(2)

        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
            )



    else:
        
        """Show new choice of buttons"""        
        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="11"),
                InlineKeyboardButton("2", callback_data="112"),
                InlineKeyboardButton("3", callback_data="113"),
                InlineKeyboardButton("4", callback_data="114"),
                InlineKeyboardButton("5", callback_data="115"),
                InlineKeyboardButton("6", callback_data="116"),
            ]

        ]
        context.chat_data[query.message.chat.id][users[3]][3]=1
        #context.chat_data[query.message.chat.id][users[3]][5]=1
        #context.user_data[update.callback_query.from_user.id][4]=context.user_data[update.callback_query.from_user.id][1]
        if context.chat_data[query.message.chat.id][users[3]][0]==0:
            context.chat_data[query.message.chat.id][users[3]][0]=1
        else:
            context.chat_data[query.message.chat.id][users[3]][0]=0

        reply_markup = InlineKeyboardMarkup(keyboard)

        
        if context.chat_data[query.message.chat.id][users[3]][5]!=0:
            score=context.chat_data[query.message.chat.id][users[3]][5]
            tg=""
        else:
            score=context.chat_data[query.message.chat.id][users[3]][1]
            tg=str(users[0])

        
        msg_markup="2nd Inning Starts\n\n"+tg+"Target :"+str(score)+"\nChoose your move:"

        query.edit_message_text(text="Bold!\n"+str(users[0])+" Move:"+str(rand_choice)+"\nYour Move: "+str(moves[0]))

        time.sleep(2)

        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
        )
        # Transfer to conversation state `SECOND`
        return SECOND


    return FIRST


#B person
def Gplay1_end(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()    

    moves=context.chat_data[query.message.chat.id]["moves"]
    print(query.data)

    if query.data=="11":
        moves[1]=1
    elif query.data=="112":
        moves[1]=2
    elif query.data=="113":
        moves[1]=3
    elif query.data=="114":
        moves[1]=4
    elif query.data=="115":
        moves[1]=5
    elif query.data=="116":
        moves[1]=6
    else:
        moves[1]=0

    """Show new choice of buttons"""        
    keyboard = [
        [
            InlineKeyboardButton("Next", callback_data="14"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    users=context.chat_data[query.message.chat.id]["players"]
    
    query.edit_message_text(text="Wait for : "+str(users[1])+" move.", reply_markup=reply_markup)

    return SECOND


#B player
def GRplay1_end(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""

    query = update.callback_query
    query.answer()    

    moves=context.chat_data[query.message.chat.id]["moves"]
    users=context.chat_data[query.message.chat.id]["players"]

    rand_choice = moves[0]

    
    if rand_choice!=moves[1]:

        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="11"),
                InlineKeyboardButton("2", callback_data="112"),
                InlineKeyboardButton("3", callback_data="113"),
                InlineKeyboardButton("4", callback_data="114"),
                InlineKeyboardButton("5", callback_data="115"),
                InlineKeyboardButton("6", callback_data="116"),
            ]

        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if context.chat_data[query.message.chat.id][users[2]][3]==0:
            state="1st Inning\n"
        else:
            state="2nd Inning\n"

        if context.chat_data[query.message.chat.id][users[2]][0]==0:
            msg="You are Bowling Right now\n"
            context.chat_data[query.message.chat.id][users[2]][2]+=1
            msg1="Bowl: "+str(context.chat_data[query.message.chat.id][users[2]][2])
            context.chat_data[query.message.chat.id][users[2]][6]+=rand_choice
            if context.chat_data[query.message.chat.id][users[2]][1]>context.chat_data[query.message.chat.id][users[2]][6]:
                query.edit_message_text(text="You Won! by "+str(context.user_data[update.callback_query.from_user.id][1]-context.user_data[update.callback_query.from_user.id][6]))
                Won=1
                Lost =0
                if str(update.callback_query.from_user.id) in user_data_dict["users"]:
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Played"]+=1
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Won"]+=Won
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Lost"]+=Lost
                    
                    with open("user.json", "w") as outfile:
                        json.dump(user_data_dict, outfile)
                else:
                    new_data={str(update.callback_query.from_user.id):{
                    "Matches":{"Played":1,"Won":Won,"Lost":Lost}}}
                    user_data_dict["users"].update(new_data)

                    with open("user.json", "w") as outfile:
                        json.dump(user_data_dict, outfile)

                return ConversationHandler.END


        else:
            msg="You are Batting Right now\n"
            context.chat_data[query.message.chat.id][users[2]][4]+=moves[1]
            msg1="Your Score: "+str(context.chat_data[query.message.chat.id][users[2]][4])
        
        msg2="\n"
        msg3="Choose Your Move:-"
        msg_markup=state+msg+msg1+msg2+msg3

        query.edit_message_text(text=str(users[1])+" Move:"+str(rand_choice)+"\nYour Move: "+str(moves[1]))
  
        time.sleep(2)

        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
            )

    else:
        """Returns `ConversationHandler.END`, which tells the
        ConversationHandler that the conversation is over.
        """
        Won=0
        Lost=0
        if context.chat_data[query.message.chat.id][users[2]][1]!=0:
            if context.chat_data[query.message.chat.id][users[2]][1]>context.chat_data[query.message.chat.id][users[2]][6]:
                query.edit_message_text(text="You Won! by "+str(context.user_data[update.callback_query.from_user.id][1]-context.user_data[update.callback_query.from_user.id][6]))
                Won=1
            elif context.chat_data[query.message.chat.id][users[2]][1]==context.chat_data[query.message.chat.id][users[2]][6]:
                query.edit_message_text(text="Match Drawn!!")
            else:
                query.edit_message_text(text="You Lose! by "+str(context.chat_data[query.message.chat.id][users[2]][6]-context.chat_data[query.message.chat.id][users[2]][1]))
                Lost=1
        elif context.chat_data[query.message.chat.id][users[2]][5]!=0:
            if context.chat_data[query.message.chat.id][users[2]][4]>context.chat_data[query.message.chat.id][users[2]][5]:
                query.edit_message_text(text="You Won! by "+str(context.chat_data[query.message.chat.id][users[2]][4]-context.chat_data[query.message.chat.id][users[2]][5]))
                Won=1
            elif context.chat_data[query.message.chat.id][users[2]][4]==context.chat_data[query.message.chat.id][users[2]][5]:
                query.edit_message_text(text="Match Drawn!!")
            else:
                query.edit_message_text(text="You Lose! by "+str(context.chat_data[query.message.chat.id][users[2]][5]-context.chat_data[query.message.chat.id][users[2]][4]))
                Lost=1
        else:
            query.edit_message_text(text="See you next time!")
            
        if str(update.callback_query.from_user.id) in user_data_dict["users"]:
            user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Played"]+=1
            user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Won"]+=Won
            user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Lost"]+=Lost

            #print(user_data_dict)        
            with open("user.json", "w") as outfile:
                json.dump(user_data_dict, outfile)
        else:
            # Data to be written
            new_data={str(update.callback_query.from_user.id):{
            "Matches":{
                    "Played":1,
                    "Won":Won,
                    "Lost":Lost
                        }
            }}
         
            user_data_dict["users"].update(new_data)
            #print(user_data_dict)
            # Serializing json 
            #json_object = json.dumps(user_data_dict, indent = 4)
            # Writing to sample.json
            with open("user.json", "w") as outfile:
                json.dump(user_data_dict, outfile)




        return ConversationHandler.END
        

    return SECOND



#A person
def Oplay1_end(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()    

    moves=context.chat_data[query.message.chat.id]["moves"]
    print(query.data)

    if query.data=="11":
        moves[0]=1
    elif query.data=="112":
        moves[0]=2
    elif query.data=="113":
        moves[0]=3
    elif query.data=="114":
        moves[0]=4
    elif query.data=="115":
        moves[0]=5
    elif query.data=="116":
        moves[0]=6
    else:
        moves[0]=0

    """Show new choice of buttons"""        
    keyboard = [
        [
            InlineKeyboardButton("Next", callback_data="14"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    users=context.chat_data[query.message.chat.id]["players"]
    
    query.edit_message_text(text="Wait for : "+str(users[0])+" move.", reply_markup=reply_markup)

    return SECOND



#A Player
def ORplay1_end(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""

    query = update.callback_query
    query.answer()    

    moves=context.chat_data[query.message.chat.id]["moves"]
    users=context.chat_data[query.message.chat.id]["players"]

    rand_choice = moves[1]

    
    if rand_choice!=moves[0]:

        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="11"),
                InlineKeyboardButton("2", callback_data="112"),
                InlineKeyboardButton("3", callback_data="113"),
                InlineKeyboardButton("4", callback_data="114"),
                InlineKeyboardButton("5", callback_data="115"),
                InlineKeyboardButton("6", callback_data="116"),
            ]

        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if context.chat_data[query.message.chat.id][users[3]][3]==0:
            state="1st Inning\n"
        else:
            state="2nd Inning\n"

        if context.chat_data[query.message.chat.id][users[3]][0]==0:
            msg="You are Bowling Right now\n"
            context.chat_data[query.message.chat.id][users[3]][2]+=1
            msg1="Bowl: "+str(context.chat_data[query.message.chat.id][users[3]][2])
            context.chat_data[query.message.chat.id][users[3]][6]+=rand_choice
            
            if context.chat_data[query.message.chat.id][users[3]][1]>context.chat_data[query.message.chat.id][users[3]][6]:
                query.edit_message_text(text="You Won! by "+str(context.chat_data[query.message.chat.id][users[3]][1]-context.chat_data[query.message.chat.id][users[3]][6]))
                Won=1
                Lost=0
                if str(update.callback_query.from_user.id) in user_data_dict["users"]:
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Played"]+=1
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Won"]+=Won
                    user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Lost"]+=Lost

                    with open("user.json", "w") as outfile:
                        json.dump(user_data_dict, outfile)
                else:
                    new_data={str(update.callback_query.from_user.id):{"Matches":{"Played":1,"Won":Won,"Lost":Lost}}}
                    user_data_dict["users"].update(new_data)

                    with open("user.json", "w") as outfile:
                        json.dump(user_data_dict, outfile)

                return ConversationHandler.END


        else:
            msg="You are Batting Right now\n"
            context.chat_data[query.message.chat.id][users[3]][4]+=moves[0]
            msg1="Your Score: "+str(context.chat_data[query.message.chat.id][users[3]][4])
        
        msg2="\n"
        msg3="Choose Your Move:-"
        msg_markup=state+msg+msg1+msg2+msg3

        query.edit_message_text(text=str(users[0])+" Move:"+str(rand_choice)+"\nYour Move: "+str(moves[0]))

        time.sleep(2)

        query.edit_message_text(
            text=msg_markup, reply_markup=reply_markup
            )

    else:
        """Returns `ConversationHandler.END`, which tells the
        ConversationHandler that the conversation is over.
        """
        Won=0
        Lost=0
        if context.chat_data[query.message.chat.id][users[3]][1]!=0:
            if context.chat_data[query.message.chat.id][users[3]][1]>context.chat_data[query.message.chat.id][users[3]][6]:
                query.edit_message_text(text="You Won! by "+str(context.chat_data[query.message.chat.id][users[3]][1]-context.chat_data[query.message.chat.id][users[3]][6]))
                Won=1
            elif context.chat_data[query.message.chat.id][users[3]][1]==context.chat_data[query.message.chat.id][users[3]][6]:
                query.edit_message_text(text="Match Drawn!!")
            else:
                query.edit_message_text(text="You Lose! by "+str(context.chat_data[query.message.chat.id][users[3]][6]-context.chat_data[query.message.chat.id][users[3]][1]))
                Lost=1
        elif context.chat_data[query.message.chat.id][users[3]][5]!=0:
            if context.chat_data[query.message.chat.id][users[3]][4]>context.chat_data[query.message.chat.id][users[3]][5]:
                query.edit_message_text(text="You Won! by "+str(context.chat_data[query.message.chat.id][users[3]][4]-context.chat_data[query.message.chat.id][users[3]][5]))
                Won=1
            elif context.chat_data[query.message.chat.id][users[3]][4]==context.chat_data[query.message.chat.id][users[3]][5]:
                query.edit_message_text(text="Match Drawn!!")
            else:
                query.edit_message_text(text="You Lose! by "+str(context.chat_data[query.message.chat.id][users[3]][5]-context.chat_data[query.message.chat.id][users[3]][4]))
                Lost=1
        else:
            query.edit_message_text(text="See you next time!")
            
        if str(update.callback_query.from_user.id) in user_data_dict["users"]:
            user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Played"]+=1
            user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Won"]+=Won
            user_data_dict["users"][str(update.callback_query.from_user.id)]["Matches"]["Lost"]+=Lost

            #print(user_data_dict)        
            with open("user.json", "w") as outfile:
                json.dump(user_data_dict, outfile)
        else:
            # Data to be written
            new_data={str(update.callback_query.from_user.id):{
            "Matches":{
                    "Played":1,
                    "Won":Won,
                    "Lost":Lost
                        }
            }}
         
            user_data_dict["users"].update(new_data)
            #print(user_data_dict)
            # Serializing json 
            #json_object = json.dumps(user_data_dict, indent = 4)
            # Writing to sample.json
            with open("user.json", "w") as outfile:
                json.dump(user_data_dict, outfile)




        return ConversationHandler.END
        

    return SECOND


###############_____END_____GROUP_____PLAY______################################ 

def main() -> None:
    #start handler

    start_handler=CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('playwithbot', playwithbot)],
        states={
            FIRST: [
                CallbackQueryHandler(normal, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(normal, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(heads, pattern='^' + str(FOUR) + '$'),
                CallbackQueryHandler(tails, pattern='^' + str(FIVE) + '$'),
                CallbackQueryHandler(play, pattern='^' + str(SIX) + '$'),
                CallbackQueryHandler(batting, pattern='^' + str(SEVEN) + '$'),
                CallbackQueryHandler(bowling, pattern='^' + str(EIGHT) + '$'),
                CallbackQueryHandler(playbatting, pattern='^' + str(NINE) + '$'),
                CallbackQueryHandler(playbowling, pattern='^' + str(TEN) + '$'),
                CallbackQueryHandler(play1, pattern='^' + "11" + '$'),
                CallbackQueryHandler(play1, pattern='^' + "12" + '$'),
                CallbackQueryHandler(play1, pattern='^' + "13" + '$'),
                CallbackQueryHandler(play1, pattern='^' + "14" + '$'),
                CallbackQueryHandler(play1, pattern='^' + "15" + '$'),
                CallbackQueryHandler(play1, pattern='^' + "16" + '$'),

            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(play1_end, pattern='^' + "11" + '$'),
                CallbackQueryHandler(play1_end, pattern='^' + "12" + '$'),
                CallbackQueryHandler(play1_end, pattern='^' + "13" + '$'),
                CallbackQueryHandler(play1_end, pattern='^' + "14" + '$'),
                CallbackQueryHandler(play1_end, pattern='^' + "15" + '$'),
                CallbackQueryHandler(play1_end, pattern='^' + "16" + '$'),

            ],
        },
        fallbacks=[CommandHandler('playwithbot', playwithbot)],
    )

    #A person
    grp_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.chat_type.group & Filters.command & Filters.regex('/challenge'), challenge_group)],
        states={
            FIRST: [
                CallbackQueryHandler(ok_group, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(cancel_group, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(Oheads, pattern='^' + str(FOUR) + '$'),
                CallbackQueryHandler(ORheads, pattern='^' + "12" + '$'),
                CallbackQueryHandler(Otails, pattern='^' + str(FIVE) + '$'),
                CallbackQueryHandler(ORtails, pattern='^' + '13' + '$'),
                CallbackQueryHandler(preplay, pattern='^' + "preplay" + '$'),
                CallbackQueryHandler(Oplay, pattern='^' + str(SIX) + '$'),
                CallbackQueryHandler(Obatting, pattern='^' + str(SEVEN) + '$'),
                CallbackQueryHandler(Obowling, pattern='^' + str(EIGHT) + '$'),
                CallbackQueryHandler(Gplaybatting, pattern='^' + str(NINE) + '$'),
                CallbackQueryHandler(Gplaybowling, pattern='^' + str(TEN) + '$'),
                CallbackQueryHandler(Oplay1, pattern='^' + "11" + '$'),
                CallbackQueryHandler(Oplay1, pattern='^' + "112" + '$'),
                CallbackQueryHandler(Oplay1, pattern='^' + "113" + '$'),
                CallbackQueryHandler(Oplay1, pattern='^' + "114" + '$'),
                CallbackQueryHandler(Oplay1, pattern='^' + "115" + '$'),
                CallbackQueryHandler(Oplay1, pattern='^' + "116" + '$'),
                CallbackQueryHandler(ORplay1, pattern='^' + "14" + '$'),

            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(Oplay1_end, pattern='^' + "11" + '$'),
                CallbackQueryHandler(Oplay1_end, pattern='^' + "112" + '$'),
                CallbackQueryHandler(Oplay1_end, pattern='^' + "113" + '$'),
                CallbackQueryHandler(Oplay1_end, pattern='^' + "114" + '$'),
                CallbackQueryHandler(Oplay1_end, pattern='^' + "115" + '$'),
                CallbackQueryHandler(Oplay1_end, pattern='^' + "116" + '$'),
                CallbackQueryHandler(ORplay1_end, pattern='^' + "14" + '$'),
            ],
        },
        fallbacks=[MessageHandler(Filters.chat_type.group & Filters.command & Filters.regex('/challenge'), challenge_group)],
    )

    #B person
    start_ch = ConversationHandler(
        entry_points=[MessageHandler(Filters.reply & Filters.regex('/accept'), challenge_start)],
        states={
          FIRST: [
                CallbackQueryHandler(toss, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(cancel_group, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(Gheads, pattern='^' + str(FOUR) + '$'),
                CallbackQueryHandler(GRheads, pattern='^' + '12' + '$'),
                CallbackQueryHandler(Gtails, pattern='^' + str(FIVE) + '$'),
                CallbackQueryHandler(GRtails, pattern='^' + '13' + '$'),
                CallbackQueryHandler(preplay, pattern='^' + "preplay" + '$'),
                CallbackQueryHandler(Gplay, pattern='^' + str(SIX) + '$'),
                CallbackQueryHandler(Gbatting, pattern='^' + str(SEVEN) + '$'),
                CallbackQueryHandler(Gbowling, pattern='^' + str(EIGHT) + '$'),
                CallbackQueryHandler(Gplaybatting, pattern='^' + str(NINE) + '$'),
                CallbackQueryHandler(Gplaybowling, pattern='^' + str(TEN) + '$'),
                CallbackQueryHandler(Gplay1, pattern='^' + "11" + '$'),
                CallbackQueryHandler(Gplay1, pattern='^' + "112" + '$'),
                CallbackQueryHandler(Gplay1, pattern='^' + "113" + '$'),
                CallbackQueryHandler(Gplay1, pattern='^' + "114" + '$'),
                CallbackQueryHandler(Gplay1, pattern='^' + "115" + '$'),
                CallbackQueryHandler(Gplay1, pattern='^' + "116" + '$'),
                CallbackQueryHandler(GRplay1, pattern='^' + "14" + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(Gplay1_end, pattern='^' + "11" + '$'),
                CallbackQueryHandler(Gplay1_end, pattern='^' + "112" + '$'),
                CallbackQueryHandler(Gplay1_end, pattern='^' + "113" + '$'),
                CallbackQueryHandler(Gplay1_end, pattern='^' + "114" + '$'),
                CallbackQueryHandler(Gplay1_end, pattern='^' + "115" + '$'),
                CallbackQueryHandler(Gplay1_end, pattern='^' + "116" + '$'),
                CallbackQueryHandler(GRplay1_end, pattern='^' + "14" + '$'),
            ],
          },
        fallbacks=[MessageHandler(Filters.reply & Filters.regex('/accept'), challenge_start)],
    )
    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(grp_conv_handler)
    #start_ch=MessageHandler(Filters.reply & Filters.regex('/accept'), challenge_start)
    dispatcher.add_handler(start_ch)

    #playwithbot command
    playbot = CommandHandler('playwithbot', playwithbot)
    dispatcher.add_handler(playbot)

    #mystats command
    stats = CommandHandler('mystats', mystats)
    dispatcher.add_handler(stats)

    #challenge command

    #challenge_M=MessageHandler(Filters.chat_type.group & Filters.command & Filters.regex('/challenge'), challenge_group)
#    dispatcher.add_handler(challenge_M)

    challenge_ = CommandHandler('challenge', challenge)
    dispatcher.add_handler(challenge_)


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()