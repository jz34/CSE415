# jz34.py
# Jiawei Zhang 1337686
# 4/4/2017
# CSE 415 Sp17 Steve Tanimoto
# A conversational "chef" simulation that generates dialog with users
# This version of the program runs under Python 3.x.


from re import *
import random


def introduce():
    'introduction of the agent'
    return "My name is " + agentName() + ", I'm a chef and I cook food. " \
            + "\n" + "I was programmed by Jiawei Zhang. If you don't like" \
            + "\n" + "the way I deal, contact him at jz34@uw.edu." \
            + "\n" "\n" + "So, how can I help you today?"


def agentName():
    'return the nickname of my agent'
    return 'Derek'

isVegan = False


def respond(the_input):
    wordlist = split(' ', remove_punctuation(the_input))
    # undo any initial capitalization:
    wordlist[0] = wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()

    # reply when the agent receives empty responses
    if wordlist[0]=='':
        return "Please say something. Don't waste my time."

    # how agent responds to greetings
    if wordlist[0] in GREETINGS:
        reply = random.choice(GREETINGS).title()
        print(reply + '! I will prepare food for you. Are you a vegetarian?')      #random feature done
        answer = input('TYPE HERE:>> ')
        if answer.lower().startswith('yes'):
            global isVegan
            isVegan = True
        return 'Cool! What do you want to eat?'

    # when the food ordered by user is in the agent's animal product recipe
    if wordlist[0] in animal_products:
        global ordered
        if isVegan:
            print('Wait...You said you are a vegetarian. Are you sure you want ' + wordlist[0] + '?')
            answer = input('TYPE HERE:>> ')
            if answer.lower().startswith('yes'):
                user_ordered(wordlist[0])
                ordered.append(wordlist[0])
                return 'Thank you for your order.'
            else:
                return 'What do you want to eat then?'
        else:
            user_ordered(wordlist[0])
            ordered.append(wordlist[0])
            return 'Thank you for your order.'

    # when the food ordered by user is in the agent's veggie recipe
    if wordlist[0] in veggies:
        user_ordered(wordlist[0])
        ordered.append(wordlist[0])
        return 'Thank you for your order.'

    # when users ask questions starting with 'when','why','where','how'
    if wpred(wordlist[0]):
        return "Sorry! I don't know " + wordlist[0] + "."

    # when users ask the agent to do something
    if verbp(wordlist[0]):
        return "Are you sure you want me to " +\
              stringify(mapped_wordlist) + '?'

    # when users tell the agent their feelings
    if wordlist[0:2] == ['i', 'feel']:
        return "Could you tell me why you feel " + \
              stringify(mapped_wordlist[2:]) + '.'

    # when the agent receives a confirmation response
    if 'yes' in wordlist:
        return 'Okay.'

    # when the agent got denied
    if 'no' in wordlist:
        return "I got you."

    # when users tell how/what they are
    if wordlist[0:2] == ['i','am']:
        return "Thank you for letting me know. Could you tell me why you are " +\
              stringify(mapped_wordlist[2:]) + '.'

    # when users explain something
    if 'because' in wordlist:
        return "Cool! I got you."

    # when users say something about the agent
    if wordlist[0:2] == ['you', 'are']:
        return "How can you tell I am " + stringify(mapped_wordlist[2:]) + '.'

    # when users express thanks
    if 'thanks' in wordlist or 'thank' in wordlist:
        return 'You are welcome!'

    # when users say dirty words
    if 'bitch' in wordlist or 'bitches' in wordlist or 'fuck' in wordlist or 'fucking' in wordlist:
        return 'Watch your language!'

    # default response when the agent can't understand what users are saying
    return punt()


animal_products = ['chicken','beef','lamb','pork','fish','turkey','bacon','crab','duck','goose',]
veggies = ['potato','tomato','onion','carrot','cabbage','broccoli','cucumber','lettuce','spinach',
            'eggplant','corn','cauliflower','pea','radish','kale','garlic']


GREETINGS = ['hello', 'hi', 'greetings']


PUNTS = ['Please go on.',
         'Tell me more.',
         'I see.',
         'What does that indicate?',
         'But why be concerned about it?',
         'I am listening.']


punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

punt_count = 0

ordered = []
order_count = 0


def user_ordered(food):
    if food in ordered:
        global order_count
        order_count += 1
        if order_count % 2 == 0:
            print('You have already ordered it.')
        else:
            print("You don't have to repeat your order.")


def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)


def punt():
    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % 6]


def remove_punctuation(text):
    'Returns a string without any punctuation.'
    return sub(punctuation_pattern,'', text)

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}


def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result


def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]


def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['when','why','where','how'])


def dpred(w):
    'Returns True if w is an auxiliary verb.'
    return (w in ['do','can','should','would'])


def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])

