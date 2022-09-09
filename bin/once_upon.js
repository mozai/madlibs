'use strict';

var once = {
  "#": "From the card game 'Once Upon A Time'",
  "@": [ "Z_tale" ],
  "Z_tale": [
    "A %Aspect %Character, a %Item, and a %Event.",
    "A %Character, a %Aspect %Item, and a %Event."
  ], 
  "Aspect": [
    "Beautiful",
    "Blind",
    "Brave",
    "Cursed",
    "Diseased",
    "Disguised",
    "Dying",
    "Empty",
    "Evil",
    "Far Away",
    "Frightened",
    "Greedy",
    "Happy",
    "Haunted",
    "Hidden",
    "Idle",
    "Insane",
    "Long-Lost",
    "Lost",
    "Lucky",
    "Poisoned",
    "Sad",
    "Secret",
    "Sleeping",
    "Stolen",
    "Stupid",
    "Talking (animal)",
    "Talking (item)",
    "That Can Fly",
    "Tiny",
    "Ugly",
    "Very Strong",
    "Very Wise"
  ],
  "Character": [
    "Beggar",
    "Bird",
    "Child",
    "Cook",
    "Enemy",
    "Fairy",
    "Farm Animal",
    "Farmer",
    "Fiend",
    "Frog",
    "Ghost",
    "Giant",
    "Guard",
    "Horse",
    "King",
    "Monster",
    "Murderer",
    "Old Man",
    "Old Woman",
    "Orphan",
    "Outcast",
    "Parent",
    "Prince",
    "Princess",
    "Queen",
    "Shepherdess",
    "Sibling",
    "Spouse",
    "Stepmother",
    "Thief",
    "Troublemaker",
    "Witch",
    "Wolf"
  ],
  "Event": [
    "Change Of Ruler",
    "Chase",
    "Death",
    "Fight",
    "Rescue",
    "Trap",
    "Argument",
    "Object Breaking",
    "Contest",
    "Dream",
    "Escape",
    "Hard Times",
    "Journey",
    "People Meeting",
    "People Parting Company",
    "Plan",
    "Revenge",
    "When Someone Disobeys",
    "When Someone Faints",
    "Someone Is Hurt",
    "Someone Is Punished",
    "Someone Is Sent Away",
    "Someone is Punished",
    "Someone is Sent Away",
    "Something Is Revealed",
    "Storm",
    "Swallowed Whole",
    "Time Passes",
    "Transformation",
    "Two People Fall In Love"
  ],
  "Item": [
    "Barrier",
    "Command",
    "Cure",
    "Hole",
    "Wound",
    "Eye",
    "Axe",
    "Boat",
    "Book",
    "Crown",
    "Door",
    "Fire",
    "Food",
    "Gift",
    "Heart",
    "Key",
    "Ring",
    "Set of Clothes",
    "Skull",
    "Spell",
    "Sword",
    "Treasure",
    "Tree",
    "Window"
  ],
  "Place": [
    "Foreign Land",
    "Grave",
    "Well",
    "Arena",
    "Sea",
    "Cave",
    "Chapel",
    "Cottage",
    "Daytime",
    "Farm",
    "Field",
    "Forest",
    "Home",
    "In Bed",
    "Island",
    "Kingdom",
    "Kitchen",
    "Market",
    "Mountain",
    "Nighttime",
    "Palace",
    "Prison",
    "River",
    "Road",
    "Ruin",
    "Stairs",
    "Tower",
    "Town",
    "Village"
  ],
  "Ending": [
    "And for all I know they may be dancing still.",
    "And he listened to his mother's advice from then on.",
    "And he was reuinted with his family.",
    "And in the course of time they became king and queen.",
    "And never as long as she lived could it be removed.",
    "And she was reunited with her family.",
    "And so he escaped their plan for revenge.",
    "And so the prophecy had been fulfilled.",
    "And the flames rose higher and the evil place was destroyed.",
    "And the king was delighted with such an unusual gift.",
    "And the kingdom rejoiced at the end of the tyrant's reign.",
    "And the parents were reunited with their long-lost child.",
    "And there they sit to this very day.",
    "And they were blind for the rest of their days for their wickedness and falsehood.",
    "And to this day no one knows where she ran to.",
    "And when they died they passed it on to their children.",
    "As dawn broke they could see it was perfect.",
    "Beaten, the foul creature vanished and was never seen again.",
    "But it had vanished as mysteriously as it had appeared.",
    "But no matter how hard they searched they were never able to find it again.",
    "But she still visted them from time to time.",
    "Every day he saw the result of his disobedience, and wept.",
    "Every year she put cherry blossoms on the graves of her children.",
    "He lived the rest of his life as a beggar... which was perfectly just.",
    "He picked up his weapon and went on his way.",
    "He saw the error of his ways and repented.",
    "Her sorrow came to an end and her joy began.",
    "His dedication had broken the spell.",
    "His wound was healed but his heart remained broken forever.",
    "In this way, she avoided the punishment she deserved.",
    "It fit perfectly.",
    "It is said that he will haunt that place until she forgives him.",
    "She always wore it to help remind her.",
    "She never let it out of her sight again.",
    "So everything was restored to its former glory.",
    "So he forgave her and they were married.",
    "So he knew that his visitor had been a monster all along.",
    "So he realized how loyal his brother had been.",
    "So he told her he was the Prince and they lived happily ever after.",
    "So it was transformed back into human form.",
    "So she revealed her true identity and they were married.",
    "So the King agreed to spare his life.",
    "So the King relented and the two were wed.",
    "So the Queen gave them the prize as she had promised.",
    "So the evil-doers wre thrown down a well.",
    "So the riddle was finally answered.",
    "So the rightful ruler was placed once more upon the throne.",
    "So the spell was broken and they were free.",
    "So the village was restored to prosperity.",
    "So they changed places and everything was back to normal.",
    "So they escaped their captors and fled home.",
    "So they promised never to fight again.",
    "So they returned it to its original owner.",
    "The King fulfilled his side of the bargain and everyone was happy.",
    "The curse was lifted as had been foretold.",
    "The farm was returned to its rightful owners.",
    "The monster was destroyed and the farm was safe once more.",
    "They ate it at the feast and it was delicious.",
    "They loooked after it until she was old enough.",
    "They thanked the hero who had saved them all.",
    "They were buried in the same grave, and the kingdom mourned them.",
    "This is the terrible fate that awaits those who commit murder.",
    "True love had broken the enchantment.",
    "When her father saw her babies, he realized he had to allow the marriage.",
    "Which is how the kingdom got its name.",
    "Which proves that a pure heart will always triumph in the end.",
    "Which proves that one should always be careful of one's companions.",
    "Which shows that a good deed will be rewarded in the end.",
    "With the ghost banished, their hardship ended.",
    "With the rival dead hey could get married at last.",
    "\"You have freed me from my enchantment and tomorrow we will be married.\""
  ]
};

/* probably bad for me to write to Array.prototype, but not sure the best way
   to disrupt in-place arrays
*/
Array.prototype.shuffle=function(){for(var t=[];this.length;)t.push(this.splice(Math.random()*this.length,1)[0]);for(;t.length;)this.push(t.pop());return this};
Array.prototype.rotate=function(t){if("undefined"==typeof t&&(t=1),t>0)for(;0!=t;)this.push(this.shift()),t--;else if(0>t)for(;0!=t;)this.unshift(this.pop()),t++;return this};
if(!Array.prototype.choice)
  Array.prototype.choice=function(){return this[Math.floor(Math.random()*this.length)];}
/* newer Javascript already has 'Array.isArray()' */
if(!Array.isArray) 
  Array.isArray = function(i){return Object.prototype.toString.call(i)==='[object Array]';}
function Madlibs(brain) {
  "use strict";
  /* brain: an object with at least '@' property */
  /* expected to look like this:
     { "@" : ["default_templates",],
       "default_templates": [ "The %aspect %person and the %(good|bad) %person.", ],
       "aspect" : [ "young", "old", "short", "tall" ],
       "person" : [ "man", "woman", "child", "bear" ]
     }
  */
  this.brain = brain;
  for(var i in brain){ 
    /* Object.keys(brain).forEach(function(k,i){ ... }) is better than for...in but needs Javascript 1.8.5 */
    if(brain.hasOwnProperty(i)) { 
      if(!Array.isArray(brain[i])) brain[i] = [brain[i],];
      /* causes '#' to become a list but I don't care */
      brain[i].shuffle();
    }
  }
  var _lookup = function(thing, brain, sanity) {
    // console.log("_lookup(\""+thing+"\", "+brain+","+sanity+");");
    if(thing.indexOf('|') > 0)
      thing = thing.split('|').choice();
    else if(typeof(brain[thing])!=='undefined') 
      // console.log(brain[thing]);
      // console.log(brain[thing].choice());
      thing = _story(brain[thing].choice(), brain, sanity)
    return thing;
  }
  this.story = function(frame) { return _story(frame, this.brain, 10); }
  var _story = function(frame, brain, sanity) {
    var answer,i,j;
    // console.log("_story(\""+frame+"\","+brain+","+sanity+");");
    sanity-=1;
    if(sanity < 0)
      throw "sanity depleted; loop detected in brain file?";
    if(typeof(frame)==='undefined')
      frame = brain[brain['@'].choice()].choice();
    answer = "";
    i = 0;
    j = -1;
    while(i<frame.length) {
      if(frame[i] == '%') {
        if(frame[i+1] == '%') {
          i=i+1;
          answer+='%';
        }
        else if(frame[i+1] == '(') {
          /* TODO: what if nested "%(foo|%(bar|baz)|quux)"  ? */
          j = frame.indexOf(')',i);
          if(i<j) {
            answer+=_lookup(frame.substr(i+2,j-i+1), brain, sanity);
            i=j;
          }
          else
            throw "unmatched %( : " + frame;
        }
        else if(frame[i+1] == '{') {
          /* TODO: what if nested "%{foo|%{bar|baz}|quux}"  ? */
          j = frame.indexOf('}',i);
          if(i<j) {
            answer+=_lookup(frame.substr(i+2,j-i+1), brain, sanity);
            i=j;
          }
          else
            throw "unmatched %{ : " + frame;
        }
        else {
          var match = frame.substr(i+1).match(/^[a-zA-Z0-9]+/);
          if(match) {
            /* %boogerHammer */
            answer += _lookup(match[0], brain, sanity);
            i+=match[0].length;
          }
          else
            /* %. */
            answer += '%';
        }
      }
      else {
        answer += frame[i];
      }
      i=i+1;
    }
    /* TODO: replace "a _argument_" with "an _argument_" before throwing back */
    return answer;
  }
}

if(typeof process === 'object') {
  /* I'm in Node */
  var madlibs = new Madlibs(once);
  console.log(madlibs.story())
}

