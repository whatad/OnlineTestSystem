var height1 = $("#this_question").height();
$("#vertical_line1").height(height1);

var height2 = $("#this_result").height();
$("#vertical_line2").height(height2);
$("#vertical_line3").height(height2);


//修改页面里分值前面的竖线
var height3 = $("#vertical_line_question").height();
$("#vertical_line_modify").height(height3);


$("#modify_question_btn").click(function () {
    if ($("#modify_question_div").css("display")=="none") {
        $("#modify_question_div").show();
        $("#training_record_div").hide();
        $("#word_database_div").hide();
    } else {
        $("#modify_question_div").hide();
    }

});


$("#word_database_btn").click(function () {
    if ($("#word_database_div").css("display") == "none") {
        $("#word_database_div").show();
        $("#modify_question_div").hide();
        $("#training_record_div").hide();
    } else {
        $("#word_database_div").hide();
    }
});


$("#training_record_btn").click(function () {
    if ($("#training_record_div").css("display") == "none") {
        $("#training_record_div").show();
        $("#word_database_div").hide();
        $("#modify_question_div").hide();
    } else {
        $("#training_record_div").hide();
    }
});

function jump(id) {
    $(location).prop('href', '/exam/training/?id='+id);
}