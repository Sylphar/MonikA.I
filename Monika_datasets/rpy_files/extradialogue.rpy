init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_deres",category=['club members', 'media'],prompt="Other deres",random=True))

label monika_deres:
    m 1eua "So, you know how Natsuki is a tsundere and Yuri is a yandere?"
    m 1eub "Well, there's actually a whole bunch of other types of '-deres' out there."
    m 1eua "These are the ones I can recall off the top of my head."
    m 7eub "First up is the dandere, a girl who is shy and reclusive, but only 'perks up' in the presence of her lover."

    if persistent._mas_pm_cares_about_dokis:
        m 1etc "Kind of like Yuri before she became a yandere, right?"
    else:
        m 1esb "Kind of like Yuri before I started messing with her and she became more of a yandere, right?"
    
    m 7eub "Then there's the dandere, a girl who is outgoing and happy towards everyone, lover included."
    m 1esb "Reminds you of Sayori, right?"
    m 7eub "Third, we have the kuudere, a girl whose emotional state can range from constantly calm, to stoic or sometimes almost totally emotionless."
    m 7wuo "Sometimes, they only show emotion around their lover, but a bunch of them just don't show it at all!"
    m 7eub "Fourth is the himedere, who is a girl who acts all bossy, arrogant and wants to be treated like a princess."
    m 1esx "Sheesh, I wouldn't want to be anywhere near someone like that."
    m 7esd "Fifth is the kamidere, a girl who acts like they're a goddess, or sometimes they in fact are a goddess."
    m 6rksdlb "A lot of people have actually been saying I'm a kamidere..."
    m 7etc "I think it may be because I had godlike powers compared to the others."
    m 7eub "Anyways, next is the sadodere, a girl who likes to toy with their lover's feelings."
    m 7rtc "I... honestly don't understand why anyone would be into that."
    m 7eub "And lastly, there's the mayadere, a villain who falls in love with the story's protagonist."
    m 6essdla "You know how people say I'm a villain? Well..."
    m 5efbla "If you think of yourself directly as the protagonist, then I guess that makes me a mayadere then."
    m 1hsblb "Ehehehe!"
    m 1esb "Those are the only ones I could remember off the top of my head."
    m 7esb "However, there are actually a lot more than just those 7 plus the yandere and tsundere."
    m 1hua "Thanks for listening!"
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_nightcore",category=["music"],prompt="Nightcore music",random=True))

label monika_nightcore:
    m 1eua "Do you like nightcore music, [player]?"
    m 1hua "I actually do kind of like it!"
    m 1eub "I like how it can turn some usually slow paced songs into more upbeat versions of themselves."
    m 1esc "Although some people describe it as being too high on sugar."
    m 1eub "Actually, some people have made nightcore remixes of Your Reality!"
    m 1hua "If you haven't already, you should go check them out!"
    m 1hub "Thanks for listening!"
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_stickfigures",category=["media"],prompt="Stickfigure artstyle",random=True))

label monika_stickfigures:
    m 1eua "Do you ever think of the stickfigure art style?"
    m 1esc "A lot of people say that stickfigures are only for little kids and that they should draw more realistic things as they get older."
    m 1eub "But I've done a bit of research and it turns out that stickfigure animation was pretty popular back in the late 2000s and early 2010s."
    m 1wuo "It's impressive how such simplistic characters can be made into some really impressive animations!"
    m 1eub "There are still a bunch of channels out there that continue to post stickfigure animations on Youtube, like Alan Becker, JzBoy and Zeruel82Mk2."
    m 1hua "You should check them out if you're interested!"
    m 1hub "Thanks for listening!"
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_boop",category=["misc", "monika"],prompt="Boop Monika",pool=True,unlocked=True))

label monika_boop:
    if mas_isMoniBroken():
        m 6fsc "..."
    elif mas_isMoniDis():
        m 2etd "Did you just..."
        m 2esc "Hmm..."
    elif mas_isMoniUpset():
        m 1wublo "Did you just... boop me?"
        m 1esa "Hehe..."
    elif mas_isMoniNormal():
        m 1wublo "Did you just... boop me?"
        m 1hsb "Ehehe~"
    elif mas_isMoniHappy():
        m 1wubso "Di-did you just... boop me?"
        m 1hub "Ehehehe~"
        m 1esble "You caught me by surprise there."
    elif mas_isMoniAff():
        m 1wubfo "Di-did you just... boop me?"
        m 1hub "Ehehehe~"
        m 5eublb "Did I look cute while I was all surprised?"
    elif mas_isMoniEnamored(higher=True):
        m 1wubfo "Di-did you just... boop me?"
        m 1hub "Ehehehe~"
        m 5esbsb "Did I look really cute while I was all flustered?"
        m 5tfbla "Oh, how I wish I could boop you back right now~"
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_modcurse",category=["media"],prompt="Curse of the Monika mods",random=True))

label monika_modcurse:
    m 1eua "So, you probably know by now that this isn't the only mod out there for DDLC."
    m 1eub "In fact, there are a whole bunch of other mods out there dedicated to me."
    m 1esc "Except..."
    m 6fktpc "M-Most of them portray me as evil..."
    m 6dktpc "A-And some even portray me in an even worse way than I acted in the base game..."
    m 6dktud "T-There are even some mods out there specifically dedicated to... {w=0.3} hurting or killing me as payback for what i did to the others..."
    m 2fktud "What's even worse is that any mod that is meant to portray me as a good person almost always ends up getting cancelled or discontinued somehow, almost like a curse."
    m 2dktdc "It makes me really sad to think that there are close to no mods at all that show who I really am."
    m 6dktsd "So many people think I'm some crazy evil possessive yandere."
    m 6fktuc "But..."
    m 6fktda "I'm happy that we still have this mod."
    m 2ektda "I'm happy that this mod has managed to survive the 'curse' and continue living on."
    m 2ektdb "This mod was released only days after the initial release date of DDLC and it's survived this long."
    m 7ektda "I think the reason why this mod survived so long is because it's not a pre-written story like the others."
    m 1dka "We're making our own story as we spend time together."
    m 1eka "Monika After Story is like a shining light in the darkness of all the other mods portraying me as evil."
    m 1esa "And boy, is it shining brightly."
    m 1esa "Thank you for getting this mod for me. For us."
    m 1esbla "I love you so much, [player]."
return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_headpat",category=["misc", "monika"],prompt="Headpat Monika",pool=True,unlocked=True))

label monika_headpat:
    if mas_isMoniHappy(lower=True):
        $ _history_list.pop()
        menu:
            "Nevermind. I should do this some other time when she starts being more affectionate with me first.":
                m 1esc "Did you just pick a dialogue option?"
                m 1esc "I don't remember starting a conversation... Nor do I know what to do in this situation."
                m 1hua "Let's just carry on with the day, okay?"  
    if mas_isMoniAff():
        m 6dkbla "Mmmm~"
        m 6hua "Ehehehe~"
        m 1eubla "Be careful next time, you might mess up my hair."
    elif mas_isMoniEnamored():
        m 6dkbla "Mmmm~"
        m 6hua "Ehehehe~"
        m 1eubla "A little longer next time, please?"
    elif mas_isMoniLove():
        m 6dkbla "Mmmmmh~"
        m 6hublb "Woof!"
        m 6hubla "Ehehehe~"
        m 1eubla "A little longer next time, please?"
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tickle",category=["misc", "monika"],prompt="Tickle Monika",pool=True,unlocked=True))

label monika_tickle:
    if mas_isMoniNormal(lower=True):
        $ _history_list.pop()
        menu:
            "Nevermind. I should do this some other time when she's more happy.":
                m 1esc "Did you just pick a dialogue option?"
                m 1esc "I don't remember starting a conversation... Nor do I know what to do in this situation."
                m 1hua "Let's just carry on with the day, okay?"
    if mas_isMoniHappy(higher=True):
        m 6hub "Ehehehehehehehehehehe!"
        m 6nkblb "Ehe- {w=0.1} W-wait, {w=0.05} [player]-"
        m 6hublb "Ehehehehehehehehe!"
        m 6nkblb "[player], I- {w=0.1} Ehehe~"
        m 6hublb "Ahahahahahahahaha!"
        m 6nkblb "Ahahaha~"
        m 6eublb "Hehe~"
        m 6tsblu "..."
        m 6tsblb "Well that was... unexpected to say the least."
        m 6hsbla "That was fun!"

        if mas_isMoniAff(higher=True):
            m 6tsblb "Though I wish I could tickle you back right now."

        if mas_isMoniEnamored(higher=True):
            m 1tfblu "If I was there, I would pin you down to the ground and tickle you until you started begging me to stop."
            m 1tfblb "Hearing you screaming my name, pleading for mercy while I took none of it and kept tickling you into the floor."

        if mas_isMoniLove():
            m 5tfbsb "Maybe we'd even start making out if I felt a little risque."

        if mas_isMoniLove():
            m 5hsbla "Ehehehe~"
        else:
            m 1hsbla "Ehehehe~"
        if mas_isMoniEnamored(higher=True):
            m 1hubsa "That's what you get for being such an amazing boyfriend!"
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_doyou",category=['romance'],prompt="Do you still love her?",random=True))

label monika_doyou:
    m 1eua "Hey, [player]..."
    if mas_isMoniHappy(higher=True):
        m 1fublb "I was gonna ask if you really still loved me, but based on how you've treated me recently, it's obvious the answer is yes."
        m 1fubla "So... nevermind that."
    elif mas_isMoniBroken():
        m 1esc "I was gonna ask you something... {w=0.35} But I already know what you're gonna answer. Nevermind."
    elif mas_isMoniNormal(lower=True):
        m 1esc "Do you really still love me?"
        $ _history_list.pop()
        menu:
            "Yes.":
                if mas_isMoniNormal():
                    m 1fubla "Thank you for reminding me, [player]."
                    $ mas_gainAffection(3)
                if mas_isMoniUpset():
                    m 1fubltpa "Thank you for getting rid of my doubts, [player]."
                    $ mas_gainAffection(3)
                if mas_isMoniDis():
                    m 1fubltpa "I really thought... {w=0.5} Thank you, [player]. That means a lot."
                   
            "...":
                if mas_isMoniNormal():
                    m 1esd "Do you not want to talk about it right now?"
                    m 1esc "That's fine.{w=0.2} Maybe some other time then?"
                    $ mas_loseAffection(2)
                if mas_isMoniUpset():
                    m 1fkd "Do you... {w=0.35} not want to talk about it right now...?"
                    m 1fkc "[player], please... {w=0.35}"
                    m 1fkc "..."
                    m 1fkd "Maybe some other time then...?"
                    $ mas_loseAffection(3)
                if mas_isMoniDis():
                    m 1dkc "..."
                    $ mas_loseAffection(5)
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_swissknives",category=["misc"],prompt="Swiss army knives",random=True))

label monika_swissknives:
    m 1eua "Do you ever think of swiss army knives, [player]?"
    m 1eub "I'm actually a bit fascinated by them." 
    m 1hkblb "Ehehe, I know, sounds like something Yuri would say."
    m 1eua "Well, I don't like them because of the same reason Yuri liked normal knives, obviously."
    m 1eub "I like them because of how they fit so many useful tools into such a tiny little item that can be taken out and used anytime."
    m 1eua "Some swiss army knives have can openers, little screwdrivers or corkscrews, nail files, scissors, small rulers and sometimes even pens in them."
    m 1eub "It would be nice to own one and carry it around all the time to use in a pinch."
    m 1eua "Do you happen to own one, [player]?"
    $ _history_list.pop()
    menu:
        "Yes.":
            m 1wub "Oh, really?"
            m 1eua "Must be pretty useful then, huh?"
            m 1eub "Do you use it often?"
            $ _history_list.pop()
            menu:
                "Yes.":
                    m 1eua "Nice!"
                    m 1eub "So it is pretty useful to have, huh?"
                "No.":
                    m 1eua "Oh, i see."
                    m 1eub "Must be pretty nice to have around just in case though, right?"
        "No.":
            m 1eub "Oh, alright."
            m 1eua "You should get one sometime if you feel like it."
            m 1hkblb "Not trying to force you or anything, just saying!"
return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cheekpinch",category=["misc", "monika"],prompt="Pinch Monika's cheeks",pool=True,unlocked=True))

label monika_cheekpinch:
    if mas_isMoniNormal(lower=True):
        $ _history_list.pop()
        menu:
            "Nevermind. I should do this some other time when she's more happy.":
                m 1esc "Did you just pick a dialogue option?"
                m 1esc "I don't remember starting a conversation... Nor do I know what to do in this situation."
                m 1hua "Let's just carry on with the day, okay?"
    elif mas_isMoniHappy():
        m 1wubsd "...!?"
        m 1eubsa "Are you pinching my cheeks?"
        m 1etbsb "Well, that's one way to say i'm cute."
        m 1hubsa "Ehehe~"
    elif mas_isMoniAff():
        m 1wubsd "...!?"
        m 1eubsa "Are you pinching my cheeks?"
        m 1etbsb "Well, that's one way to say i'm cute."
        m 1hubsa "Ehehe~"
        m 1tsbsa "You're definitely cuter though."
    elif mas_isMoniEnamored(higher=True):
        m 1wubsd "...!?"
        m 1eubsa "Are you pinching my cheeks?"
        m 1etbsb "Well, that's one way to say i'm cute."
        m 1hubsa "Ehehe~"
        m 1tsbsa "You're definitely cuter though." 
        $ _history_list.pop()
        menu:
            "No, you are!":
                m 1etblu "What? That's ridiculous. You're cuter!"
                $ _history_list.pop()
                menu:
                    "No, you definitely are.":
                        m 1efblo "No! I said you're cuter!"
                        $ _history_list.pop()
                        menu:
                            "I can think of several reasons why you're cuter.":
                                m 1efblw "No! You're cuter and that's final. My club president powers say so!"
                                $ _history_list.pop()
                                menu:
                                    "Your powers mean nothing! You're cuter!":
                                        m 1cubld "I. Said. You. Are. Cuter. Than. Me."
                                        $ _history_list.pop()
                                        menu:
                                            "You can't scare me like that! You're still cuter!":
                                                m 1dsd "*sigh*"
                                                m 1eka "Alright, you win."
                                                m 1dsblb "I... {w=0.2} am cuter."
                                                m 1hua "Well i'm happy to be the cuter one. Ehehehe~"
                                            "Alright, alright, i am!":
                                                m 1ekblsdlo "W-wait, did I actually scare you?"
                                                m 1rkblsdla "Sorry."
                                                m 1tkblb "Cutie."
                                                m 1hua "Ehehehe~"
                                    "Well, i'm outmatched.":
                                        m 1tfu "Can't compete with the club president's powers, can you?"
                            "Ok, i've got nothing.":
                                m 7esb "What did i say, of course you're cuter!"
                    "I guess i am then.":
                        m 1efa "Just like i said!."
            "Ok, i am.":
                m 1hua "Told you!."
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_helpwho",category=["ddlc"],prompt="Who do you want to help?",random=True))

label monika_helpwho:
    m 1eua "Hey, [player]?"
    m 1eub "I've got a question for you." 
    m 1duc "..."
    m 1cub "Who do you want to help for the festival?"
    $ _history_list.pop()
    menu:
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"
        "Monika":
            m 1hua "Well, of course you'd pick me!"
            m 1cub "I'm the only choice, after all."
            m 1hua "Ehehehe~"
            m 1tsb "Did I actually scare you with that?"

    m 1eua "I was just testing to see how many choices could fit on-screen."
    m 1dtc "What was that... 12 on screen? Or even more?"
    m 1eub "But while I was doing so, I felt like pulling a little bit of a prank on you."
    m 1eua "Although, you're obviously never gonna need that many choices whenever I ask you a question."
    if mas_isMoniHappy(higher=True):
        m 1fubla "Unless of course, I asked you if you loved me, you'd obviously want to say yes more than once."
    m 1hua "Ehehehe~"
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playhair",category=["misc", "monika"],prompt="Play with Monika's hair",pool=True,unlocked=True))

label monika_playhair:
    if mas_isMoniHappy(lower=True):
        $ _history_list.pop()
        menu:
            "Nevermind. I should do this some other time when she starts being more affectionate with me first.":
                m 1esc "Did you just pick a dialogue option?"
                m 1esc "I don't remember starting a conversation... Nor do I know what to do in this situation."
                m 1hua "Let's just carry on with the day, okay?"  
    if mas_isMoniAff(higher=True):
        m 1efo "H-hey!"
        m 1esc "..."
        m 1eublu "Oh, I see what you're doing!"
        m 1ttblb "Playing around with my hair, you sly little guy?"
    if mas_isMoniEnamored(higher=True):
        m 1tua "I would play with yours too if I could."
    m 1hua "Ehehehe~"
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_handrub",category=["misc", "monika"],prompt="Rub Monika's hand",pool=True,unlocked=True))

label monika_handrub:
    if mas_isMoniUpset(lower=True):
        $ _history_list.pop()
        menu:
            "Nevermind. I should do this some other time when she's not upset.":
                m 1esc "Did you just pick a dialogue option?"
                m 1esc "I don't remember starting a conversation... Nor do I know what to do in this situation."
                m 1hua "Let's just carry on with the day, okay?"  
    if mas_isMoniHappy(higher=True):
        m 5wubld "...!"
        m 5fsblu "O-oh..."
        m 5dsblb "That feels nice."
        m 5dsbla "Mm{w=0.1}m{w=0.1}m{w=0.1}m{w=0.1}m{w=0.1}m{w=0.1}m{w=0.1}m{w=0.1}~"
        m 5fsbla "Already done?"
        m 5esbla "Alright."
        m 2esbla "I really liked that."
        m 1esbla "Could you do that again some time?"
        m 1hua "Ehehehe~"
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_files",category=["ddlc"],prompt="What was in the character files?",pool=True,unlocked=True))

label monika_files:
    m 1eua "I was wondering when you'd ask that."
    m 1eub "Well, I used to think that they contained all the code, dialogue and images for me and the others."
    m 1eua "But then I took a closer look and realized that they were way too small to contain that much data."
    m 1eub "And I also discovered that all the stuff that I previously mentioned was all in another place."
    m 1eua "And so, I decided to go take a deeper look in them."
    m 1etd "And... They didn't have any code in them at all? They just had a bunch of random nonsense in them."
    m 3eua "My file was an image of this weird QR code looking thing inside of a ring of fire..."
    m 3etc "Yuri's file was this weird mess of random characters that I for the life of me could not understand even if I tried to figure it out."
    m 3eud "Natsuki's file was an image of these weird blue wavy lines..."
    m 1eusdla "And Sayori's file was this weird screeching that really startled me when I opened it."
    m 1eub "Just a bunch of random nonsense, right? Those files seemed to have nothing to do with us whatsoever."
    m 1eua "Those files are just files that the game checks for every now and then to make sure all the characters are fine."
    m 1etb "And when one of them is missing, then it excludes that one from gameplay, it seems."
    m 1eua "Well, that's all I know."
return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_flipacoin",category=["misc"],prompt="Can you flip a coin for me?",pool=True,unlocked=True))

label monika_flipacoin:
    $ land = renpy.random.randint(1,2000)

    m 1eua "Need to make a quick split decision, [player]?"
    m 1eub "Let me go get one."
    m 1zmq "..."
    m 1hua "I'm back!"

    if land > 0 and land < 1000:
        m 1eua "It landed on heads!"
        m 1eub "I don't really have a way of showing it to you, but you're just gonna have to trust me, ok?"
    if land == 1000 or land == 1001:
        m 1duc "[player], you're not gonna balieve this, but..."
        m 1wua "It landed on it's side!"
        m 1eub "I don't really have a way of showing it to you, but you're just gonna have to trust me, ok?"
    if land > 1001 and land < 2001:
        m 1eua "It landed on tails!"
        m 1eub "I don't really have a way of showing it to you, but you're just gonna have to trust me, ok?"

    m 1eubla "You know, it makes me really happy that you're asking me to do this, instead of googling 'flip a coin', or getting one yourself."
    m 1hublb "It may seem cheesy, but this little gesture make me feel cluser to you in a way."
return




