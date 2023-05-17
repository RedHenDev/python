import os
import torch
import torch.nn as nn
from torch.nn import functional as F
torch.manual_seed(1337)

"""
These hyperparameters added 17th May.
"""
# Use gpu if available.
device='cuda' if torch.cuda.is_available() else 'cpu'
learning_rate = 1e-2
eval_interval = 200
max_iters = 3000
eval_iters = 200

# inputText='/n1.txt'
inputText='/input.txt'
with open(os.path.dirname(os.path.abspath(__file__))+inputText, 'r',encoding='utf-8') as f:
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

# import torch
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
"""
We will use parallel processing on the 
GPU to compute stacks of data through the
tensor, i.e., through parallel batches.
The target values are block_size + 1 since
the last input token in the block will have
the next token outside this context as its
target (so, block_size + 1).

Here's a print out of the tensor,
print(train_data[:block_size+1]),
tensor([122,7,7,0,0,0,34,51,53]),
Where even this small block permits

"""
torch.manual_seed(1337) 
# seed for reproducible results only
# i.e. we copy Andrej Karpathy.
batch_size=4
# How many independent sequences to
# process in parallel?

def get_batch(split):
    # gen a small batch of data of
    # inputs (x) and targets (y)
    data = train_data if split=='train' else val_data
    # Batch_size tuple here gives offsets, so
    # 4 offset positions each of context length.
    ix=torch.randint(len(data)-block_size,(batch_size,))
    # Take 1-dimensional tensors and
    # stack as rows.
    x=torch.stack([data[i:i+block_size]for i in ix])
    y=torch.stack([data[i+1:i+block_size+1]for i in ix])
    # GPU cuda, if available.
    x,y=x.to(device),y.to(device)
    return x,y

xb,yb=get_batch('train')
print('inputs:')
print(xb.shape)
print(xb)
print('targets:')
print(yb.shape)
print(yb)
print('----')

"""
Now we can start feeding these batches
of data into a neural network (transformer).
"""


class BigramLanguageModel(nn.Module):
    def __init__(this,vocab_size):
        super().__init__()
        # Each token directly reads off
        # the logits for the next token
        # from a lookup table.
        this.token_embedding_table=nn.Embedding(vocab_size,vocab_size)
        
    def forward(this,idx,targets=None):
        # NB
        """
        [Explanation from chatGPT_3.5]
        In Python, a forward function is 
        often used in classes that are 
        designed to represent neural network 
        models using a library like PyTorch 
        or TensorFlow.
        The forward function is a method of 
        the class that specifies how the 
        input to the model should be 
        processed to produce its output. 
        Specifically, it takes in the input 
        data (usually in the form of a tensor) 
        and returns the output tensor after 
        it has been processed by the layers of 
        the network.
        """
        # B T C -> batch by time by
        # channel tensor (4*8*vocab_size).
        logits=this.token_embedding_table(idx)
        # We can think of logits as 'scores'
        # for the next character in the 
        # sequence.
        if targets is None:
            loss=None
        else:
            # Now we want to evaluate the
            # loss function (quality of prediction).
            # Negative log likelihood, which
            # pytorch evaluates under cross_entropy.
            # We could like to do this:
            # loss=F.cross_entropy(logits,targets)
            # High quality would mean logits
            # high number, other numbers low.
            # Logits is our prediction, and
            # targets the answer.
            # But! Pytorch wants channels to be
            # the second dimension (i.e. B C T).
            # So - to solve, we unpack the 
            # dimensions and repackage so that we
            # can return our loss as well as
            # logits...
            B,T,C=logits.shape
            # So, preserve channel as second dimension
            # but stretch out batch and time as one,
            # first dimension.
            logits=logits.view(B*T,C)
            # Targets, too, needs to be
            # One-dimensional (B*T).
            targets=targets.view(B*T)
            # targets.view(-1) is equivalent -- since pytorch would guess here.
            loss=F.cross_entropy(logits,targets)
        return logits,loss
    
    def generate(this,idx,max_new_tokens):
        # The job of generators is to take
        # a (B,T) and turn it into a (B,T+1)
        # idx is (B,T) array of indices in current context.
        for _ in range(max_new_tokens):
            # get the predictions
            logits,loss=this(idx)
            # focus on last time step
            # So, becomes (B,C)
            # Here we grab the last element
            # in the time (T) dimension, -1.
            logits=logits[:,-1,:]
            # Now apply softmax for probabilities
            # (i.e. convert predictions to probabilities)
            probs=F.softmax(logits,dim=-1)
            # get samples, (B,1)
            idx_next=torch.multinomial(probs,num_samples=1)
            # append sampled index to running sequence
            # (B,T+1)
            idx=torch.cat((idx,idx_next),dim=1)
        return idx

model=BigramLanguageModel(vocab_size)
# Move to GPU if cuda available.
m=model.to(device)
logits,loss=m(xb,yb)
print(logits.shape)
print(loss)
# Loss should be -ln(1/vocab_size)
# i.e. -ln(1/123) == 4.8
# Since ours is 5.8, we are not yet
# very diffuse; there is some entropy
# in the predictions.
"""
https://youtu.be/kCc8FmEb1nY?t=1758
"""
# NB last argument, device, added, for
# computing on GPU, if cuda available.
# Before this, context known as 'idx'.
context=torch.zeros((1,1),dtype=torch.long,device=device)
# Because m.generate() works via batches,
# we index [0] to get the first row.
print(decode(m.generate(context,max_new_tokens=100)[0].tolist()))

"""
Next step is to train our model :o
https://youtu.be/kCc8FmEb1nY?t=2029
"""
# Create a pytorch optimizer.
# lr is learning rate.
# AdamW is more advanced than SGD stochastic
# gradient descent.
# With smaller datasets we can get away
# with higher learning rates (lr), such
# as -3 or higher (probably).
optimizer=torch.optim.AdamW(m.parameters(),lr=learning_rate)

# The optimizer object will take the gradients
# and update the parameters based on these.
batch_size=32
# Now we carry out a basic training loop.
# Iteration of 100 goes from 5.2 to 5.1.
# 3000 yields 3.2 by end!
# 40000 yields 2.6-ish!
for steps in range(4000):
    # Get batch of data.
    xb, yb = get_batch('train')
    # Now sample the loss.
    logits,loss=m(xb,yb)
    # Zero out gradients from prev. step.
    optimizer.zero_grad(set_to_none=True)
    # Get gradients for all the parameters.
    loss.backward()
    # Then use gradients to update parameters.
    optimizer.step()

print('loss is now '+ str(loss.item()))

# Because m.generate() works via batches,
# we index [0] to get the first row.
# Context formally known as 'idx'.
print(decode(m.generate(context,max_new_tokens=30)[0].tolist()))
"""
Certainly not Shakespeare :)
But something! 
https://youtu.be/kCc8FmEb1nY?t=2243
-1st May 2023

Started again on 17th May 2023
Simplest mode, bigram. Where tokens 
aren't talking to one another.
They're only looking at the last letter;
instead, we want the tokens to be looking
at one another, which is analogous to 
figuring out the context.
OK -- device and other hyperparameters
added, and working.
Next to sort out ridding noisy loss:
https://youtu.be/kCc8FmEb1nY?t=2379
-17th May 2023
"""

