#!/usr/bin/env node
"use strict"

/* This was made from Elijah Mills's "A Tale Told Out West"
   storytelling game; it plays similar to Hold'em Poker.

   Players each get a hand of three cards.  Each describes a character
   that is one of: a liar, a tycoon, a lover, or a bandit.  Three cards
   are dealt face-up on the table (the "flop") that is the start of the
   story these characters share (the goal, the obstacle, the boon).
   Players can play cards from their hand to replace any of the three
   cards. When they are finished, they start telling a shared story.
   When the flop cards are used and they feel it's right or the story
   slows down, deal a fourth shared card (the "turn") to be a plot-twist.
   Players can play cards from their hand again but only to alter the
   "turn," then they continue the story.  When the plot-twist is addressed,
   deal the last card (the "river") and players can play cards from their
   hand to alter only the "river."  Then collaboratively finish the story.
*/


const suits = { "C": "Liar", "D": "Tycoon", "H": "Lover", "S": "Bandit" }
/* [ goal, obstacle, boon, twist, outcome ] */
const card_chart = {
  "2C": [ "win the poker tournament", "a watchful eye", "a distraction", "a cheater", "the great challenge is won" ],
  "2D": [ "buy land from hostile farmer", "the farmer's angry posse", "some recovered paperwork", "a secret in the farmer's land", "the sought-after land is claimed" ],
  "2H": [ "reunite with a lost love", "a hostile ex-lover", "a benevolent ex-lover", "a secret admirirer", "their love reignited" ],
  "2S": [ "shoot the sherrif", "the sheriff's deputies", "the sheriff's illicit activities", "a traitor in your midst", "the sheriff is dead" ],
  "3C": [ "win the poker tournament", "a watchful eye", "a distraction", "a cheater", "the great challenge is won" ],
  "3D": [ "buy land from hostile farmer", "the farmer's angry posse", "some recovered paperwork", "a secret in the farmer's land", "the sought-after land is claimed" ],
  "3H": [ "reunite with a lost love", "a hostile ex-lover", "a benevolent ex-lover", "a secret admirirer", "their love reignited" ],
  "3S": [ "shoot the sherrif", "the sheriff's deputies", "the sheriff's illicit activities", "a traitor in your midst", "the sheriff is dead" ],

  "4C": [ "trick the mayor", "the mayor's friends", "a juicy secret", "the mayor's secret agenda", "an opponent is tricked" ],
  "4D": [ "finance a new railroad", "an entire town", "a wealthy benefactor", "an ally's secret is revealed", "the project is completed" ],
  "4H": [ "find new love", "a jealous rival", "a wise mentor", "the fact their lover loves another", "there is a bittersweet goodbye" ],
  "4S": [ "rob the bank", "armed guards", "an insider", "more than just money in the bank", "great wealth is obtained"],
  "5C": [ "trick the mayor", "the mayor's friends", "a juicy secret", "the mayor's secret agenda", "an opponent is tricked" ],
  "5D": [ "finance a new railroad", "an entire town", "a wealthy benefactor", "an ally's secret is revealed", "the project is completed" ],
  "5H": [ "find new love", "a jealous rival", "a wise mentor", "the fact their lover loves another", "there is a bittersweet goodbye" ],
  "5S": [ "rob the bank", "armed guards", "an insider", "more than just money in the bank", "great wealth is obtained"],

  "6C": ["escape a debt", "angry debt collectors", "a disguise", "a lender's dark secret", "responsibility was evaded" ],
  "6D": ["sell the derelict saloon", "a squatter", "the mayor", "an enemy's hidden identity", "a great burdern is lifted" ],
  "6H": ["find a childhood sweetheart", "an angry guardian", "a loving relative", "a tragic loss", "there is a reunion" ],
  "6S": ["rob the train", "a fast train", "a rickety train bridge", "a rival gang", "the dangerous mission is completed" ],
  "7C": ["escape a debt", "angry debt collectors", "a disguise", "a lender's dark secret", "responsibility was evaded" ],
  "7D": ["sell the derelict saloon", "a squatter", "the mayor", "an enemy's hidden identity", "a great burdern is lifted" ],
  "7H": ["find a childhood sweetheart", "an angry guardian", "a loving relative", "a tragic loss", "there is a reunion" ],
  "7S": ["rob the train", "a fast train", "a rickety train bridge", "a rival gang", "the dangerous mission is completed" ],

  "8C": ["avoid a hanging", "clear evidence of a crime", "hidden allies", "an official with shady connections", "a deadly fate was evaded"],
  "8D": ["find a hidden treasure", "guardians of the treasure", "a helpful clue", "a misunderstanding of the treasure", "the treasure is claimed"],
  "8H": ["leave a hateful lover", "an enemy with leverage", "evidence of betrayal", "a hateful lover's ex-lover", "the toxic relationship is ended"],
  "8S": ["steal cattle", "a great distance", "a helpful environment", "a dangerous interested person", "the journey is completed"],
  "9C": ["avoid a hanging", "clear evidence of a crime", "hidden allies", "an official with shady connections", "a deadly fate was evaded"],
  "9D": ["find a hidden treasure", "guardians of the treasure", "a helpful clue", "a misunderstanding of the treasure", "the treasure is claimed"],
  "9H": ["leave a hateful lover", "an enemy with leverage", "evidence of betrayal", "a hateful lover's ex-lover", "the toxic relationship is ended"],
  "9S": ["steal cattle", "a great distance", "a helpful environment", "a dangerous interested person", "the journey is completed"],

  "TC": ["disgrace a public figure", "loyal allies", "damning evidence", "lies that get revealed", "there is a fall from grace"],
  "TD": ["claim an inheritence", "a vengeful banker", "a legal loophole", "an illegitimate child", "a windfall is accepted"],
  "TH": ["shame a bitter rival", "the absence of the quarry", "a friend who knows something", "an untimely death", "there is sweet revenge"],
  "TS": ["destroy a rival gang", "the rival gang's loyal members", "a retired soldier's armoury", "the rival gang's hidden agenda", "their rival is destroyed"],
 
  "JC": ["rob a grave", "the undertaker", "a detailed itinerary", "a burial gone wrong", "the dead are disturbed"],
  "JD": ["gain powerful status", "a big-city lawyer", "dirt on important people", "a hidden plan", "power status is recieved"],
  "JH": ["help someone in need", "a person's sordid past", "a chance at a new start", "a terrible secret", "a person thrives"],
  "JS": ["break out a prisoner", "the prison", "a compelling bribe", "an unknown vulnerability", "freedom is gained"],

  "QC": ["gaslight the town", "a local newspaper", "a powerful truth", "a new influence", "a group of people are tricked"],
  "QD": ["destroy a business rival", "the rival's great success", "help from a powerful friend", "a mysterious fire", "the enemy suffers"],
  "QH": ["restore their reputation", "wrongs done in the past", "a favour owed", "a reminder of the past", "a legacy is restored"],
  "QS": ["burn down the barn", "a violent militia", "dynamite", "an unplanned explosion", "the target is destroyed"],
}


Array.prototype.shuffle=function(){var e=[];while(this.length){e.push(this.splice(Math.random()*this.length,1)[0])}while(e.length){this.push(e.pop())}return this}

function build_story() {
  var deck = Object.keys(card_chart)
  deck.shuffle()
  var story = []
  var nchars = Math.floor(Math.random()*3+1)
  var buffer = ""
  if(nchars > 1) {
    // this is ugly I surely can improve this
    buffer = "The main characters are a "
    for (var i=0; i<nchars; i++) {
      buffer += suits[deck[0].substr(1)]
      deck.shift()
      if(i == (nchars-2))
        buffer += ", and a "
      else if(i != (nchars-1))
        buffer += ", a "
    }
  }
  else {
    buffer = "The main character is a " + suits[deck[0].substr(1)]
    deck.shift()
  }
  buffer += "."
  story.push(buffer)

  if(nchars > 1)
    buffer = "Their goal is to "
  else
    buffer = "The goal is to "
  buffer += card_chart[deck[0]][0] + "."
  story.push(buffer)
  deck.shift()

  buffer = "The obstacle is " + card_chart[deck[0]][1] + "."
  story.push(buffer)
  deck.shift()

  buffer = "They have " + card_chart[deck[0]][2] + ","
  story.push(buffer)
  deck.shift()
  
  buffer = "but there is " + card_chart[deck[0]][3] + "."
  story.push(buffer)
  deck.shift()

  buffer = "In the end, " + card_chart[deck[0]][4] + "."
  story.push(buffer)
  deck.shift()

  return story.join(" ")
}

var story = build_story()
process.stdout.write(story)
process.stdout.write("\n")

