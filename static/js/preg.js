$(document).ready(function () {
    console.log("hi");
    var psubmit = $('#psubmit');
    var pcancel = $('#pcancel');
    var list = $('.camp_btn');
    var child_sp = $('.sp-child > button');

    psubmit.click(function(){
        var parent_div = $(this).closest('div');
        var form = $(this).closest('form')
        curInputs = parent_div.find("input[type='text'],input[type='url'],input[type='email'],input[type='tel'],input[type='date'],input[type='file']"),
        isValid = true;

        $(".form-group").removeClass("has-error");
        for(var i=0; i< curInputs.length; i++){
            if (!curInputs[i].validity.valid){
                isValid = false;
                $(curInputs[i]).closest(".form-group").addClass("has-error");
            }
        }
        if(!isValid){
            return false;
        }
        return true;

    });

    pcancel.click(function(){
        window.location = '/home';
    });

    list.click(function(){
        var parent_div = $(this).closest('div');
        var camp = $(this)[0].innerHTML;
        var selected_camp = parent_div.find('input[type=hidden]');
        selected_camp.attr("value", camp);
        return true;
    });

    child_sp.click(function(){
        console.log($(this).closest('div'));
        var div = $(this).closest('div')
        var hidden = div.find('input[type=hidden]');
        if (hidden[0].getAttribute("value") != 0 || hidden[0].getAttribute("value") != ""){
            $('#child_id').val(hidden[0].getAttribute("value"));
            return true;
        }

        return false;
    });

});
