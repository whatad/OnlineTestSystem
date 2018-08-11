 var qt_type="1";
        $(function () {
            function Editor(input, preview) {
                this.update = function () {
                    preview.innerHTML = markdown.toHTML(input.value);
                    // 标记答案
                    markAnswer(qt_type);
                    changeSize();
                };
                //   changeSize();
                input.editor = this;
                this.update();
            }
            var $ = function (id) { return document.getElementById(id); };
            new Editor($("text-input"), $("preview"));
        })
        // 标记答案
        function markAnswer(type) {
            var list = ['A','B','C','D','E','F','G','H'];
            if(type=="1"||type=="2"){
                $(".question").each(function (index, element) {
                    var answer = $(this).find(".qt_answer").addClass("hidden").text().replace(/^答案[:：]/,"").toUpperCase();
                    for (var i = 0; i < list.length; i++) {
                        if(answer.search(list[i])!=-1){
                            $(this).find(".key_"+list[i]+" .checkOrRadio").prop("checked",true);
                        }
                    }
                });
            }
        }
        //当题号过长时改变字号
        function changeSize() {
            $(".question .qt_title .title").each(function(index, element) {
                var $numWords = $(this).text().length;
                if($numWords==4){
                    $(this).css({"font-size":"20px"});
                }else if ($numWords==5) {
                    $(this).css({"font-size":"16px"});
                }else if ($numWords>5) {
                    $(this).css({"font-size":"14px"});
                }
            });
        }
        //关键字提示信息的出现与隐藏
        $('.keyWordBadge').hover(function(){
            $(this).css({"background":"#A9B3BF"});
            $('#keyWordContent').css({"display":"block"});
        },function(){
            $(this).css({"background":"#ddd"});
            $('#keyWordContent').css({"display":"none"});
        });
        // 试题类型以及难度选择
        $(".body-content .cont-r .tab-content .batch-type .simulationSelect").click(function(e){
            e.stopPropagation();
            $(this).children(".simulationOption").show();
            $(this).siblings(".simulationSelect").children(".simulationOption").hide();
        });
        $('body').click(function(){
            $('.simulationOption').hide();
        });
        $(".body-content .cont-r .tab-content .batch-type .simulationOption div").click(function(e){
            var idx = $(this).index();
            $(this).parents('.simulationSelect').next().children().prop("selected",false);
            e.stopPropagation();
            var sel = $(this).text();
            $(this).parents(".simulationSelect").children("span").text(sel);
            $(this).parent().hide();
            $(this).parents('.simulationSelect').next().children().eq(idx).prop('selected','selected').change()
        });


        //答案乱序

        // excle导入模态框
        $(".excel_import").on("click",function(){
            $('#excleImportModal').modal({
                backdrop:"static",
                keyboard:false
            });
        });
        $(".disorder-help").mouseover(function(){
            $(".disorder-prompt").show();
        }).mouseout(function(){
            $(".disorder-prompt").hide();
        })

        $(".answer-help").mouseover(function(){
            $(".answer-prompt").show();
        }).mouseout(function(){
            $(".answer-prompt").hide();
        })
