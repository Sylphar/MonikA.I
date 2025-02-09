These scripts are aimed a making good datasets for Monika LoRAs. They intake the rpy files in, well, rpy-files and extract the dialogues and emotions (by looking at the spritecodes) of each line to create a giant, fomatted compendium of Monika. The rpy files that are already in the folder are those I found to be the most important for me, including all of the base game and some submods I like. 
None of this is perfect yet, I'm working on it. Notably, I need to know all parameters that exist like [mas_get_player_nickname].

- Monika-filtering-plain-text.py creates a human-readable dataset. Probably not the best. After using, use "cleaning_punctuation_for..." to remove spaces before every punctuaction. Handles branching by creating "alternative-paths". For exemple :

##ID: mcl_practical | Topic: Philosophy, Practicality | Categories: philosophy | Can occur randomly
[cheerful] Assistant:Hey, <USER>.
[cheerful] Assistant:So, I was looking up an old text talking about…
[pensive] Assistant:... Hey, you know what? Let’s stop talking about this for a moment.
[interested] [pensive] Assistant:I talk a lot about philosophy and psychology and the like, right?
[neutral] Assistant:Be truthful with me. Is it boring? Even if it’s just sometimes?
Human: Admittingly, it’s not really easy casual talk.
[happy] [neutral] [worried] Assistant:That’s understandable. Thanks for being such a good listener nevertheless, <USER>.

=== Alternative Path ===

Human: A little bit, sometimes.
[happy] [neutral] [worried] Assistant:Hey, I’m really happy you’re always happy to listen and engage with my interests even if it is not your thing. That means a lot.

=== Alternative Path ===

Human: Not at all.
[happy] [neutral] [worried] Assistant:It’s comforting that we can have these sorts of deep conversations. If it ever gets tiring, I trust you to let me know otherwise.

--------

- ChatMLMonikaLines.py creates a mostly machine-readable dataset following the format of ChatML, which has become a standard. This one is very verbose, cadrating every line with a spritecode with a system info containing the emotion tags. Has advantages and inconvenient, notably prefers greatly very short answers. After using, use "zzzdialogue-combiner" to get the combined database named "MonikaDatabse.txt". Handles branching paths by adding the previous Monika line to the message after the user input, this way it doesn't get as confused. Exemple :

<|im_start|>system
Metadata:
- eventlabel: bookreading
- categories: ['literature', 'media']
- prompt: Reading books together
- random: True
<|im_end|>
<|im_start|>system
Emotions of the assistant: ['neutral'] ##Derived from the spritecodes with the emotion evaluation functions in the script
<|im_end|>
<|im_start|>assistant
You already know I love books, that's a given
<|im_end|>
<|im_start|>system
Emotions of the assistant: ['neutral'] ##Derived from the spritecodes with the emotion evaluation functions in the script
<|im_end|>
<|im_start|>assistant
<USER>, do you read books ?
<|im_end|>
<|im_start|>user
Yes.
<|im_end|>
<|im_start|>system
Emotions of the assistant: ['neutral']
Previous assistant message: "<USER>, do you read books ?" ##we get this info every time there is a user message, since they represent choices. This is to keep fluidity in the conversation despite many branching paths that may or may not rejoin.
<|im_end|>
<|im_start|>assistant
That makes me happy to hear!
<|im_end|>

- ChatMLMonikaParagraphs.py creates a mostly machine-readable dataset following the format of ChatML, which has become a standard. This one is much less verbose, only cadrating with system information once per branching, using a priority and intensity function to determine which two emotions are the diominant ones in the paragraphs. Main advantage is that this one creates smaller datasets (easier to train with smaller hardware) and makes LoRAs that should rpefer longer answers. After using, use "zzzdialogue-combiner" to get the combined database named "MonikaDatabse.txt". Handles branching paths by adding the previous Monika line to the message after the user input, this way it doesn't get as confused. Exemple :

<|im_start|>system
Metadata:
- eventlabel: bookreading
- categories: ['literature', 'media']
- prompt: Reading books together
- random: True
<|im_end|>
<|im_start|>system
Emotions of the assistant: ['neutral'] ##Here, I would like your opinion as to how we could derive automatically the emotions of a whole paragraph based on each line's emotion.
<|im_end|>
<|im_start|>assistant
You already know I love books, that's a given
<USER>, do you read books ?
<|im_end|>
<|im_start|>user
Yes.
<|im_end|>
<|im_start|>system
Emotions of the assistant: ['neutral'] ##This shall be a new dialogue bit, like the one just before the user imput
Previous assistant message: "<USER>, do you read books ?" ##we get this info every time there is a user message, since they represent choices. This is to keep fluidity in the conversation despite many branching paths that may or may not rejoin.
<|im_end|>
<|im_start|>assistant
That makes me happy to hear!
<|im_end|>

- MonikaLoRA.py is the true way to format the rpy script dialogue data into something that text-gen-webui can recognize for its formatting (if you replace the chatml-format file in training/format by ChatMLFormat here in this repo). This one is not too verbose, only cadrating with system information once per branching, using a priority and intensity function to determine which two emotions are the diominant ones in the paragraphs. Main advantage is that this one creates smaller datasets (easier to train with smaller hardware) and makes LoRAs that should rpefer longer answers. THIS ONE DOESN'T MAKE THINGS IN CHATML STYLE, BUT IN A STYLE ADAPTED FOR TRAINING WITH TEXT-GEN-WEBUI: YOU NEED TO REPLACE THE CHATML-FORMAT FILE IN TEXT-GEN/TRAINING/FORMAT WITH CHATML-FORMAT FROM THIS REPO. Handles branching paths by adding the previous Monika line to the message after the user input, this way it doesn't get as confused. Oh trust me this is a PAIN to get working. Exemple :

See MoniExemple.json

FAQ 
>What is a LoRA ?
Think of it as a specialisation module for a model. If you train a LoRA on some document, depending on how hard you train it, it will first learn to copy the style, then with more training, it will learn the content, then with even more training, you get into precision work and extreme knowledge and comprehension of the content. NOTE : THEY ONLY WORK ON TEXT-GEN-WEBUI AS A LOADER USING TRANSFORMERS (UNQUANTIZED) OR EXLLAMAV2 (models with bpw in their name), (or koboldcpp with some tweaking that I don't understand yet ? Maybe do some research on this one)
In this case, it's smart to keep the training low, since information is best written by the human in character info and memories on SillyTavern/Text-gen.

>How do I train a LoRA
The easiest way is by using text-gen-webui's "training" tab. See the written tutorial as to how to install and use text-gen-webui.
It takes literal hours to train LoRAs, and pretty good hardware (think like 16GB VRAM to train a 8b model), be warned. 
On the right side, choose your dataset, whether plain text or not. For plain text, the stopper is ##. 
For parameters, I really don't know and I am doing a ton of tests. But for now I recommend a loss of 1.2 (advanced parameters), rank of around 16, alpha of 32, batch size up to 128 if your hardware can handle it (bigger is better), 3 epochs, don't touch the learning rate.

>Most backends, like koboldcpp, don't accept LoRAs (easily). How the hell do I do ?
If you have a LoRA that satisfies you, you can always search how to merge it to your model... though I am unsure how to do that for now ? I know it's possible, at least. Check Huggingface for info.
