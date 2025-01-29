This script exists to intake .rpy files and output AI-readable datasets, to maybe create a Monika LoRA.
Put .rpy scripts in To-Convert
Get pure text versions of them in Converted, with a big file named "monika_dataset" that is a fusion of all of them.


Need to replace [mas_get_player_nickname] with <USER>

You're absolutely on the right track with the emotional indicators! Associating specific sprites with emotional tags is a great way to capture Monika's personality and tone. Expanding those tags to include combinations (e.g., [serious], [sarcastic], [playful]) or even using an AI to help classify the emotional tone of each line could add even more nuance to the dataset. This would help the model better understand the subtleties of her speech patterns.

Now, let’s dive into your questions about LoRA training! Since your goal is to make the model speak more like Monika (focusing on style while allowing for some learning), here are some key considerations:

1. Loss Value
The loss value is a measure of how well the model is learning the patterns in your dataset. For LoRA training, you want the loss to decrease over time, but the exact value you should aim for depends on the complexity of the dataset and the model you're using.

Typical Loss Range:

For fine-tuning tasks like this, a loss value between 0.2 and 0.5 is often a good target. If the loss drops below 0.2, it might indicate overfitting (the model is memorizing the dataset rather than generalizing). If it stays above 0.5, the model might not be learning effectively.

However, since your focus is on style rather than factual accuracy, you might tolerate a slightly higher loss (e.g., 0.3–0.6) as long as the output sounds like Monika.

Monitoring Loss:

Keep an eye on both training loss and validation loss. If the training loss keeps decreasing but the validation loss plateaus or increases, it’s a sign of overfitting. In that case, you might need to adjust your dataset or regularization parameters.

2. Rank
The rank of a LoRA determines how many additional parameters are added to the base model during training. A higher rank allows the model to learn more complex patterns, but it also increases the risk of overfitting.

Recommended Rank:

For style-focused fine-tuning, a rank between 8 and 32 is usually a good starting point.

Start with a lower rank (e.g., 8 or 16) and gradually increase it if the model isn’t capturing Monika’s style well enough.

Higher ranks (e.g., 32 or 64) might be necessary if Monika’s speech patterns are particularly complex or nuanced, but be cautious of overfitting.

Trade-offs:

Lower ranks are more efficient and less prone to overfitting but may not capture all the subtleties of Monika’s style.

Higher ranks can capture more detail but require more data and computational resources.

3. Other Key Parameters
Here are some additional parameters to consider when training your LoRA:

a. Learning Rate
The learning rate controls how quickly the model adapts to the new data.

For LoRA fine-tuning, a learning rate between 1e-5 and 5e-4 is typical.

Start with a lower learning rate (e.g., 1e-5) and increase it if the model isn’t learning effectively.

If the loss fluctuates wildly, the learning rate might be too high.

b. Batch Size
The batch size determines how many samples the model processes at once.

A batch size of 8 to 32 is usually a good range for LoRA training.

Larger batch sizes can speed up training but require more memory.

Smaller batch sizes can help with generalization but may slow down training.

c. Epochs
The number of epochs determines how many times the model sees the entire dataset.

For style-focused fine-tuning, 3 to 10 epochs are often sufficient.

Monitor the loss and stop training if it plateaus or starts to increase (indicating overfitting).

d. Regularization
Regularization techniques like dropout or weight decay can help prevent overfitting.

If you’re using a small dataset, consider adding a small amount of weight decay (e.g., 0.01) or dropout (e.g., 0.1).

e. Dataset Size
Since your dataset contains nearly all of Monika’s dialogue, it should be large enough for effective training. However, if you notice overfitting, consider:

Adding slight variations to the dialogue (e.g., paraphrasing some lines).

Using data augmentation techniques (e.g., shuffling word order slightly while maintaining meaning).

4. Style vs. Content
Since your primary goal is to capture Monika’s style, you might want to prioritize the following:

Emphasis on Emotional Tags: Ensure the model pays close attention to the emotional indicators ([happy], [blushing], etc.). These tags are key to replicating her tone.

Contextual Prompts: Include contextual cues in your dataset (e.g., [festival planning], [philosophical discussion]) to help the model understand the situation and respond appropriately.

Avoid Overfitting: Since you’re not as concerned with factual accuracy, you can afford to let the model generalize a bit more. This means you might not need to push the loss value as low as you would for a factual task.

5. Evaluation
After training, evaluate the model’s performance by:

Qualitative Testing: Generate responses and check if they sound like Monika. Pay attention to tone, phrasing, and emotional consistency.

Quantitative Metrics: Use metrics like perplexity (how well the model predicts the next word) or BLEU score (how closely the output matches reference dialogue) to measure performance.

6. Tools and Frameworks
If you’re using a specific framework (e.g., Hugging Face’s peft library for LoRA), make sure to:

Use their built-in tools for monitoring loss and adjusting parameters.

Experiment with different configurations (e.g., rank, learning rate) to find the best setup for your task.

Summary of Recommendations
Loss Value: Aim for 0.2–0.5, but prioritize style over strict accuracy.

Rank: Start with 8–16 and increase if necessary.

Learning Rate: Begin with 1e-5 and adjust as needed.

Batch Size: Use 8–32 depending on your hardware.

Epochs: Train for 3–10 epochs, monitoring for overfitting.

Regularization: Add slight weight decay or dropout if overfitting occurs.

If you have any more questions or need further clarification, feel free to ask! Your project is incredibly cool, and I’m excited to see how it turns out. Monika would be proud! 😊