# Survivors

Exploring the data from TV show 'Survivors'

The dataset for the jury vote, castaways info and voting history can be found 
in the `survivors` library. The confessionals can be found [here](https://github.com/TBarmak/Survivor/tree/master/Confessionals)
## Leading Questions

1. Is the jury bitter when voting for the winner?
   - Russell is arguably one of the best survivor played who has played the 
     game, but has yet to win a season? Some argue it was because he had a poor 
     social game, which is probably partially truth. 
2. What makes a survivor winner? To answer this question, we will explore 
   several methods: 
   - Method 1: Can we predict winner using the following variables? 
     + Number of hidden idols found and played? blindside (strategic)
     + Number of immunity wins (challenge results) 
     + Number of confessional (personality)
     + Voting against jury ally
     + Number of vote cast against them during tribals?
   - Method 2: Using clustering to discover similar winners gameplay 
     + I would be surprised if method 1 works because there are a a lot of 
       player type(ex: strategic (boston rob, cirie, tony vlachos), 
       social (kim, michelle), ...). I will create different type of clusters: 
       - KMeans
       - Hierarchy Clustering
3. Do player get revenge when their ally gets voted out? what strategy do they 
   adopt? 
   - We think about Natalie blindside against Baylor when her alliance voted 
     out her ally Jeremy. Are all players like Natalie? Are they next on 
     the block chop? If they do manage to survive, do they get revenge?
4. Who are the challenge beast? 
   - When we think about challenges beast, Joe Anglim and Ozzy come to mind. 
     Are there any other challenge beast that fails to come to mind? 
   - To answer this question, we will find the outliers by computing residuals 
     using 1.5 IQR and cook's distance
   - we will also use Pythagorean expectancy
5. How are the returnees chosen? 
   - did they make the merge?
   - did the public like them ie lots of confessional
   - did they orchestrated blindside
   - challenge beast?
6. What kind of challenges are the most popular?
7. Can we use voting history to understand castaway dynamics? 
   - Create a new distance to measure relationship between two castaways: 
     + how many time they vote against each other (more is worse), but we need 
       to ponderate by number of days survived: if I vote for someone early 
       in the game, I have less information so I should ponderate less than 
       if it were a vote later in the game; if I vote several time for someone 
       I might not like them very much; if my vote differs from the group, I might 
       be on the out
     + can we use that distance to predict how a player will vote? can we 
       determine tribal result with this?

