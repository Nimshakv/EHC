// Tooltips Initialization
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
  $( "#student_birthday" ).datepicker({ dateFormat: 'yy-mm-dd'});

//  $('#profile_image').change( function(e) {
//
//    var img = URL.createObjectURL(e.target.files[0]);
//    $('.prof_pic').attr('src', img);
//  });
//
//  $('#id_card').change( function(e) {
//
//    var img = URL.createObjectURL(e.target.files[0]);
//    $('#id_cd').attr('src', img);
//  });

})

// Steppers
$(document).ready(function () {
  var navListItems = $('div.setup-panel-2 div a'),
          allWells = $('.setup-content-2'),
          allNextBtn = $('.nextBtn-2'),
          allPrevBtn = $('.prevBtn-2');
  allWells.hide();

  navListItems.click(function (e) {
      e.preventDefault();
      var $target = $($(this).attr('href')),
              $item = $(this);

      if (!$item.hasClass('disabled')) {
          navListItems.removeClass('btn-amber').addClass('btn-blue-grey');
          $item.addClass('btn-amber');
          allWells.hide();
          $target.show();
          $target.find('input:eq(0)').focus();
      }
  });

  allPrevBtn.click(function(){
      var curStep = $(this).closest(".setup-content-2"),
          curStepBtn = curStep.attr("id"),
          prevStepSteps = $('div.setup-panel-2 div a[href="#' + curStepBtn + '"]').parent().prev().children("a");

          prevStepSteps.removeAttr('disabled').trigger('click');
  });

  allNextBtn.click(function(){
      var curStep = $(this).closest(".setup-content-2"),
          curStepBtn = curStep.attr("id"),
          nextStepSteps = $('div.setup-panel-2 div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
          curInputs = curStep.find("input[type='text'],input[type='url'],input[type='email'],input[type='tel'],input[type='date'],input[type='file']"),
          isValid = true;

      $(".form-group").removeClass("has-error");
      for(var i=0; i< curInputs.length; i++){
          if (!curInputs[i].validity.valid){
              isValid = false;
              $(curInputs[i]).closest(".form-group").addClass("has-error");
          }
      }

      if (isValid)
          nextStepSteps.removeAttr('disabled').trigger('click');
  });

  $('div.setup-panel-2 div a.btn-amber').trigger('click');

  $(function(){
    $('#profile_image').change( function(e) {

        var img = URL.createObjectURL(e.target.files[0]);
        $('.prof_pic').attr('src', img);

    });

  });

  function submitForm(){
    alert("hi");
    document.getElementById('st_det').submit();
  }
});