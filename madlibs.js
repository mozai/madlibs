'use strict';

/* probably bad for me to write to Array.prototype, but not sure the best way
   to disrupt in-place arrays
*/
Array.prototype.shuffle=function(){var i,j,k;for(i=this.length-1;i;i--){j=Math.floor(Math.random()*(i+1));k=this[i];this[i]=this[j];this[j]=k;}return this;}
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
    if(thing.indexOf('|') > 0)
      thing = thing.split('|').choice();
    else if(typeof(brain[thing])!=='undefined')
      thing = _story(brain[thing].choice(), brain, sanity)
    return thing;
  }
  this.story = function(frame) { return _story(frame, this.brain, 10); }
  var _story = function(frame, brain, sanity) {
    var answer,i,j;
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
            answer+=_lookup(frame.substr(i+2,j-i-2), brain, sanity);
            i=j;
          }
          else
            throw "unmatched %( : " + frame;
        }
        else if(frame[i+1] == '{') {
          /* TODO: what if nested "%{foo|%{bar|baz}|quux}"  ? */
          j = frame.indexOf('}',i);
          if(i<j) {
            answer+=_lookup(frame.substr(i+2,j-i-2), brain, sanity);
            i=j;
          }
          else
            throw "unmatched %{ : " + frame;
        }
        else {
          var match = frame.substr(i+1).match(/^[a-zA-Z0-9_]+/);
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
