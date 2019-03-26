$(document).ready(function(){
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

    $('.branch_btn').click(function () {
        var index = $('.branch_btn').index(this);
        if($(this).text()=="修改") {
            $('.branch').eq(index).find('.d_key').each(function () {
                $(this).attr('contenteditable', true);
            });
            $('.branch').eq(index).find('.d_value').each(function () {
                $(this).attr('contenteditable', true);
            });
            $('.branch').eq(index).find('.close_btn').each(function () {
                $(this).removeClass('d-none');
            });
            $('.branch').eq(index).find('.add_btn').each(function () {
                $(this).removeClass('d-none');
            });
            $(this).text("确认");
        }
        else{
            let train_dict= Object.create(null);
            $('.branch').eq(index).find('.line').each(function () {
                train_dict[$(this).find('.d_key').text().trim()] = $(this).find('.d_value').text().trim();
            });
            $.post("/exam/updateBranch",{
                question_id: $('#question_id').val(),
                branch: index+1,
                trains: JSON.stringify(train_dict)
            },function (data, status) {
                if(status == 'success'){
                    $('.branch').eq(index).find('.close_btn').each(function () {
                        $(this).addClass('d-none');
                    });
                    $('.branch').eq(index).find('.add_btn').each(function () {
                        $(this).addClass('d-none');
                    });
                    $('.branch').eq(index).find('.d_key').each(function () {
                        $(this).attr('contenteditable', false);
                    });
                    $('.branch').eq(index).find('.d_value').each(function () {
                        $(this).attr('contenteditable', false);
                    });
                    $('.branch_btn').eq(index).text("修改");
                }
            });

        }
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

    $("#question_jump").attr('href', '/exam/shortAnswer?no='+$('#question_id').val());

    $('#pre_ques').attr('href', '/exam/shortAnswer?no='+(parseInt($('#question_id').val())-1));
    $('#next_ques').attr('href', '/exam/shortAnswer?no='+(parseInt($('#question_id').val())+1));

    $('#pre_stu').attr('href', '/exam/shortAnswer?no='+$('#question_id').val()+'&&answer='+(parseInt($('#answer_no').val())-1));
    $('#next_stu').attr('href', '/exam/shortAnswer?no='+$('#question_id').val()+'&&answer='+(parseInt($('#answer_no').val())+1));

    $(document).on('click','.close_btn',function (){
        $(this).parent().remove();
    });

    $('.add_btn').click(function () {
        var new_word = "<div class=\"d-flex flex-row line\"><div class=\"border p-1 d_key\" contenteditable=\"true\">&emsp;</div><div class=\"border p-1 d_value\" contenteditable=\"true\">&emsp;</div><button type=\"button\" class=\"btn btn-outline-danger p-1 close_btn\" aria-label=\"Close\">&times;</button></div>";
        $(this).parent().before(new_word);
    });

    $('#save_btn').click(function () {
        let trains_dict= Object.create(null);
        $('.stu_answer').each(function () {
            trains_dict[$(this).text().trim()] = $('.score_input').eq($('.stu_answer').index(this)).val().trim();
        });
        $.post("/exam/saveTraining",{
            question_id: $('#question_id').val(),
            trains: JSON.stringify(trains_dict)
        },function (data, status) {
            if(status == 'success'){
                location.reload();
            }
        });
    });
});
