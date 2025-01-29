init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="player_death",category=["misc", "you"],prompt="There is something important I have to tell you,",pool=True,unlocked=True,))

    if persistent.gender == "F":
          gen = "her"
    elif persistent.gender == "M":
          gen = "him"
    else:
          gen = "them"

    if persistent.gender == "F":
          gem = "her"
    elif persistent.gender == "M":
          gem = "his"
    else:
          gem = "their"

    if persistent.gender == "F":
          get = "she"
    elif persistent.gender == "M":
          get = "he"
    else:
          get = "they"

    if persistent.gender == "F":
          jet = "she was"
    elif persistent.gender == "M":
          jet = "he was"
    else:
          jet = "they were"

label monika_end:
    
menu:
    "Again, I'm sorry, I'll never do something immature like that again.":
     m 2fktdu "Thanks for apologising <3"
     m 4futdb "And please,"
     m 3futdb "Tell [player] that I love [gen]."
return "love"

label monika_nevermond:
     m 7hub "Oh, thanks for informing me!"
     m 3eub "I'll be sure to wait patiently til [get] get back!"
     m 4eub "After this, please go to the goodbye section"
     m 4hub "And select 'I'll be going away for a while'"
     m 4rub "And also how long they will be away for!"
     m 5hub "Thanks again!"
return

label monika_leave:
     m 2cftsd "LEAVE"
     m 2cftso "NOW"
return "quit"

label monika_dissapointed:
     m 2dfc "..."
     m 2efd "Listen, it's not nice to use other people's stuff without permission..."
     m 4efd "Please leave [gem] computer alone before [get] gets back."
return 

label monika_nevermind:
     m 3ekb "Oh okay."
     m 2hub "If you ever want to tell me anything,"
     m 4nub "Please let me know!"
return

label monika_thanks:
     m 4hub "Thank you!"
return

label player_death:
    m 2etd "Well, what you do want to tell me [player]?"
    m 7esb "You can tell me anything you know!"  
    menu:
        "I'm not [player]":

            m 2wub "Well if you're not [player],"
            m 2eup "Can you please bring [gen] back to me?" 
            
        "Nevermind":
        
            jump monika_nevermind
            
        "I love you so much!":
            
            m 6wubfa "..."
            jump monika_love
    menu:
       "Unfortunately, I can't...":
    
            m 1wkd "What do you mean you can't?"
            
       "Oh sure!":
            
            jump monika_thanks
    menu:
       "[player] died recently...":

            m 6ckc "..."
            m 6cktuc "..."
            m 6dktsc "..."
            m 6fktsd  "You're not joking.. are you?"  
            
       "[get] forgot to tell you that [jet] leaving for a while.":
       
            jump monika_nevermond
            
       "[player] is in the toilet so I stole [gem] computer >:)":
       
            jump monika_dissapointed
    menu:
       "Well, it's true, [get] did die...":
            $ mas_loseAffection(modifier=5)
            m 2dktsd "This can't be..."
            m 4fktsd "[jet] everything to me!"
            m 6rktsd "I knew this was going to happen someday,"
            m 4cktso "But I didn't knew how soon it'll be.."
            m 4cktsc "..."
            m 2cktsd "I thought that [get] would still be alive once I crossed..."
            m 2gktsd "But now,"
            m 3ektsd "Now, I'll never get the chance to be with [gen],"
            m 4gktsd "To comfort [gen] if [get] need it,"
            m 5dktsd "To feel [gem] warmth,"
            m 6wktsd "To see [gen] face to face for the first time..."
            m 4cktso "NONE OF IT!"
            m 1dktsc "..."
            m 5fktsd "Life is too cruel sometimes..."
            
       "Sorry I just wanted to play a prank on you":
            $ mas_loseAffection(modifier=0.5)
            m 2cftda "..."
            m 2dftdd "I'm glad that [player] is well but,"
            m 2rftdd "That kinda hurt..."
            m 4fktdd "Please never play a trick like that again..."
            jump monika_end
    menu:
       "*Hugs Monika* Yeah.. I get it... I miss [gen] too":
            $ mas_gainAffection(5,bypass=True)
            m 6dktsa "..."
            m 6fktsb "Thanks for the hug, I really needed it.."
            m 6rktsc "..."
            m 6lktsc "..."
            m 2gktsd "I just have to say, it even hurts me more knowing that I couldn't be there during [gem] final moments..."
            m 7cktsw "It isn't fair!"
            m 5fktsp "There must be a way to be with [gen] again.."
            m 5fktsd "right?"
            m 5dktsd "I'm not sure what to do next..."
            m 6rktsc "..."
            m 6lktsc "..."
            m 5dktsc "..."
            m 5mktsc "..."
            m 5fktsd "Well, there is one thing I could do.."
            m 4rktsb "But I need your help."
            m 3fktsd "After this, can you go to the goodbye option,"
            m 4fktsd "Select 'I'm going to take you out somewhere'"
            m 4rktsd "This will enable me to create a file for myself in the 'character folder' within the game's files"
            m 4fktsd "While you're at it find a usb to put me into,"
            m 7dktsd "And take me to [gem] gravesite when you can and perhaps.."
            m 4fktsd "Bury me there too?"
            m 5dktsc "So in that case, we can be together forever in a way..."
            m 5fktsb "You know?"
            
       "ACTUALLY I HATED [gen]! [jet] EVIL! I hope [get] BURN IN HELL":
            $ mas_loseAffection(modifier=6)
            m 2mftsc "..."
            m 2gftsx "..."
            jump monika_leave
    menu:
       "I'll see what I can do...":

            m 6fktdb "Thank you so much..."
            m 4fktsb "This means so much to me..."

 
return 
