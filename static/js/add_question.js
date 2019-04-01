$(document).ready(function(){
    $('#space_add').click(function () {
        var new_space = "<div class=\"m-2\">\n" +
            "                    <label>空格1</label>\n" +
            "                    <div class=\"space border rounded p-2 \">\n" +
            "                        <div class=\"form-group row\">\n" +
            "                            <label class=\"col-2 col-form-label\">匹配模式</label>\n" +
            "                            <select class=\"form-control col-9 mode\" name=\"mode\">\n" +
            "                                <option value=\"0\">完全匹配</option>\n" +
            "                                <option value=\"1\">关键词匹配</option>\n" +
            "                                <option value=\"2\">语义匹配</option>\n" +
            "                            </select>\n" +
            "                        </div>\n" +
            "                        <div class=\"form-group row\">\n" +
            "                            <label class=\"col-2 col-form-label\">分数</label>\n" +
            "                            <input name=\"score\" class=\"form-control col-9 score\" placeholder=\"请输入分值\"/>\n" +
            "                        </div>\n" +
            "                        <div class=\"form-group row\">\n" +
            "                            <label class=\"col-2 col-form-label\">得分点</label>\n" +
            "\n" +
            "                            <div class=\"col-9 input_word\">\n" +
            "                                <textarea name=\"point\" class=\"form-control point\" placeholder=\"请输入得分内容\" rows=\"3\"></textarea>\n" +
            "                                <small class=\"form-text text-muted\">可代替得分点在同一行，用英文分号分开，形式为：得分点+空格+得分百分比(语义匹配时只需将关键词用分号隔开，完成点击确定键)</small>\n" +
            "                            </div>\n" +
            "\n" +
            "                            <div class=\"col-9 checkboxes d-none\">\n" +
            "\n" +
            "                            </div>\n" +
            "\n" +
            "                            <input class=\"btn btn-primary col-1 offset-9 d-none sememes\" type=\"button\" value=\"确定\"/>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "                </div>";
        $(this).before(new_space);
    });

    $('#branch_add').click(function () {
        var new_branch = "<div class=\"m-2\">\n" +
            "                    <label>分点1</label>\n" +
            "                    <div class=\"space border rounded p-2 \">\n" +
            "                        <div class=\"form-group row\">\n" +
            "                            <label class=\"col-2 col-form-label\">分数</label>\n" +
            "                            <input name=\"scoreb\" class=\"form-control col-9 scoreb\" placeholder=\"请输入分值\"/>\n" +
            "                        </div>\n" +
            "                        <div class=\"form-group row\">\n" +
            "                            <label class=\"col-2 col-form-label\">分点答案</label>\n" +
            "                            <textarea name=\"branch\" class=\"form-control col-9 m-2 branch\" placeholder=\"请输入分点答案\" rows=\"3\"></textarea>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "                </div>";
        $(this).before(new_branch);
    });

    $('#type').change(function () {
        if($(this).val() == '1'){
            $('#fillblank_area').removeClass('d-none');
            $('#short_answer_area').addClass('d-none');
        }
        else{
            $('#fillblank_area').addClass('d-none');
            $('#short_answer_area').removeClass('d-none');
        }
    });

    $(document).on('change','.mode',function () {
        var index = $('.mode').index(this);
       if($(this).val() == '2') {
            $('.sememes').eq(index).removeClass('d-none');
       }
       else{
           $('.sememes').eq(index).addClass('d-none');
           $('.checkboxes').eq(index).addClass('d-none');
           $('.input_word').eq(index).removeClass('d-none');
       }
    });

    $(document).on('click','.sememes',function () {
        var index = $('.sememes').index(this);
        $.post("/exam/getConcepts/",
            {
                words: $('.point').eq(index).val()
            },
            function(data,status){
                if(status == 'success'){
                    alert("success");
                    $('.input_word').eq(index).addClass("d-none");
                    var check_div = $('.checkboxes').eq(index);
                    check_div.removeClass("d-none");
                    data = JSON.parse(data);
                    var concept_list = data['concept_list'];
                    for ( var i = 0; i <concept_list.length; i++){
                        var concept = JSON.parse(concept_list[i]);
                        var div = $("<div></div>");
                        var input = "<input name=\"point\" type=\"checkbox\" value=\""+concept.id+"\" />";
                        var label = $("<label></label>").text(concept['word'] + " " + concept['type'] + " " + concept['concept']);
                        var label2 = $("<label class='float-right'></label>").text("分值%：")
                        var per = "<input type='text' name='score' class='float-right' size='5'/>"
                        div.append(input);
                        div.append(label);
                        div.append(per);
                        div.append(label2);
                        check_div.append(div);
                    }
                }
            }
        );
    });

});