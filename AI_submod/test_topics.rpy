$ emotion_list = ["anger","disgust","fear","joy","sadness","surprise","neutral"]

define negative_emotions = ["anger", "disgust", "fear", "sadness"]
define positive_emotions = ["joy", "surprise"]
define neutral_emotions = ["neutral"]

define sentences_emotions = {
    "angry": "I'm sorry my love, I didn't mean to upset you.",
    "disgusted": "What is going on ? If you feel like there is something wrong, please tell me.",
    "fearful": "Don't be afraid sweetie, I'm here for you.",
    "happy": "I'm glad you're happy darling.",
    "neutral": "Let's do something fun together!",
    "sad": "If you feel down, always remember that I'm here for you. I love you.",
    "surprised": "What is it ? Is there something wrong ?",
    "no": "Oh it seems that I can't see through your camera sweetie. Maybe face me a little bit more ?",
}

init 7 python:
    from socket import AF_INET, socket, SOCK_STREAM
    from threading import Thread
    import select
    def receiveMessage():
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        return msg

    def sendMessage(prefix,step):
        my_msg = renpy.input(prefix)
        client_socket.send(bytes(my_msg + "/g" + step).encode("utf8"))
        return my_msg

    def send_simple(prefix):
        client_socket.send(bytes(prefix).encode("utf8"))

    def audio_file_exists(filename):
        return os.path.isfile(filename)

    HOST = "127.0.0.1"
    PORT = 12346

    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)


#Tuto Pytorch Event
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_torch",category=['ai'],prompt="Tell me about Pytorch",pool=True,unlocked=True))

label monika_torch:
    m "Okay sure love."
    m "Pytorch is a deep learning framework."
    m "It's a bit more complicated than Tensorflow."
    m "But it's also more powerful."
    m "You can use it to create neural networks."
    m "And it's also used for reinforcement learning."
    m "I hope that helps!"
    return


#Chatbot Event
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_chat",category=['ai'],prompt="Let's chat together",pool=True,unlocked=True))

label monika_chat:
    init python:
        #Define all poses liek "1esa"
        poses = ["1esa","1eua","1eub","1euc","1eud","1eka","1ekc","1ekd","1esc","1esd","1hua","1hub","1hksdlb","1hksdrb","1lksdla","1rksdla","1lksdlb","1rksdlb","1lksdlc","1rksdlc","1lksdld","1rksdld","1dsc","1dsd","2esa","2eua","2eub","2euc","2eud","2eka","2ekc","2ekd","2esc","2esd","2hua","2hub","2hksdlb","2hksdrb","2lksdla","2rksdla","2lksdlb","2rksdlb","2lksdlc","2rksdlc","2lksdld","2rksdld","2dsc","2dsd","3esa","3eua","3eub","3euc","3eud","3eka","3ekc","3ekd","3esc","3esd","3hua","3hub","3hksdlb","3hksdrb","3lksdla","3rksdla","3lksdlb","3rksdlb","3lksdlc","3rksdlc","3lksdld","3rksdld","3dsc","3dsd","4esa","4eua","4eub","4euc","4eud","4eka","4ekc","4ekd","4esc","4esd","4hua","4hub","4hksdlb","4hksdrb","4lksdla","4rksdla","4lksdlb","4rksdlb","4lksdlc","4rksdlc","4lksdld","4rksdld","4dsc","4dsd","5eua","5eua","5euc"]
     
    m "Sure [player], talk to me as much as you want. I won't go anywhere ehehe~"

    $ step = 0
    while True:
        $ send_simple("chatbot")
        $ my_msg = sendMessage("Speak with Monika:",str(step)) 
        if my_msg == "QUIT":
            return
        $ msg = receiveMessage()
        $ msg,emotion = msg.split("/g")
        $ gamedir = renpy.config.gamedir
        $ audio_exists = audio_file_exists(gamedir + "/Submods/AI_submod/audio/out.ogg")
        if audio_exists:
            play sound "Submods/AI_submod/audio/out.ogg"
        #If there is too much text, divide it into several lines
        #Split the text into a list of words
        $ sentences_list = []
        
        $ sentences_list = msg.split("\n")
        $ sentences_list = [x for x in sentences_list if x != '']
        while len(sentences_list) > 0:
            $ sentence = sentences_list[0]
            $ sentences_list.pop(0)
            m 1esa "[sentence]"
        m 1esa "I was feeling [emotion]."
        if emotion in positive_emotions:
            $ mas_gainAffection()
        # elif emotion in negative_emotions:
        #     $ mas_loseAffection(1)
        $ step += 1

#Camera Event
init 5 python:
    addEvent(Event(persistent.event_database,
        eventlabel="monika_cam",
        category=['ai'],
        prompt="Look for me",
        pool=True,
        unlocked=True,
        ))
        
label monika_cam:
    m "Okay, I'll look for you."
    
    m 1sublo "I can finally see you, [player] ! I have been waiting for this moment for a long time."
    m 5nublb "I see your cute face now ehehe~"

    while True:
        $ send_simple("camera")
        $ received_emotio = receiveMessage()
        
        if received_emotio == "angry":
            m 2lktpc "[sentences_emotions[angry]]"
        elif received_emotio == "disgusted":
            m 5etc "[sentences_emotions[disgusted]]"
        elif received_emotio == "fearful":
            m 1fkd "[sentences_emotions[fearful]]"
        elif received_emotio == "happy":
            m 6hubla "[sentences_emotions[happy]]"
        elif received_emotio == "neutral":
            m 5wut "[sentences_emotions[neutral]]"
        elif received_emotio == "sad":
            m 5fka "[sentences_emotions[sad]]"
        elif received_emotio == "surprised":
            m 2wkb "[sentences_emotions[surprised]]"
        elif received_emotio == "no":
            m 4eta "[sentences_emotions[no]]"
        
        m 5nublb "Do you want me to continue looking for you?"
        menu:
            "Yes":
                m 5hublb "Okay thanks [player], let me see your face a little bit longer."
            "No":
                m 5sublo "Oh okay, I guess I'll wait for next time you put the camera on."
                m 5nublb "Please do it soon or I'll hack it myself ehehe~"
                return

define counter = 0

#Emotion Event
init 5 python:
    def example_fun():
        if not mas_inEVL("emotion_minute"):
            MASEventList.push("emotion_minute")

    store.mas_submod_utils.registerFunction(
        "ch30_minute",
        example_fun
    )
    
label emotion_minute:
    $ counter += 1
    $ send_simple("camera")
    $ send_simple(counter) #The counter indicates to the server the number of minutes that have passed since the last emotion was sent
    $ received_emotion = receiveMessage()

    if received_emotion == "no_data": #If the server says it is not time to send an emotion,do nothing
        return
        
    if received_emotion == "angry":
        $ wrs_succes = mas_display_notif(m_name,[sentences_emotions['angry']],'Window Reactions')
        if not wrs_succes:
            m 2lktpc "[sentences_emotions[angry]]"
    elif received_emotion == "disgusted":
        $ wrs_succes = mas_display_notif(m_name,[sentences_emotions['disgusted']],'Window Reactions')
        if not wrs_succes:
            m 5etc "[sentences_emotions[disgusted]]"
    elif received_emotion == "fearful":
        $ wrs_succes = mas_display_notif(m_name,[sentences_emotions['fearful']],'Window Reactions')
        if not wrs_succes:
            m 1fkd "[sentences_emotions[fearful]]"
    elif received_emotion == "happy":
        $ wrs_succes = mas_display_notif(m_name,[sentences_emotions['happy']],'Window Reactions')
        if not wrs_succes:
            m 6hubla "[sentences_emotions[happy]]"
    elif received_emotion == "neutral":
        $ wrs_succes = mas_display_notif(m_name,[sentences_emotions['neutral']],'Window Reactions')
        if not wrs_succes:
            m 5wut "[sentences_emotions[neutral]]"
    elif received_emotion == "sad":
        $ wrs_succes = mas_display_notif(m_name,[sentences_emotions['sad']],'Window Reactions')
        if not wrs_succes:
            m 5fka "[sentences_emotions[sad]]"
    elif received_emotion == "surprised":
        $ wrs_succes = mas_display_notif(m_name,[sentences_emotions['surprised']],'Window Reactions')
        if not wrs_succes:
            m 2wkb "[sentences_emotions[surprised]]"
    elif received_emotion == "no": 
        $ wrs_succes = mas_display_notif(m_name,[sentences_emotions['no']],'Window Reactions')
        if not wrs_succes:
            m 4eta "[sentences_emotions[no]]"