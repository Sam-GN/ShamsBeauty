
$(document).ready(function() {

$('#sessionModelSave').on('click', function(e) {
  var str = window.location.pathname;
  var sessionID = str.substring(str.lastIndexOf("%2C")+3);
  var canvas =document.getElementById("paintCanvas") ;
  var cx = canvas.getContext('2d');
    $.ajax({
      url: '/session_update_model?sessionID=' + sessionID+'&modelString='+cx.canvas.toDataURL(),
      type: 'PUT',
      success: function(data) {
     $("#paintModal").modal('hide');
        //alert(cx.canvas.toDataURL())
         location.reload();
    }
    });
});


   var canvas =document.getElementById("sessionCanvas") ;
   if(canvas){
        var str = window.location.pathname;
        var sessionID = str.substring(str.lastIndexOf("%2C")+3);
        if(sessionID==='-1'){
         var imageModal=document.getElementById("open-paint_image_id") ;
         imageModal.disabled=true;
        } else{
        $.ajax({
          url: '/session_get_model?sessionID=' + sessionID ,
          type: 'GET',
          success: function(data) {
             var cx = canvas.getContext('2d');
           var image = new Image();
            image.onload = function() {
              //cx.drawImage(image, 0, 0);
              cx.drawImage(image, 0, 0, 480,    480,     // source rectangle
                   -5, 0, 240, 240); // destination rectangle
            };
            //alert(data)
            image.src = data.replaceAll(' ','+');
              }
        });
        }


    }
$(document).on("click", ".open-paint_image", function () {
     var file = $(this).data('file');
     $(".modal-body .picturepanel").css({"background-image": 'url('+file+')','background-repeat': 'no-repeat'});
     $(".modal-body .picturepanel").css("background-position", 'center');

});

$(document).on("click", "#deleteSession", function () {
     var str = window.location.pathname;
     var sessionID = str.substring(str.lastIndexOf("%2C")+3);
      $(".modal-footer #deleteSessionConfirm").data('file',sessionID);
});

$('#deleteSessionConfirm').on('click', function(e) {
$.ajax({
  url: '/delete_session?sessionID=' + $(".modal-footer #deleteSessionConfirm").data('file'),
  type: 'DELETE',
  success: function(data) {
     $("#deleteSessionModal").modal('hide');
    window.location.replace(data);
  }
});
});

$(document).on("click", "#deletePatient", function () {
     var str = window.location.pathname;
     var patientID = str.substring(str.lastIndexOf("/")+1);
      $(".modal-footer #deletePatientConfirm").data('file',patientID);
});

$('#deletePatientConfirm').on('click', function(e) {
$.ajax({
  url: '/delete_patient?patientID=' + $(".modal-footer #deletePatientConfirm").data('file'),
  type: 'DELETE',
  success: function(data) {
     $("#deletePatientModal").modal('hide');
    window.location.replace(data);
  }
});
});


$(document).on("click", ".open-modal_image", function () {
     var file = $(this).data('file');
     $(".modal-body #modal_image").attr("src", file);
});

$(document).on("click", ".deleteUser", function () {
     var username = $(this).data('username');
    $(".modal-footer #deleteUserConfirm").data('username',username);
});

$('#deleteUserConfirm').on('click', function(e) {
    $.ajax({
      url: '/user/remove_user?username=' + $(".modal-footer #deleteUserConfirm").data('username'),
      type: 'PUT',
      success: function(data) {
     $("#deleteUserModal").modal('hide');
        window.location.replace(data);
    }
    });
});


  $('#deletePic').on('click', function(e) {
    $.getJSON('/delete_pic?filename=' + $('.modal-body #modal_image').attr('src').replaceAll('/','%2F'),
        function(data) {
      //do nothing

    });
    $("#pictureModal").modal('hide');
    $("#pictureModalDelete").modal('hide');
    location.reload();
    return false;
  });


$('nav a').click(function() {
<!--  alert( "Handler for .click() called." );-->
  window.name="";
  $("#search").val( '') ;
});
console.log(window.name);
 $("#search").val( window.name) ;
// save value on navigation out
  window.onbeforeunload = function() {
  if(window.location.href.includes('_list')){
    window.name = $("#search").val();
    return;
    }
  }

   if(window.location.href.endsWith('_list'))
        if($("#search").val())
              search($("#search").val());
   $("#date").kendoDatePicker();
   $("#nextDate").kendoDatePicker();
   $(".k-datepicker").css({"background-color": "transparent", "width": "100%"});
   $("ul#sessions").css("height", "100%");
   $("ul#users").css("height", "100%");
   $('#search').on("input", function(e) {
      var input = $(this);
      var val = input.val();
      if (input.data("lastval") != val) {
        input.data("lastval", val);
        search(val);
      }
    });

});
function updateLevel(username){

  $.ajax({
      url: '/user/update_level?username='+username+'&level='+$('#input_'+username).val(),
      type: 'PUT',
      success: function(data) {
      }
});



}

$("#input_admin").prop('disabled', true);
$("#deleteUser_admin").prop('disabled', true);

function search(val){
 var myUrl = "/patient";
        if(window.location.href.includes('session'))
            myUrl = "/session";
         myUrl = myUrl + "_list_ajax?search=" + val;
         $.ajax({
            dataType : "html",
            contentType: "application/x-www-form-urlencoded; charset=UTF-8", // this is the default value, so it's optional
            url: myUrl,
            success : function(result) {
                $("#myDiv").html(result);
            },
        });
}
