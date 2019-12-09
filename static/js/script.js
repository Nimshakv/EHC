$(document).ready(function(){

  $('.input').focus(function(){
    $(this).parent().find(".label-txt").addClass('label-active');
  });

  $(".input").focusout(function(){
    if ($(this).val() == '') {
      $(this).parent().find(".label-txt").removeClass('label-active');
    };
  });

  $(".user_select").each(function(){
    var btn = this;
    btn.addEventListener("click", set_val, false);
  });

  $(".lg_user_select").each(function(){
    var btn = this;
    btn.addEventListener("click", lg_set_val, false);
  });
//   document.getElementsByClassName("user_select").addEventListener("click", set_val, false);

});

function set_val(){
    var parent = this.parentElement;
    parent.style.display = "None";
    $("#su").css("display", "block");
    console.log($(this).val());
    $("#user_type").val($(this).val());

}

function lg_set_val(){
    var parent = this.parentElement;
    parent.style.display = "None";
    $("#lg").css("display", "block");
    console.log($(this).val());
    $("#lg_user_type").val($(this).val());

}