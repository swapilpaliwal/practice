# Coding challenge:
# Average degree calculator  

#### Notes
I have used python programming language (version 2.7) for this challenge
and windows programming environment.

#### Dependency :
- numpy package (1.11.0)

#### Notes for unittests:
- I haven't done unit tests due to lack of time right now, but here are few
things i would consider checking.

testing suite would probably be unittests or nosetests

  1. The size of array of time matches the size of array of tweets.
    This was true in the tweets.txt file but i would test for it in case they
    are different.
    I would also like to see if try/except blocks are working in any cases that
    i haven't considered.

  2. I would make a toy set and check for constraints like average degree for
     out of order tweets, average degree for in order but outside time window tweets
     and average degree of tweets (with no hastags and with one hashtag).


  #### Notes for scalability:
  The current code takes around 2.5 minutes to run through and consists of for loops.
  1.  I think i can make it faster using map and lambda functions, vectorized numpy arrays, and distributed computing like spark, hadoop with map reduce architecture.

  #### note on one slight logic error that might be there.
  1. I have not considered all tweets timimgs and thus the 60 sec rule might not have been followed when the tweets did not have any hashtags.
  The code in that case took more than 8-10 minutes when i tried running all tweets in the for loop.

  perhaps numpy vectorized functions, Cython,  and map/lambda functions could ease that.
