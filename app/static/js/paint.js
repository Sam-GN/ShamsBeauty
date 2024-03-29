/************************************************************************
 *
 * Eloquent JavaScript
 * by Marijn Haverbeke
 *
 * Chapter 19
 * Project: A Paint Program
 *
 * Just so you know, most of this code is Marijn's, comments are mine.
 * This exercise is meant to be a fun way of exploring how JavaScript can
 * interact with form elements while reviewing previous material in the
 * book. If you want to learn how to program with JavaScript, I sincerely
 * hope you check his book out. It's free online:
 *
 * http://eloquentjavascript.net/
 *
 * but I suggest buying it and marking it all up with your own notes
 * and thoughts.
 *
 * Now, TO THE CODE!!!
 *
 * Ryan Boone
 * falldowngoboone@gmail.com
 *
 ***********************************************************************/

// the core of the program; appends the paint interface to the
// DOM element given as an argument (parent)
function createPaint(parent) {
  var canvas = elt('canvas', {width: 480, height: 480, id:'paintCanvas'});
  var cx = canvas.getContext('2d');

     var str = window.location.pathname;
        var sessionID = str.substring(str.lastIndexOf("%2C")+3);

     $.ajax({
          url: '/session_get_model?sessionID=' + sessionID ,
          type: 'GET',
          success: function(data) {
             var image = new Image();
                image.onload = function() {
                  cx.drawImage(image, 0, 0);
                };
                if(sessionID!='-1')
                    image.src = data.replaceAll(' ','+');
                //console.log(data);
              }
        });

  var toolbar = elt('div', {class: 'toolbar center'});

  // calls the every function in controls, passing in context,
  // then appending the returned results to the toolbar
  for (var name in controls)
    toolbar.appendChild(controls[name](cx));

  var panel = elt('div', {class: 'picturepanel'}, canvas);
  parent.appendChild(elt('div', null, panel, toolbar));

  cx.lineWidth = 3;
}

/************************************************************************
 * helper functions
 ***********************************************************************/

// creates an element with a name and object (attributes)
// appends all further arguments it gets as child nodes
// string arguments create text nodes
// ex: elt('div', {class: 'foo'}, 'Hello, world!');
function elt(name, attributes) {
  var node = document.createElement(name);
  if (attributes) {
    for (var attr in attributes)
      if (attributes.hasOwnProperty(attr))
        node.setAttribute(attr, attributes[attr]);
  }
  for (var i = 2; i < arguments.length; i++) {
    var child = arguments[i];

    // if this argument is a string, create a text node
    if (typeof child == 'string')
      child = document.createTextNode(child);


    node.appendChild(child);
  }
  return node;
}

// figures out canvas relative coordinates for accurate functionality
function relativePos(event, element) {
  var rect = element.getBoundingClientRect();
  return {x: Math.floor(event.clientX - rect.left),
          y: Math.floor(event.clientY - rect.top)};
}

// registers and unregisters listeners for tools
function trackDrag(onMove, onEnd) {
  function end(event) {
    removeEventListener('mousemove', onMove);
    removeEventListener('mouseup', end);
    if (onEnd)
      onEnd(event);
  }
  addEventListener('mousemove', onMove);
  addEventListener('mouseup', end);
}

// loads an image from a URL and replaces the contents of the canvas
//function loadImageURL(cx, url)  {
//  var image = document.createElement('img');
//  image.addEventListener('load', function() {
//    var color = cx.fillStyle, size = cx.lineWidth;
//    cx.canvas.width = image.width;
//    cx.canvas.height = image.height;
//    cx.drawImage(image, 0, 0);
//    cx.fillStyle = color;
//    cx.strokeStyle = color;
//    cx.lineWidth = size;
//  });
//  image.src = url;
//}

// used by tools.Spray
// randomly positions dots
//function randomPointInRadius(radius) {
//  for (;;) {
//    var x = Math.random() * 2 - 1;
//    var y = Math.random() * 2 - 1;
//    // uses the Pythagorean theorem to test if a point is inside a circle
//    if (x * x + y * y <= 1)
//      return {x: x * radius, y: y * radius};
//  }
//}

/************************************************************************
 * controls
 ***********************************************************************/

// holds static methods to initialize the various controls;
// Object.create() is used to create a truly empty object
var controls = Object.create(null);


controls.tool = function(cx) {
  var select = elt('select');
  var mode = 'Line';
  var btnPencil = elt('button', {style:'width:30px;height:30px;margin:2px;', id:'btnPencil'});

    btnPencil.addEventListener('click', function() {
    cx.lineWidth=3;
   mode = 'Line';

  });
  var i = elt('i', {class:'fa fa-pencil'});
  btnPencil.appendChild(i);
  var btnEraser = elt('button', {style:'width:30px;height:30px;margin:2px;', id:'btnEraser'});
    btnEraser.addEventListener('click', function() {
    cx.lineWidth = 14;
    mode = 'Erase';
  });
 var i2 = elt('i', {class:'fa fa-eraser'});
  btnEraser.appendChild(i2);
  // populate the tools
  for (var name in tools)
    select.appendChild(elt('option', null, name));

  // calls the particular method associated with the current tool
  cx.canvas.addEventListener('mousedown', function(event) {

    // is the left mouse button being pressed?
    if (event.which == 1) {

      // the event needs to be passed to the method to determine
      // what the mouse is doing and where it is
      tools[mode](event, cx);
      // don't select when user is clicking and dragging
      event.preventDefault();
    }
  });

  return elt('span', null, btnPencil,btnEraser);
};

controls.buttons = function(cx) {



var btn2 = elt('button', {style:'width:30px;height:30px;background-color:black;margin:2px;'});
    btn2.addEventListener('click', function() {
    cx.fillStyle = '#000000';
    cx.strokeStyle = '#000000';
  });
  var btn = elt('button', {style:'width:30px;height:30px;background-color:red;margin:2px;'});
    btn.addEventListener('click', function() {
    cx.fillStyle = '#FF0000';
    cx.strokeStyle = '#FF0000';
  });

  var btn3 = elt('button', {style:'width:30px;height:30px;background-color:blue;margin:2px;'});
    btn3.addEventListener('click', function() {
    cx.fillStyle = '#0000FF';
    cx.strokeStyle = '#0000FF';
  });
  var btn4 = elt('button', {style:'width:30px;height:30px;background-color:green;margin:2px;'});
    btn4.addEventListener('click', function() {
    cx.fillStyle = '#006400';
    cx.strokeStyle = '#006400';
  });
  var btn5 = elt('button', {style:'width:30px;height:30px;background-color:#C80080;margin:2px;'});
    btn5.addEventListener('click', function() {
    cx.fillStyle = '#C80080';
    cx.strokeStyle = '#C80080';
  });
  var i = elt('i',{class:'fa'});
  btn.appendChild(i);
   var i2 = elt('i',{class:'fa'});
  btn2.appendChild(i2);
   var i3 = elt('i',{class:'fa'});
   btn3.appendChild(i3);
    var i4 = elt('i',{class:'fa'});
    btn4.appendChild(i4);
    var i5 = elt('i',{class:'fa'});
    btn5.appendChild(i5);

  return elt('span', null, btn2,btn,btn3,btn4,btn5);
};



// color module
//controls.color = function(cx) {
//  var input = elt('input', {type: 'color'});
//
//  // on change, set the new color style for fill and stroke
//  input.addEventListener('change', function() {
//    cx.fillStyle = input.value;
//    cx.strokeStyle = input.value;
//  });
//  return elt('span', null, 'Color: ', input);
//};

// brush size module
//controls.brushSize = function(cx) {
//  var select = elt('select');
//
//  // various brush sizes
//  //var sizes = [1, 2, 3, 5, 8, 12, 25, 35, 50, 75, 100];
//  var sizes = [3,14];
//
//  // build up a select group of size options
//  sizes.forEach(function(size) {
//    select.appendChild(elt('option', {value: size}, size + ' pixels'));
//  });
//
//  // on change, set the new stroke thickness
//  select.addEventListener('change', function() {
//    cx.lineWidth = select.value;
//  });
//  return elt('span', null, 'Brush size: ', select);
//};

// save
//controls.save = function(cx) {
//  // MUST open in a new window because of iframe security stuff
//  var link = elt('a', {href: '/', target: '_blank'}, 'Save');
//  function update() {
//    try {
//      link.href = cx.canvas.toDataURL();
//    } catch(e) {
//      // some browsers choke on big data URLs
//
//      // also, if the server response doesn't include a header that tells the browser it
//      // can be used on other domains, the script won't be able to look at it;
//      // this is in order to prevent private information from leaking to a script;
//      // pixel data, data URL or otherwise, cannot be extracted from a "tainted canvas"
//      // and a SecurityError is thrown
//      if (e instanceof SecurityError)
//        link.href = 'javascript:alert(' +
//          JSON.stringify('Can\'t save: ' + e.toString()) + ')';
//      else
//        window.alert("Nope.");
//        throw e;
//    }
//  }
//  link.addEventListener('mouseover', update);
//  link.addEventListener('focus', update);
//  return link;
//};

// open a file
//controls.openFile = function(cx) {
//  var input = elt('input', {type: 'file'});
//  input.addEventListener('change', function() {
//    if (input.files.length == 0) return;
//    var reader = new FileReader();
//    reader.addEventListener('load', function() {
//      loadImageURL(cx, reader.result);
//    });
//    reader.readAsDataURL(input.files[0]);
//  });
//  return elt('div', null, 'Open file: ', input);
//};
/*

// open a URL
controls.openURL = function(cx) {
  var input = elt('input', {type: 'text'});
  var form = elt('form', null, 'Open URL: ', input,
                 elt('button', {type: 'submit'}, 'load'));
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    loadImageURL(cx, form.querySelector('input').value);
  });
  return form;
};
*/

/************************************************************************
 * tools
 ***********************************************************************/

// drawing tools
var tools = Object.create(null);

// line tool
// onEnd is for the erase function, which uses it to reset
	// the globalCompositeOperation to source-over
tools.Line = function(event, cx, onEnd) {
  cx.lineCap = 'round';

  // mouse position relative to the canvas
  var pos = relativePos(event, cx.canvas);
  trackDrag(function(event) {
    cx.beginPath();

    // move to current mouse position
    cx.moveTo(pos.x, pos.y);

    // update mouse position
    pos = relativePos(event, cx.canvas);

    // line to updated mouse position
    cx.lineTo(pos.x, pos.y);

    // stroke the line
    cx.stroke();
  }, onEnd);
};

// erase tool
tools.Erase = function(event, cx) {

  // globalCompositeOperation determines how drawing operations
  // on a canvas affect what's already there
  // 'destination-out' makes pixels transparent, 'erasing' them
  // NOTE: this has been deprecated
  cx.globalCompositeOperation = 'destination-out';
  tools.Line(event, cx, function() {
    cx.globalCompositeOperation = 'source-over';
  });
};

// text tool
//tools.Text = function(event, cx) {
//  var text = prompt('Text:', '');
//  if (text) {
//    var pos = relativePos(event, cx.canvas);
//    // for simplicity, text size is brush size, locked to sans-serif
//    cx.font = Math.max(7, cx.lineWidth) + 'px sans-serif';
//    cx.fillText(text, pos.x, pos.y);
//  }
//}

// spray paint tool
//tools.Spray = function(event, cx) {
//  var radius = cx.lineWidth / 2;
//  var area = radius * radius * Math.PI;
//  var dotsPerTick = Math.ceil(area / 30);
//
//  var currentPos = relativePos(event, cx.canvas);
//  var spray = setInterval(function() {
//    for (var i = 0; i < dotsPerTick; i++) {
//      var offset = randomPointInRadius(radius);
//      cx.fillRect(currentPos.x + offset.x,
//                  currentPos.y + offset.y, 1, 1);
//    }
//  }, 25);
//  trackDrag(function(event) {
//    currentPos = relativePos(event, cx.canvas);
//  }, function() {
//    clearInterval(spray);
//  });
//};

/************************************************************************
 * exercises
 ***********************************************************************/

/**
 * allows the user to click and drag out a rectangle on the canvas
 *
 * @param {Object} event - mousedown event (specifically left button)
 * @param {Object} cx - the canvas 2d context object
 */
//tools.Rectangle = function(event, cx) {
//  var leftX, rightX, topY, bottomY
//  var clientX = event.clientX,
//      clientY = event.clientY;
//
//  // placeholder rectangle
//  var placeholder = elt('div', {class: 'placeholder'});
//
//  // cache the relative position of mouse x and y on canvas
//  var initialPos = relativePos(event, cx.canvas);
//
//  // used for determining correct placeholder position
//  var xOffset = clientX - initialPos.x,
//      yOffset = clientY - initialPos.y;
//
//  trackDrag(function(event) {
//    document.body.appendChild(placeholder);
//
//    var currentPos = relativePos(event, cx.canvas);
//    var startX = initialPos.x,
//        startY = initialPos.y;
//
//    // assign leftX, rightX, topY and bottomY
//    if (startX < currentPos.x) {
//      leftX = startX;
//      rightX = currentPos.x;
//    } else {
//      leftX = currentPos.x;
//      rightX = startX;
//    }
//
//    if (startY < currentPos.y) {
//      topY = startY;
//      bottomY = currentPos.y;
//    } else {
//      topY = currentPos.y;
//      bottomY = startY;
//    }
//
//  	// set the style to reflect current fill
//    placeholder.style.background = cx.fillStyle;
//
//  	// set div.style.left to leftX, width to rightX - leftX
//    placeholder.style.left = leftX + xOffset + 'px';
//    placeholder.style.top = topY + yOffset + 'px';
//    placeholder.style.width = rightX - leftX + 'px';
//    placeholder.style.height = bottomY - topY + 'px';
//  }, function() {
//
//    // add rectangle to canvas with leftX, rightX, topY and bottomY
//    cx.fillRect(leftX, topY, rightX - leftX, bottomY - topY);
//
//  	// destroy placeholder
//    document.body.removeChild(placeholder);
//  });
//};

/**
 * allows the user to load the color of a specific pixel
 *
 * @param {Object} event - mousedown event (specifically left button)
 * @param {Object} cx - the canvas 2d context object
 */
// TODO: rewrite with pixel object
//tools['Pick Color'] = function(event, cx) {
//  try {
//    var colorPos = relativePos(event, cx.canvas),
//        // returns an array [r, g, b, opacity];
//        imageData = cx.getImageData(colorPos.x, colorPos.y, 1, 1),
//        colorVals = imageData.data,
//        color = '';
//
//    // build the color
//    color += 'rgb(';
//
//    // only need first three args
//    for (var i = 0; i < colorVals.length - 1; i++) {
//      color += colorVals[i];
//
//      // only need two commas
//      if (i < 2)
//        color += ',';
//    }
//    color += ')';
//
//    cx.fillStyle = color;
//    cx.strokeStyle = color;
//
//  } catch(e) {
//    if (e instanceof SecurityError)
//        alert('Whoops! Looks like you don\'t have permission to do that!');
//      else
//        throw e;
//  }
//};

// helpers for flood fill

// iterates over N, S, E and W neighbors and performs a function fn
//function forEachNeighbor(point, fn) {
//  fn({x: point.x - 1, y: point.y});
//  fn({x: point.x + 1, y: point.y});
//  fn({x: point.x, y: point.y - 1});
//  fn({x: point.x, y: point.y + 1});
//}
//
//// checks if 2 points in data, point1 and point2, have the same color
//function isSameColor(data, point1, point2) {
//  var offset1 = (point1.x + point1.y * data.width) * 4;
//  var offset2 = (point2.x + point2.y * data.width) * 4;
//
//  for (var i = 0; i < 4; i++) {
//    if (data.data[offset1 + i] != data.data[offset2 + i]) {
//      return false;
//    }
//  }
//  return true;
//}

// end flood fill helpers

// NOTE: in my first attempt, I was creating Pixel objects and pushing them
// to isPainted instead of Booleans; that wasn't a great idea...
// I suspect there was too much initialization for the browser to handle
// and it choked fatally :(

// I think I would still like to see this done with a Pixel object, if not
// merely for the ability to extend it to done some more advanced things

/**
 * paints all adjacent matching pixels
 */
//tools["Flood Fill"] = function(event, cx) {
//  var imageData = cx.getImageData(0, 0, cx.canvas.width, cx.canvas.height),
//      // get sample point at current position, {x: int, y: int}
//  		sample = relativePos(event, cx.canvas),
//      isPainted = new Array(imageData.width * imageData.height),
//      toPaint = [sample];
//
//  // while toPaint.length > 0
//  while(toPaint.length) {
//    // current point to check
//    var current = toPaint.pop(),
//        id = current.x + current.y * imageData.width;
//
//    // check if current has already been painted
//    if (isPainted[id]) continue;
//    else {
//
//      // if it hasn't, paint current and set isPainted to true
//      cx.fillRect(current.x, current.y, 1, 1);
//      isPainted[id] = true;
//    }
//
//    // for every neighbor (new function)
//    forEachNeighbor(current, function(neighbor) {
//      if (neighbor.x >= 0 && neighbor.x < imageData.width &&
//          neighbor.y >= 0 && neighbor.y < imageData.height &&
//          isSameColor(imageData, sample, neighbor)) {
//        toPaint.push(neighbor);
//      }
//    });
//  }
//};

// initialize the app
var appDiv = document.querySelector('#paint-app');
if(appDiv){
    createPaint(appDiv);
}


/************************************************************************
 * resources
 *
 * Canvas Rendering Context 2D API
 * https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D
 *
 * Eloquent JavaScript Ch 19, Project: A Paint Program
 * http://eloquentjavascript.net/19_paint.html
 ***********************************************************************/
