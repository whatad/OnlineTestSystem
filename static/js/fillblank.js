$(document).ready(function(){
    $("#question_jump").click(function () {
        location.href = '/exam/fillblank?no='+parseInt($('#question_id').val());
    });

    $('#pre_ques').attr('href', '/exam/fillblank?no='+(parseInt($('#question_id').val())-1));
    $('#next_ques').attr('href', '/exam/fillblank?no='+(parseInt($('#question_id').val())+1));

    $('#pre_stu').attr('href', '/exam/fillblank?no='+$('#question_id').val()+'&&answer='+(parseInt($('#answer_no').val())-1));
    $('#next_stu').attr('href', '/exam/fillblank?no='+$('#question_id').val()+'&&answer='+(parseInt($('#answer_no').val())+1));

    $("#question_btn").click(function(){
        if($(this).text()=="修改"){
            $("#level_select").removeAttr('disabled');
            $(this).text('确认');
        }
        else{
            $.post("/exam/updateQuestion/",
                {
                    question_id: $('#question_id').val(),
                    level_name: $("#level_select").find("option:selected").text(),
                    level: $("#level_select").val()
                },
                function(data,status){
                    if(status == 'success'){
                        $("#level_select").find("option[text="+data['level']+"]").attr("selected",true);
                        $("#level_select").attr("disabled", true);
                        $("#question_btn").text("修改");
                    }
                }
            );
        }
    });

    $("#answer_btn").click(function(){
        if($(this).text()=="修改"){
            $("#answer").attr('contenteditable', true);
            $(this).text('确认');
        }
        else{
            $.post("/exam/updateAnswer/",
                {
                    question_id: $('#question_id').val(),
                    answer: $("#answer").text(),
                },
                function(data,status){
                    if(status == 'success'){
                        $("#answer").text(data['answer']);
                        $("#answer").attr('contenteditable', false);
                        $("#answer_btn").text("修改");
                    }
                }
            );
        }
    });

    $('.point_btn').click(function () {
        var index = $('.point_btn').index(this);
        if($(this).text()=="修改") {
            $('.space').eq(index).find('.d_key').each(function () {
                $(this).attr('contenteditable', true);
            });
            $('.space').eq(index).find('.d_value').each(function () {
                $(this).attr('contenteditable', true);
            });
            $('.space').eq(index).find('.close_btn').each(function () {
                $(this).removeClass('d-none');
            });
            $('.space').eq(index).find('.add_btn').each(function () {
                $(this).removeClass('d-none');
            });
            $('.mode_selector').eq(index).removeAttr('disabled');
            $(this).text("确认");
        }
        else{
            var point_list = new Array();
            $('.space').eq(index).find('.line').each(function () {
                //var dict = new Array();
                let dict= Object.create(null);
                $(this).find('.point').each(function () {
                    dict[$(this).find('.d_key').text().trim()] = $(this).find('.d_value').text().trim()
                });
                point_list.push(JSON.stringify(dict));
            });
            $.post("/exam/updatePoints",{
                question_id: $('#question_id').val(),
                space: index+1,
                points: JSON.stringify(point_list),
                mode: $('.mode_selector').eq(index).val()
            },function (data, status) {
                if(status == 'success'){
                    $('.space').eq(index).find('.close_btn').each(function () {
                        $(this).addClass('d-none');
                    });
                    $('.space').eq(index).find('.add_btn').each(function () {
                        $(this).addClass('d-none');
                    });
                    $('.space').eq(index).find('.d_key').each(function () {
                        $(this).attr('contenteditable', false);
                    });
                    $('.space').eq(index).find('.d_value').each(function () {
                        $(this).attr('contenteditable', false);
                    });
                    $('.mode_selector').eq(index).attr("disabled", true);
                    $('.point_btn').eq(index).text("修改");
                }
            });

        }
    });

    $(document).on('click','.close_btn',function (){
        $(this).parent().remove();
    });

    $('.add_btn').click(function () {
        var new_word = "<div class=\"d-inline-flex point\">" +
                            "<div class=\"border p-1 d_key\" contenteditable=\"true\">&emsp;</div>" +
                            "<div class=\"border p-1 d_value\" contenteditable=\"true\">&emsp;</div>" +
                            "<button type=\"button\" class=\"btn btn-outline-danger p-1 close_btn\" aria-label=\"Close\">&times;</button>" +
                        "</div>";
        $(this).parents('.line').find('.add_div').before(new_word);
    });

    $('.score_btn').click(function () {
        var index = $('.score_btn').index(this);
        if($(this).text() == "修改"){
            $('.score_input').eq(index).removeAttr("disabled");
            $(this).text('确认');
        }
        else{
            var totalScore = 0;
            $('.score_input').each(function () {
                totalScore = totalScore + parseFloat($(this).val()) * parseFloat($('.score').eq($('.score_input').index(this)).text()) * 0.01;
            });
            $.post("/exam/updateScore/",
                {
                    answer_id: $('#answer_id').val(),
                    totalScore: totalScore
                },
                function(data,status){
                    if(status == 'success'){
                        $('.score_input').eq(index).attr("disabled", true);
                        $('.score_btn').eq(index).text('修改');
                        $('#total').text(totalScore);
                    }
                }
            );
        }
    });
});