**Intermediate Project Report**

Henry Miller and Ryan Greer

We are doing the Mancala game implementation, so we already had a decent framework. We fixed several small edge cases that were causing trouble from HW7, as well as implementing a random game function.
3. We simulated 100 games between 2 random players, and often found player 1 with slightly more wins, usually having a 50-55% winrate. This isn't always the case, but we suspect it has something to do with having the first move, and some rules that were omitted from this version of Mancala could benefit player 1 as well. We also simulated 10,000 games, and found it was about 51% winrate for player 1. It takes on average around 41.38 turns per game.

4. Our minimax AI player has a 99-100% winrate, barely ever losing a game. On average, it takes around 29.56 turns per game.

5. When testing our minimax player with a depth of 5, the AI player almost always has 100% winrate across 100 games. It takes on average around 29.56 turns per game, and also has a runtime average of 68.79 seconds. The AI player is very dominant over the random player, essentially never losing a game. This makes a lot of sense because a player that can look at every possible move 5 steps ahead and choose the one that is going to maximize their mancala score is bound to win over a random player, or even probably most average human players. This is a stark difference from the random player, who cannot even look 1 move ahead.

6. We then built an alpha-beta AI player, which turned out to be very similar to the minimax AI player.

7.  After playing 100 games at a depth of 5 with the alpha-beta AI player, we got very similar results to minimax. The runtime however, was 26.92 seconds, which is much shorter compared to minimax. The winrate was essentially 100% across 100 games. The average turns were within 1 turn compared to minimax (around 29.12). The only main difference between this alpha-beta player and our minimax player was the runtime being much shorter on the alpha-beta side, which makes sense because alpha-beta prunes away branches that we have already found a better state for. With this, we are able to get the same result without needing to evaluate as many game states.

8. (Extra Credit) After playing 100 games of the alpha-beta player vs a random player at a depth of 10, the runtime total was 22 minutes and 38.65 seconds, and an average per game was around 13.59 seconds. The alpha-beta AI still wins 100% of the time, and it takes an average of 27.16 turns per game. Increasing the number of plies here does not make a noticeable difference against a random player, because the AI will still win everytime when looking 5 moves ahead vs 10 moves ahead. If the random player was changed to a human or a different AI model where the winrate for 5 plies wasn't as dominant, then 10 plies would be much better compared to 5, but it is at the cost of runtime.

Through this project, we learned a lot about minimax and alpha- beta pruning algorithms. It required a deep understanding of how they function, in a step-by-step way, in addition to knowledge of the tools required to code them in a game like mancala. Not only did this help us understand the fundamental recursive operations, but also how the algorithms work on each node, which we found especially helpful in understanding the deceptive simplicity and efficiency of alpha-beta pruning.
