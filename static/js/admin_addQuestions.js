var comb_data={question:'',insert_data:[]};
$(document).ready( function() {
	//excel批量导入
   $("body").on("change", "#excelUpload", function() {
        $("#uploadForm").submit();
        $(".loading").show();
        var obj = document.getElementById('excelUpload') ;
        obj.outerHTML=obj.outerHTML;
    });

    $("#excelFrame").on("load",function(){
        var msg=JSON.parse($(this).contents().find("body").text());
        $(".loading").hide();
        $('#excleImportModal').modal('hide');
        showExcelRes(msg);
    });

	//答案乱序默认开启
	$(".pull-right .has-switch div").attr("class","switch-on");


	$(".keyJudge, .keyFill, .keyCloze").hide();


    $("input[type=file]").change(function() {
        $("#uploadForm").submit();
        $(".loading").show();
    });

	// 重置页面
	$(".btn-reset").click(function(e) {
		e.stopPropagation();
		e.preventDefault();
		resetPage();
	});

	// 初始化编辑器
    $.each($('.questions_add').toArray().reverse(),function() {
		initialEditor($(this));
    });

	// 保持只有一个编辑器
	$('body').on('click','.wangEditor-container',function () {
		$('.wangEditor-container').removeClass('active');
		$(this).addClass('active');
	});

	//选择分类
	$("body").on("click", "#selTypeLink", function(e) {
        e.stopPropagation();
		e.preventDefault();
		showSelType(this);
    });

	//切换试题分类
	$(".batch-type select[name=type]").change(function(e) {
		$('.wangEditor-container').removeClass('active');
		$("#asyncForm input[name=type]").val($(this).val());
		changeType($(this).val(),true);
	});

	//<!---------问答题关键字start------------>
	// 添加关键词（normalWord普通关键字，keyWord核心关键字）
	$("#normalWord, #keyWord").click(function() {
		var keyWord = $.trim($(this).parents(".keyWordPanel").find("input[name=key_word]").val());
		// escape keyWord
		keyWord = escapeKeyHTML(keyWord);
		var keyType = $(this).hasClass("btn-normal-word") ? 'normal-word' : 'key-word';
		var keyLength = $("#keyBlock").find(".whole-word").length;
		var index = (keyLength==0) ? 0 : (parseInt($("#keyBlock").find(".whole-word").last().attr("index"))+1);
		var key_html = "";
		if(keyWord==""){
			alert("请输入关键词！");

			return false;
		}else {
			if(keyWord.search(/[\||｜]/)==-1){//单个关键词
				key_html = '<span class="word single-word">' + keyWord + '</span><em class="remove-word glyphicon glyphicon-remove"></em>';
			}else {//组合型关键词
				var keyWords = keyWord.split(/[\||｜]/);
				for (var i = 0; i < keyWords.length; i++) {
					key_html += '<span class="word multi-word">' + keyWords[i] + '</span>' +
							   ((i==keyWords.length-1) ? '<em class="remove-word glyphicon glyphicon-remove"></em>' : '<em class="relate-word">或</em>');
				}
			}
			$("#keyBlock").append('<div class="whole-word ' + keyType + '" id="word' + index + '" index="' + index + '">' + key_html + '</div>');
			$(this).parents(".keyWordPanel").find("input[name=key_word]").val("");
			// 初始化每个关键词的提示框
			initialPopover($("#word"+index),index);
			if(keyLength==0){
				$("#keyBlock").slideToggle(200);
			}
		}

	});

	// 切换关键词类型
	$("body").on("click", ".switch-word" , function(e) {
		e.stopPropagation();//阻止事件冒泡
		e.preventDefault();//阻止事件默认行为
		var index = $(this).attr("index");
		var $word = $("#word"+index);
		if($(this).hasClass("switch-key-word")){//normal->key
			$($word).removeClass("normal-word").addClass("key-word");
		}else if ($(this).hasClass("switch-normal-word")) {//key-normal
			$($word).removeClass("key-word").addClass("normal-word");
		}
	});

	// 删除关键词
	$("body").on("click", ".remove-word", function(e) {
		e.stopPropagation();
		e.preventDefault();
		var $o = $(this);
		var $p = $($o).parents(".key_block");
		$($o).parents(".whole-word").remove();
		var keyLength = $("#keyBlock").find(".whole-word").length;
		if(keyLength==0){
			$("#keyBlock").slideToggle(200);
		}
	});

	//<!---------问答题关键字end------------>



	// <------批量导入组合题小题start------>
	//选择试题类型，显示不同示例
	$(".combBatchPanel input[name=insert_type]").change(function(e) {
		// 更换试题类型时给出提示信息
		if(confirm("输入区试题内容会清空，请确认")==false){
			$(".combBatchPanel #type"+qt_type).prop("checked",true);
			return false;
		}
		qt_type = $(".combBatchPanel input[name=insert_type]:checked").val();
		$("#text-input").val("");
		$("#preview").empty();
		$("#qtExample .accordion").hide();
		$("#accordion"+qt_type).show();
	});

	// 点击查看例题示范
	$("#showExample").click(function (e) {
		e.stopPropagation();
		e.preventDefault();
		$('#qtExample').modal({});
	});

	// 点击关闭例题示范
	$(".btn-close").click(function(e){
		e.stopPropagation();
		e.preventDefault();
		$('#qtExample').modal('hide');
	});

	// 点击显示下一个错误
	$("#nextError").click(function (e) {
		e.stopPropagation();
		e.preventDefault();
		checkError();
	});

	// 组合题列表中删除小题
	$("body").on("click",".questionList .icons8-delete",function(e) {
		e.preventDefault();
		e.stopPropagation();
		var insert_obj= $(this).parents(".single");
		deleteInsert(insert_obj);
	});

	// 组合题列表中上移小题
	$("body").on("click",".questionList .icon-a_arrow_up",function(e) {
		e.preventDefault();
		e.stopPropagation();
		var insert_obj= $(this).parents(".single");
		chevronUpInsert(insert_obj);
	});

	// 组合题列表中下移小题
	$("body").on("click",".questionList .icon-a_arrow_down",function(e) {
		e.preventDefault();
		e.stopPropagation();
		var insert_obj= $(this).parents(".single");
		chevronDownInsert(insert_obj);
	});

	//批量导入小题
	$("#importBtn").click(function(e) {
		e.stopPropagation();
		e.preventDefault();
		if(checkError()==0) return false;
		var text = $("#text-input").val();
		$("#errorText , #errorTextNew").hide();
		if(text==""){
			alert("导入内容不能为空！");
			return false;
		}else{
			var data=serializeFn();
			var dataForm=JSON.stringify(data);
			$("#import").hide();
			$("#import_questions").show();
			$.ajax({
			  type: "POST",
			  cache : false,
			  headers: { "cache-control": "no-cache" },
			  dataType: "json",
              contentType: "application/json",
              url: "",
			  data: dataForm,
			  success: function(data){
				  addBatchInsert(data.bizContent);
				  $("#text-input").val("");
				  $("#preview").empty();
				  $("#import_questions").hide();
				  $("#import").show();
			  }
		  });
		}
	});

	// <------批量导入组合题小题 end ------>



	//选择题 增加答案选项
	$("body").on("click",".keyRadio .addKey",function() {
		var obj = $(this).parents(".keyPanel");
		var keyLength = $(obj).find(".keyList").length;
		var input_type = $("select[name=type]").val()=="1" ? "radio" : "checkbox";
		var html =  '<div class="keyList keyListAdd">'+
                    '    <div class="keyLeft">'+
                    '        <input type="' + input_type + '" class="radioOrCheck" name="keyChk" />'+
                    '    </div>'+
                    '    <div class="keyRight keyRight'+(keyLength+1)+'">'+
                    '        <div id="key'+(keyLength+1)+'Editor" class="questions_add"></div>'+
                    '        <input name="answer'+(keyLength+1)+'" type="hidden" />'+
                    '    </div>'+
                    '    <a href="javascript:void(0);" class="removeKey glyphicon glyphicon-trash"></a>'+
                    '</div>';
		$(obj).find(".addKeyBtn").before(html);
		initialEditor("key"+(keyLength+1)+"Editor");
		$('.wangEditor-container').removeClass('active');
		$(".keyRight"+(keyLength+1)+" .wangEditor-container").addClass('active');
		if (keyLength==7) {
			$(obj).find(".addKeyBtn").addClass("hidden");
			return false;
		}
	});

	// 选择题 删除答案选项
	$("body").on("click",".keyRadio .removeKey",function() {
		$(".keyRadio .addKeyBtn").removeClass("hidden");
		$(this).parents(".keyList").remove();
		$(".keyRadio .keyList").each(function(index, element) {
			var obj = $(this).find(".keyRight");
			$(obj).attr("class","keyRight keyRight"+(index+1));
			$(obj).find(".questions_add").attr("id","key"+(index+1)+"Editor");
			$(obj).find("input").attr("name","answer"+(index+1));
		});
	});


	//保存并新增
	$("#saveAndAddBtn").click(function(e) {
		var type=$("#asyncForm input[name=type]").val();
		if(type==6){
			var classification = $("#subForm input[name=classification]").val();
			if(classification == "0"){
				alert("请选择试题分类！");
				return false;
			}
			saveComb();
		}else {
			if(checkForm()){
				if(serializeForm()){
					asyncSub();
				}
			}
		}
    });

	// //关闭导入方式对话框
	// $("#modeModal_close").click(function(e) {
    //     hideSelMode();
    // });

	//填空题添加多个
	$("div.keyFill .addKeyFill").click(function(e) {
		var keyLength = $("input[name=keyFill]").length;
		if (keyLength==9) {
			$(".keyFill .addKeyFillBtn").addClass("hidden");
		}
		var html='<div class="keyFillContent keyFillContentAdd">'+
				 '	 <div class="input-group">'+
				 '		  <span class="input-group-addon">'+(keyLength+1)+'</span>'+
				 '		  <span><input type="text" name="keyFill"  class="form-control" placeholder="请输入答案，按下回车添加同义词。"></span>'+
				 '		  <span class="addfillgrade">分值</span>'+//添加分值
				 '		  <span><input type="text" name="addfillgrade/"></span>'+//添加分值
				 '	 </div>'+
				 '	  <a href="javascript:void(0);" class="removeKeyFill glyphicon glyphicon-remove"></a>'+
				 '</div>';
		$("div.addKeyFillBtn").before(html);
		$("input.form-control").attr("data-role","tagsinput");
		$("input.form-control").tagsinput();
    });



	//填空题删除多个
	$("body").on("click", "a.removeKeyFill", function(e) {
		$(".keyFill .addKeyFillBtn").removeClass("hidden");
        $(this).parents("div.keyFillContent").remove();
		$(".keyFill .input-group-addon").each(function(index,element) {
			$(this).text(index+1);
		});
    });

	//答案乱序
	if($(".pull-right .has-switch div input:checkbox").is(":checked")){
		$("input[name=disorder]").val(1);
	}else{
        $("input[name=disorder]").val(0);
    }


});//$(document).ready( function()结束




// 重置页面
function resetPage() {
	var type = $("#subForm select[name=type]").val();
	var html = "";
	if(type=="1"||type=="2"){
		var input_type = (type==1) ? "radio" : "checkbox";
		var key_length = $(".keyRadio").find(".keyList").length;
		for (var i = key_length; i < 4; i++) {
			html = '<div class="keyList">'+
					'    <div class="keyLeft">'+
					'        <input type="' + input_type + '" class="radioOrCheck" name="keyChk" />'+
					'    </div>'+
					'    <div class="keyRight keyRight'+(i+1)+'">'+
					'        <div id="key'+(i+1)+'Editor" class="questions_add"></div>'+
					'        <input name="answer'+(i+1)+'" type="hidden" />'+
					'    </div>'+ ((i<2) ? '' :'<a href="javascript:void(0);" class="removeKey icons8-delete"></a>')+
					'</div>';
			$(".addKeyBtn").before(html);
			initialEditor("key"+(i+1)+"Editor");
		}
	}
	$('.wangEditor-container').removeClass('active');
	if(type == "1"){
		$(".keyRadio input[type=checkbox]").attr("type","radio");
	}else if (type == "2") {
		$(".keyRadio input[type=radio]").attr("type","checkbox");
	}
	$('#asyncForm')[0].reset();
	$(".radioOrCheck").prop("checked",false);
	$("#judgeYes").prop("checked",true);
	$("div.keyFillContentAdd, div.keyListAdd").remove();
	$(".questionPanel,#keyBlock").hide();
	$(".questionPanel .questionList, .questions_add, #keyBlock, #preview").empty();
	$(".keyRadio .addKeyBtn, .keyFill .addKeyFillBtn").removeClass("hidden");
	$("input[name=keyFill], #text-input").val("");
	$(".combPanel, .descPanel, .keyPanel, .analysisPanel").find("input").val("");
}

// 初始化编辑器
function initialEditor(o) {
	var editor = new wangEditor(o);
	editor.config.printLog = false;
	editor.config.uploadImgUrl = '';//'/admin/upload/?userRole=admin&action=uploadimage';
	editor.config.uploadImgFileName = ''//'upfile';
	editor.config.uploadVideoUrl ='';// '/admin/upload/?userRole=admin&action=uploadvideo';
	editor.config.uploadVideoFileName = ''//'upfile';
	editor.config.uploadFileUrl = ''//'/admin/upload/?userRole=admin&action=uploadfile';
	editor.config.uploadFileFileName = ''//'upfile';
	editor.config.menus = [
		'bold',
		'underline',
		'italic',
		'strikethrough',
		'|',
		'fontfamily',
		'fontsize',
		'head',
		'unorderlist',
		'orderlist',
		'alignleft',
		'aligncenter',
		'alignright',
		'|',
		'table',
		'img',
		'fileUpload',
		'mediaUpload',
		'|',
		'fullscreen'
	];
	editor.create();
    // force editor blur
	editor.$txt.blur();
	var $input = $(editor.$editorContainer).next();
	editor.$txt.blur(function () {
		var $temp = $('<div></div>');
		$temp.html($(this).html());
		$.each($temp.find('.video-temp-img'), function() {
			var src = $(this).attr('temp_src');
			var alt = $(this).attr('alt');
			$(this).after('<video controls alt="'+alt+'"><source src="'+src+'"></video>');
			$(this).remove();
		});
        $.each($temp.find('.audio-temp-img'), function() {
            var src = $(this).attr('temp_src');
            var alt = $(this).attr('alt');
            $(this).after('<audio controls alt="'+alt+'"><source src="'+src+'"></audio>');
            $(this).remove();
        });
		$input.val($temp.html());
    });
}



// 初始化每个关键词的提示框
function initialPopover(o, index) {
	$('#word'+index).popover({
		'container' : '#word'+index,
		'placement' : 'top',
		'trigger' : 'hover',
		'content' : function() {
						var type = $(o).hasClass("key-word") ? "key-word" : "normal-word";
						var normal_btn = '<button class="btn btn-gray switch-word switch-normal-word" index="' + index +'">切为普通关键词</button>';
						var key_btn = '<button class="btn btn-l-orange switch-word switch-key-word" index="' + index +'">切为核心关键词</button>';
						return (type == 'key-word' ? normal_btn : key_btn);
					},
		'html' : true,
		'template' : '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-content"></div></div>',
	});
}

// escape keyWord
function escapeKeyHTML( text ) {
  return text.replace( /&/g, "&amp;" )
             .replace( /</g, "&lt;" )
             .replace( />/g, "&gt;" )
             .replace( /"/g, "&quot;" )
             .replace( /'/g, "&#39;" )
}


//显示选择分类对话框
function showSelType(obj){
	selTypeModal.location.href = "/admin/tree/tests_class";
	$("#typeModal").modal({
		backdrop:"static",
		keyboard:false
	});
}

//关闭选择分类对话框
function hideSelType(obj){
	$('#typeModal').modal('hide');
}

//接受选择分类数据
function selType(id, name){
	$("input[name=classification]").val(id);
	$("#selTypeLink").text(name);
}

//显示选择导入方式对话框
function showSelMode(obj){
	$('#modeModal').modal({
		backdrop:"static",
		keyboard:false
	});
}

//关闭选择分类对话框
function hideSelMode(obj){
	$('#modeModal').modal('hide');
}

//切换试题分类fn
function changeType(type, normal){
	resetPage();
	$(".keyPanel").hide();
	if(type==1){ //单选
		if(normal){
			$(".combPanel").hide();
			$(".combBatchPanel").hide();
			$(".questionPanel").hide();
		}
		$(".keyRadio").show();
		$(".question-content").show();
		return;
	}
	if(type==2){ //多选
		if(normal){
			$(".questionPanel").hide();
			$(".combPanel").hide();
			$(".combBatchPanel").hide();
		}
		$(".keyRadio input[type=radio]").attr("type","checkbox");
		$(".keyRadio").show();
		$(".question-content").show();
		$(".question").show();
		return;
	}
	if(type==3){ //判断
		if(normal){
			$(".combPanel").hide();
			$(".combBatchPanel").hide();
			$(".questionPanel").hide();
		}
		$(".question-content").show();
		$(".keyJudge").show();
		return;
	}
	if(type==4){ //填空
		if(normal){
			$(".combPanel").hide();
			$(".combBatchPanel").hide();
			$(".questionPanel").hide();
		}
		$(".question-content").show();
		$(".keyFill").show();
		return;
	}
	if(type==5||type==7){ //问答
		if(normal){
			$(".combPanel").hide();
			$(".combBatchPanel").hide();
			$(".questionPanel").hide();
		}
		$(".question-content").show();
		if(type==5){
			$(".keyCloze .keyWordPanel").show();
		}else if (type==7) {
			$(".keyCloze .keyWordPanel").hide();
		}
		$(".keyCloze").show();
		return;
	}
	if(type==6){ //组合题
		if(normal){
			$(".question-content").hide();
			if($(".questionPanel .input-group").length==0){
				$(".questionPanel").hide();
			}else {
				$(".questionPanel").show();
			}
			$(".combPanel").show();
			$(".combBatchPanel").show();
			// 行号
			$("#text-input").setTextareaCount({
				width: "33px",
				bgColor: "#edf2f7",
				color: "#989A9C",
				display: "inline-block",
			});
		}
		return;
	}
}

//验证表单选项
function checkForm(){
	var classification = $("#subForm input[name=classification]").val();
	var type = $("#asyncForm input[name=type]").val();
	if(classification=='0'){
		alert("请选择试题分类！");
		return false;
	}
	if(type==0){
		alert("请选择试题类型！");
		return false;
	}
	if(filterContentIsEmpty($("input[name=question]").val())){
		alert("请填写试题描述！");
		return false;
	}

	if(type==1||type==2){
		var key = $(".keyRadio .radioOrCheck");
		var ifCheck = false;
		for(var i=0;i<key.length;i++){
			var checked = $(key[i]).is(":checked");
			$(key[i]).parent().find(".key").remove();
			if(checked===true){
				ifCheck = true;
				$(key[i]).parent().append('<input type="hidden" class="key" name="key'+(i+1)+'" value="1" />');
			}else{
				$(key[i]).parent().append('<input type="hidden" class="key" name="key'+(i+1)+'" value="0" />');
			}
		}
		if(ifCheck===false){
			alert("请选择正确答案！");
			return false;
		}
		return true;
	}
	if(type==4){
		var key=$(".cont-r").find("input[name=keyFill]");
		var ifFill= true;
		for(var i=0;i<key.length;i++){
			if(filterContentIsEmpty($(key[i]).val())){
				alert("请填写试题答案！");
				ifFill=false;
				break;
			}
		}
		if(ifFill==false){
			return false;
		}
		return true;

	}
	if(type==5||type==7){
		if(filterContentIsEmpty($(".keyCloze input[name=answer1]").val())){
			 alert("请填写试题答案！");
			 return false;
		 }
	}
	return true;
}

//提交试题数据合并
function serializeForm(){
	$("#asyncForm div").html("&nbsp;");
	$("#asyncForm input[name=classification]").val($("#subForm input[name=classification]").val());
	$("#asyncForm input[name=tab_num]").val($(".keyRadio").find(".keyList").length);
	$("#asyncForm input[name=status]").val("enable");
	$("#asyncForm input[name=difficult]").val($("#subForm select[name=difficult]").val());
	$("#asyncForm input[name=encrypt]").val("0");
    if($(".pull-right .has-switch div input:checkbox").is(":checked")){
        $("#asyncForm input[name=disorder]").val(1);
    }else{
        $("#asyncForm input[name=disorder]").val(0);
    }
    // $("#asyncForm input[name=disorder]").val($(".has-switch input[type=checkbox]").val());
    //保存答案乱序
     // if(disorder=="on"){
     //    $("input[name=disorder]").val(1);
     // }else{
     //    $("input[name=disorder]").val(0);
     // }


    // if($(".pull-right .has-switch div").hasClass("switch-on")){
    //     $("input[name=disorder]").val(1);
    // }else{
    //     $("input[name=disorder]").val(0);
    // }

	// 关键词整合
	var normal_words = '';
	var normal_length = $("#keyBlock").find(".normal-word").length;
	$("#keyBlock").find(".normal-word").each(function(index, element) {
		var $w = $(this).find(".word");
		if($($w).hasClass("single-word")){//单个关键词 分隔符：＃
			normal_words += escapeKeyHTML($($w).text()) + (index == normal_length-1 ? '' : '#');
		}else if ($($w).hasClass("multi-word")) {//组合型关键词  分隔符：&
			var $w_length = $w.length;
			$($w).each(function(index, element) {
				normal_words += escapeKeyHTML($(this).text()) + (index == $w_length-1 ? '' : '||');
			});
			normal_words += (index == normal_length-1 ? '' : '#');
		}
	});
	var key_words = '';
	var key_length = $("#keyBlock").find(".key-word").length;
	$("#keyBlock").find(".key-word").each(function(index, element) {
		var $w = $(this).find(".word");
		if($($w).hasClass("single-word")){//单个关键词  分隔符：＃
			key_words += escapeKeyHTML($($w).text()) + (index == key_length-1 ? '' : '#');
		}else if ($($w).hasClass("multi-word")) {//组合型关键词  分隔符：&
			var $w_length = $w.length;
			$($w).each(function(index, element) {
				key_words += escapeKeyHTML($(this).text()) + (index == $w_length-1 ? '' : '||');
			});
			key_words += (index == key_length-1 ? '' : '#');
		}
	});
	$("#asyncForm input[name=normalWords]").val(normal_words);
	$("#asyncForm input[name=keyWords]").val(key_words);

	var parent_dom=$("#editor").parent();
	$("#asyncForm textarea[name=question]").text($("input[name=question]").val());
	$("#asyncForm textarea[name=analysis]").text($("input[name=analysis]").val());

	var type = $("#asyncForm input[name=type]").val();
	if(type==1||type==2){
		var keyList = $(".keyRadio").find(".keyList");
		for(var i=0;i<keyList.length;i++){
			if(i<=(keyList.length-1)){
				var answer='';
				//此处注意，不能用keyList，否则下面input有两个，取不到值
				answer=$(keyList[i]).find(".keyRight").children("input[name=answer"+(i+1)+"]").val();
				$(keyList[i]).find(".key").clone().appendTo("#asyncForm div");
				$("#asyncForm div").append('<textarea name="answer'+(i+1)+'"></textarea>');
				$("#asyncForm textarea[name=answer"+(i+1)+"]").text(answer);
			}
		}
		return true;
	}else if(type==3){
		if($("#judgeYes").is(":checked")){
			$("#keyYes").val("1");
			$("#keyNo").val("0");
			$("#asyncForm div").html('<input type="hidden" class="" name="key1" value="1" /><input type="hidden" class="" name="key2" value="0" /><input type="hidden" class="radioOrCheck" name="answer1" value="" /><input type="hidden" class="radioOrCheck" name="answer2" value="" />');
		}else{
			$("#keyYes").val("0");
			$("#keyNo").val("1");
			$("#asyncForm div").html('<input type="hidden" class="" name="key1" value="0" /><input type="hidden" class="" name="key2" value="1" /><input type="hidden" class="radioOrCheck" name="answer1" value="" /><input type="hidden" class="radioOrCheck" name="answer2" value="" />');
		}
		return true;
	}else if(type==4){
		var keyList = $("input[name=keyFill]");
		var html = "";
		$("input[name=keyFill]").each(function(index, element) {
            var reg=/,/g;
			html = '<input type="hidden" class="" name="key'+(index+1)+'" value="1" /><input type="hidden" class="radioOrCheck" name="answer'+(index+1)+'" value="'+$(this).val().replace(reg,"&&")+'" />';
			$("#asyncForm div").append(html);
		});
		return true;

	}else if(type==5||type==7){
		$("#asyncForm div").append('<textarea name="answer1"></textarea>');
		$("#asyncForm div").append('<input type="hidden" class="" name="key1" value="1" />');
		$("#asyncForm div textarea[name=answer1]").text($(".keyCloze input[name=answer1]").val());
		return true;
	}
}

//异步提交表单
function asyncSub(){
	var dataForm =$('#asyncForm').serialize();
	$.ajax({
		type: "POST",
		cache : false,
		headers: { "cache-control": "no-cache" },
		dataType: "json",
		url: "",//"/admin/addtestqm",
		data: dataForm + "&t="+Math.random(),
		success: function(msg){
				if(msg.success == true){
					resetPage();
					alert("保存成功！");
				}else{
					alert(msg.errmsg);
				}
		}
	});
}


// <------组合题小题操作 start ------>

// 检查组合题小题
function checkInsert(){
	var type=comb_data.insert_data[0].type;
	if(filterContentIsEmpty($("input[name=question]").val())){
		alert("请填写试题描述！");
		return false;
	}
	if(type==1||type==2){
		var key_len=$(".keyRadio .radioOrCheck:checked").length;
		if(key_len==0){
			alert("请选择正确答案！");
			return false;
		}
	}
	if(type==4){
		var key=$(".cont-r").find("input[name=keyFill]");
		var ifFill= true;
		for(var i=0;i<key.length;i++){
			if(filterContentIsEmpty($(key[i]).val())){
				alert("请填写试题答案！");
				ifFill=false;
				break;
			}
		}
		if(ifFill==false){
			return false;
		}
	}
	if(type==5||type==7){
        if(filterContentIsEmpty($(".keyCloze input[name=answer1]").val())){
            alert("请填写试题答案！");
            return false;
        }
	}
	return true;
}


// 组合题列表中删除小题
function deleteInsert(obj) {
	var has_insert_num=$(obj).find(".input-group").attr("sort");
	$(".questionPanel").find(".input-group").each(function(index, element) {
		var sort=$(this).attr("sort");
		if(sort>has_insert_num){
			$(this).attr("sort",sort-1);
			$(this).find(".input-group-addon").text(sort);
			$(this).removeClass("input-group"+sort);
			$(this).addClass("input-group"+(sort-1));
		}
	});
	$(obj).remove();
	var has_insert_num = $(".questionPanel .questionList .single").length;
	if(has_insert_num == 0){
		$(".questionPanel").hide();
	}
}

// 组合题列表中上移小题
function chevronUpInsert(obj){
	var prev_html = $(obj).prev().find(".input-div").html();
	var prev_id = $(obj).prev().find(".input-group").attr("insert_id");
	var this_html = $(obj).find(".input-div").html();
	var this_id = $(obj).find(".input-group").attr("insert_id");
	$(obj).find(".input-div").html(prev_html);
	$(obj).find(".input-group").attr("insert_id",prev_id);
	$(obj).prev().find(".input-div").html(this_html);
	$(obj).prev().find(".input-group").attr("insert_id",this_id);
}

// 组合题列表中下移小题
function chevronDownInsert(obj) {
	var next_html = $(obj).next().find(".input-div").html();
	var next_id = $(obj).next().find(".input-group").attr("insert_id");
	var this_html = $(obj).find(".input-div").html();
	var this_id = $(obj).find(".input-group").attr("insert_id");
	$(obj).find(".input-div").html(next_html);
	$(obj).find(".input-group").attr("insert_id",next_id);
	$(obj).next().find(".input-div").html(this_html);
	$(obj).next().find(".input-group").attr("insert_id",this_id);
}

// <------组合题小题操作 end ------>


// <------批量导入组合题小题 start ------>

//点击导入时检查试题中是否存在错误
function checkError() {
    // 首先检查题目中有无重复项，若有重复则对整题做标记
    $("#preview").find(".question").each(function (index,element) {
        var key_t=[];
        key_t[0]=$(this).find(".key_A").length;
        key_t[1]=$(this).find(".key_B").length;
        key_t[2]=$(this).find(".key_C").length;
        key_t[3]=$(this).find(".key_D").length;
        key_t[4]=$(this).find(".key_E").length;
        key_t[5]=$(this).find(".key_F").length;
        key_t[6]=$(this).find(".key_G").length;
        key_t[7]=$(this).find(".key_H").length;
        // 按照选项重复个数从大到小排序
        key_t.sort(function(a,b) {
            return b-a;
        });
        if(key_t[0]>1){
            $(this).addClass("check_error");;
        }
        // 对按照答案对选型进行检索，若答案不在选项中，则将答案标记为错误
        if(qt_type=="1"||qt_type=="2"){
            var ans=$(this).find(".qt_answer").text().replace(/^答案[:：]/,"").replace(/\s/g,"").toUpperCase();
            if(ans.replace(/[A-Z]/g,"")!=""){
                $(this).addClass("check_error");
            }else {
                var ans_l=$.trim(ans).split("");
                for (var i = 0; i < ans_l.length; i++) {
                    var key_f=$(this).find(".key_"+ans_l[i]).length;
                    if(key_f==0){
                        $(this).addClass("check_error");
                        break;
                    }
                }
            }
        }
        if(qt_type=="3") {
            ans=$(this).find(".qt_answer").text().replace(/^答案[:：]/,"").replace(/\s/g,"");
            if(ans != '正确' && ans != '错误' && ans != '对' && ans != '错'){
                $(this).find(".qt_answer").addClass("error");
            }
        }
        if(qt_type=='4'||qt_type=='5'){
            ans=$(this).find(".qt_answer").text().replace(/^答案[:：]/,"").replace(/\s/g,"");
            if(ans==''){
                $(this).addClass("check_error");
            }
        }
    });
    var error=$("#preview").find(".qt_error, .error, .check_error");
    if (error.length!=0){
        $("#errorCount").text(error.length);
        $("#errorText").show();
        $("#nextError").show();
        // 滚动预览区，使得第一处错误出现在视野中
        var a=$(error[0]).offset().top;
        var b=$("#preview").parent(".box").scrollTop();
        var c=$("#preview").parent(".box").offset().top;
        $("#preview").parent(".box").animate({scrollTop:a+b-c-70},200);
        // 根据预览区滚动高度占比同时滚动输入区
        var d=document.getElementById("text-input").scrollHeight;
        var e=document.getElementById("preview").scrollHeight;
        $("#text-input").animate({scrollTop:(a+b-c-70)*d/e},200);
        return 0;//仍有错误
    }else {
        // 若无错误则初始化状态
        $("#errorText").hide();
        $("#nextError").hide();
        $("#preview").parent(".box").scrollTop(0);
        $("text-input").scrollTop(0);
        return 1;//没有错误
    }
}

// 批量插入小题
function addBatchInsert(data){
	var has_insert_num = $(".questionPanel .questionList .input-group").length;
	var type = $(".combBatchBlock input[name=insert_type]:checked").val();
	var type_label = "";
	switch (type) {
		case "1": type_label = "单选题";break;
		case "2": type_label = "多选题";break;
		case "3": type_label = "判断题";break;
		case "4": type_label = "填空题";break;
		case "5": type_label = "问答题";break;
	}
	var insert_html = "";
	if(has_insert_num == 0){
		$(".questionPanel").show();
	}
	for (var i = 0; i < data.length; i++) {
		has_insert_num += 1;
		data[i].sTitle = data[i].sTitle.replace("&lt;br&gt;"," ");
		insert_html += '<div class="single">'+
					   '<div class="input-group input-group'+has_insert_num+'" sort="' + has_insert_num + '" insert_id="'+ data[i].sId +'">'+
					   '  <span class="input-group-addon">' + has_insert_num + '</span>'+
					   '  <div  class="input-div"><span class="type">' + type_label + '</span>'+ data[i].sTitle +'</div>' +
					   '</div>'+
					   '<div class="operation-icon">'+
					   '  <em class="icons8-delete"></em>'+
					   '  <em class="icon icon-a_arrow_up"></em>'+
					   '  <em class="icon icon-a_arrow_down"></em>'+
					   '</div>'+
					   '</div>';
	}
	$(".questionPanel .questionList").append(insert_html);
}

// 组织导入试题的信息
function serializeFn() {
    var classification = $("input[name=classification]").val();
    var type=qt_type;
    var difficult=$("select[name=difficult]").val();
    // var disorder=$("input[name=disorder]").val();
    var data=[];
    $("#preview").find(".question").each(function (index,element) {
		var question=escapeHTML($(this).find(".qt_title").html());
        var answer1=$(this).find(".key_A").length==0 ? "" : escapeHTML($(this).find(".key_A").html());
        var answer2=$(this).find(".key_B").length==0 ? "" : escapeHTML($(this).find(".key_B").html());
        var answer3=$(this).find(".key_C").length==0 ? "" : escapeHTML($(this).find(".key_C").html());
        var answer4=$(this).find(".key_D").length==0 ? "" : escapeHTML($(this).find(".key_D").html());
        var answer5=$(this).find(".key_E").length==0 ? "" : escapeHTML($(this).find(".key_E").html());
        var answer6=$(this).find(".key_F").length==0 ? "" : escapeHTML($(this).find(".key_F").html());
        var answer7=$(this).find(".key_G").length==0 ? "" : escapeHTML($(this).find(".key_G").html());
        var answer8=$(this).find(".key_H").length==0 ? "" : escapeHTML($(this).find(".key_H").html());
        if(type=="1"||type=="2"){
            var key=escapeHTML($(this).find(".qt_answer").html()).replace(/&nbsp;/g,"").toUpperCase();
        }else if (type=="3") {
            var key=escapeHTML($(this).find(".qt_answer").html()).replace(/(^\s+)|(\s+$)/g,"").replace(/(正确|对)/,1).replace(/(错误|错)/,0);
		}else{
            var key=escapeHTML($(this).find(".qt_answer").html());
        }
        var analysis=$(this).find(".qt_analysis").length==0 ? "" : escapeHTML($(this).find(".qt_analysis").html());
        data[index]={
            "classification":classification,
            "type":type,
            "difficult":difficult,

			// "disorder":disorder,

            "question":question,
            "answer1":answer1,
            "answer2":answer2,
            "answer3":answer3,
            "answer4":answer4,
            "answer5":answer5,
            "answer6":answer6,
            "answer7":answer7,
            "answer8":answer8,
            "key":key,
            "analysis":analysis
        };
        // 若不存在该项则不存入
        for (i in data[index]) {
            if(data[index][i]==""||!data[index][i]){
                delete data[index][i];
            }
        }
    });
    return data;
}

//转义部分，换行　$markdown_return 进行两次替换
function escapeHTML( text ) {
    return text.replace(/^[\s\S]*<span class="title"[\s\S]*>[\s\S]+<\/span>([\s\S]*)$/,"$1")
        .replace(/<br class="markdown_return">/g, "$markdown_return")
        .replace( /</g, "&lt;" )
        .replace( />/g, "&gt;" )
        .replace(/\&nbsp;/g, " ")
        .replace(/\$markdown_return/g, '<br class="markdown_return">');
}


// 组合题信息拼合
function saveComb(){
	comb_data.question= $(".combPanel input[name=comb_question]").val();
	comb_data.question = comb_data.question.replace(/\&nbsp;/g, " ");
	if(filterContentIsEmpty(comb_data.question)){
		alert("请填写大题题干！");
		return false;
	}
	if($(".questionPanel .input-group").length==0){
		alert("请至少插入一道小题！");
		return false;
	}
	comb_data.status="enable";
	comb_data.difficult=$("#subForm select[name=difficult]").val();
	comb_data.classification=$("#subForm input[name=classification]").val();
	comb_data.type='6';
	comb_data.id='';
	comb_data.tab_num='1';
	$(".questionPanel").find(".input-group").each(function(index, element) {
		var insert_id=$(this).attr("insert_id");
		comb_data.insert_data[index]=insert_id;
	});
	var dataForm = JSON.stringify(comb_data);
	$.ajax({
		type: "POST",
		cache : false,
		headers: { "cache-control": "no-cache" },
		dataType: "json",
        contentType: "application/json",
		url: "/admin/edit_mix_question/?dataType=whole&addType=text",
		data: dataForm,
		success: function(msg){
			if(msg.success == true){
				resetPage();
				comb_data={question:'',insert_data:[]};
				alert("保存成功！");
			}
		}
	});
}


// <------批量导入组合题小题 end ------>

//导入excel结果反馈
function showExcelRes(msg) {
    var result = '';
    if(msg.success == true){
        for (var key in msg.bizContent.succ) {
            switch (key)
            {
                case "table1":
                    type = "单选题";
                    break;
                case "table2":
                    type = "多选题";
                    break;
                case "table3":
                    type = "判断题";
                    break;
                case "table4":
                    type = "填空题";
                    break;
                case "table5":
                    type = "问答题";
                    break;

            }
            result += '<li class="' + key + '">' + type + ":&nbsp;" + msg.bizContent.succ[key] + "&nbsp;道" + '</li>';
        }
        	result = '<div class="success"><div class="title success-title"> 上传成功:</div><ol>' + result + '</ol></div>';
    }else{

        	result = '<div class="error"><div class="title error-title"> 上传失败:导入格式错误</div></div>';
    }

    BootstrapDialog.show({
        title: "excel导入结果",
        message: result,
        buttons: [{
            label: '查看',
            action: function(dialogItself){
                window.open("/admin/showtestqm_new");
            }
        },{
            label: '确定',
            action: function(dialogItself){
                dialogItself.close();
            }
        }]
    });
}

//过滤编辑器内容，确保确实有内容，而非无效标签
function filterContentIsEmpty(str) {
	var regImg = /<img(.*?)>/gi;
	var regTable = /<table(.*?)table>/gi;
    var regFrame = /<iframe(.*?)iframe>/gi;
    var filterStr;

    if(str==''){
		return true;
	}else if(regImg.test(str)||regTable.test(str)||regFrame.test(str)){
    	return false;
	}

	filterStr = str.replace(/<\/?[^>]*>/g, '').replace(/[ |&nbsp;|\n]/g, '');
	return filterStr=='';
}