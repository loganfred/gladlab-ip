// global variables for tracking state
var PATHS = [];
var PROPERTIES;
var FCANVAS;

// initialize the canvas with global scope
//var canvas = $('#viewer');
//var context = canvas[0].getContext('2d');
/* canvas scroll fix
var canvas_dom = $('#viewer')[0];
canvas_dom.addEventListener("touchstart",  function(event) {event.preventDefault()});
canvas_dom.addEventListener("touchmove",   function(event) {event.preventDefault()});
canvas_dom.addEventListener("touchend",    function(event) {event.preventDefault()});
canvas_dom.addEventListener("touchcancel", function(event) {event.preventDefault()});
*/

var options = {}
var hyphae = new Image();
var canvas = new fabric.Canvas('viewer', options);

function onHyphaePick(b64_hyphae, onPathClose) {
    hyphae.src = 'data:image/png;base64,' + b64_hyphae;
    hyphae.onload = () => {
        let imgInstance = new fabric.Image(hyphae)
        canvas.clear();
        canvas.setBackgroundImage(imgInstance, canvas.renderAll.bind(canvas));
        onDrawStart();
        canvas.on('path:created', (d) => onPathClose(d));
    }
}

function onDrawStart() {
    canvas.isDrawingMode = true;
    canvas.allowTouchScrolling = false;
    canvas.freeDrawingBrush.color = 'yellow';
    canvas.freeDrawingBrush.width = 4;
}

function onPathClose(options) {

    let path = options.path;
    let obj = {path:path, ...PROPERTIES}

    PATHS.push(obj)
    console.log(obj);
    console.log(`PATHS array length is now ${PATHS.length}`);
}


// update the canvas with the correct image and make metadata table
$("#imageform").submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function(data)
        {
            // append to metadata table
            $("#prop_name").text(data.file)

            $('#table').empty()

            let header = '';
            header += '<thead>'
            header += '<tr>'
            header += '<th>key</th>'
            header += '<th>value</th>'
            header += '</tr>'
            header += '</thead>'

            $('#table').append(header);
            $('#metadata-title').show()

            makeRow(data, $('#table'));

            // append to internal serialization construct
            PROPERTIES = data;

            // execute the canvas updates
            onHyphaePick(data.image, onPathClose)
        }
    });
});



// clear button should wipe the canvas, re-initialize the canvas, and clear out
// any paths present in the serialization construct
$('#clear').click( () => {
    canvas.clear();
    let imgInstance = new fabric.Image(hyphae)
    canvas.setBackgroundImage(imgInstance, canvas.renderAll.bind(canvas));
    PATHS = PATHS.filter( (o) => { return o.file !== PROPERTIES.file });
});


// dump JSON of activity
// https://stackoverflow.com/questions/19721439/download-json-object-as-a-file-from-browser
function downloadObjectAsJson(exportObj, exportName){
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href",     dataStr);
    downloadAnchorNode.setAttribute("download", exportName + ".json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}

// export button should download the serialization construct as a json file
$('#export').click( () => {
    downloadObjectAsJson(PATHS, 'export');
});


//------------------ MISC ---------------------

// MODAL BEGIN

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// MODAL END


// check the first radio button
// https://stackoverflow.com/questions/3977699/check-first-radio-button-with-jquery
$("input:radio[name=file]:first").click();


// this function exists to make the metadata table from nested json
function makeRow(data, table, prefix) {

  $.each(data, function (key, val) {

      prefix = (typeof prefix === 'undefined') ? '' : prefix;

      if (key == 'image') {
          return; // equivalent of continue in $.each()
      }
      if (typeof val == 'object') {
        makeRow(val, table, `${prefix}${key}>`);
        return;
      }
      let chunk = '';
      chunk += '<tr>';
      chunk += '<td>' + prefix + key + '</td>';
      chunk += '<td>' + val + '</td>';
      chunk += '</tr>';
      table.append(chunk);
  });
}
