import os

with open(os.path.dirname(os.path.abspath(__file__))+'/n1.txt', 'r',encoding='utf-8') as f:
    text = f.read()

print(len(text))
print('/n')
print(text[:1000])

"""
OK, so next we want a sorted list of the set of all characters.

A note from Google Bard: -
[start Bard]
The set() function in Python creates a set object. 
A set is an unordered collection of unique elements. 
This means that the elements in a set cannot be repeated, 
and they do not have a specific order.

To create a set, you can use the 
set() function and pass in an iterable object. 
An iterable object is an object that can be iterated over, 
such as a list, tuple, or string.
[end Bard]

Ah, so 'set()' will remove any repeated items.
List() makes it iterable, ordered.
And sorted does what? Let's experiment.
Join is useful in this experiment.
"""
chars_us=(list(set(text)))
chars=sorted(chars_us)
vocab_size=len(chars)
print('unsorted ' + ''.join(chars_us))
print('sorted ' + ''.join(chars))
print('vocab size is ' + str(len(chars)))

"""
Next we want to develop strategy to 'tokenise' our input text.
This means to convert our string of text into some sequence
of integers (according to a vocab of possible elements).

So, we want a pair of functions that can encode and decode our
raw text input string; for us, this will be at the level of 
characters, unlike chatGPT which tokenises at morpheme-like level.
In short, a mapping from characters to integers.

Google uses a different mapping (or schema), called SentencePiece.
It is a sub-word tokeniser.
(https://github.com/google/sentencepiece)

OpenAI uses tiktokens.
(https://github.com/openai/tiktoken)
"""
# Two look-up tables, mapping between character and integer.
stoi={ch: i for i,ch in enumerate(chars)}
itos={i:ch for i,ch in enumerate(chars)}
encode=lambda s: [stoi[c] for c in s]
decode=lambda l: ''.join([itos[c] for c in l])
# print(encode('testing, testing'))
# print(decode(encode('testing, testing')))

"""
Now we can tokenise the dataset, i.e. the input text.
To do so, we're going to use pytorch (https://pytorch.org).
[pip3 install torch torchvision torchaudio]
"""

import torch
data=torch.tensor(encode(text),dtype=torch.long)
print(data[:1000])
# 13:13 on video-https://www.youtube.com/watch?v=kCc8FmEb1nY
"""
Finally, since we now have the text in a
format ready to present to the Generative
Pretrained Transformer, the last step is to
separate out two sets, a 'train' and 
'validation' set of the data.
"""
# First 90% training set, rest validation.
n=int(0.9*len(data))
train_data=data[:n]
val_data=data[n:]

"""
We only want to train the model on blocks
of the data, not the whole data -- this 
would be computationally unfeasible.
The max size of these blocks is sometimes 
called the 'context-length'.
"""
block_size=8
print(train_data[:block_size+1])