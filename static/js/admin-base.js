$(function () {
    // initial tooltip
    $('[data-toggle="tooltip"]').tooltip();
    // initial popover
    $('[data-toggle="popover"]').popover();

    // ajaxstart with loading shown
    $( document ).ajaxStart(function() {
        $("#spinnerLoading").removeClass("hidden");
    });
    // ajaxstop with loading hidden
    $( document ).ajaxStop(function() {
        $("#spinnerLoading").addClass("hidden");
    });



    if($(".sidebar-fold").hasClass("icon-unfold")){
        $('.sidebar-nav [data-toggle="tooltip"]').tooltip('destroy');
    }

    // fold sidebar
    $("#sidebar-fold").click(function(e) {
        e.stopPropagation();
        e.preventDefault();
        if($(this).hasClass("icon-unfold")){
            // fold sidebar
            $(this).removeClass("icon-unfold").addClass("icon-fold").attr("title","展开导航").attr("data-original-title","展开导航");
            $(this).find(".icons8").removeClass("icons8-icon").addClass("icons8-icon-3");
            $(".viewFrameWork").removeClass("sidebar-full").addClass("sidebar-min");
            document.cookie = "ksxFoldState=fold; path =; domain=;";
            $('.sidebar-inner [data-toggle="tooltip"]').tooltip();
        }else if ($(this).hasClass("icon-fold")) {
            // unfold sidebar
            $(this).removeClass("icon-fold").addClass("icon-unfold").attr("title","收起导航").attr("data-original-title","收起导航");
            $(this).find(".icons8").removeClass("icons8-icon-3").addClass("icons8-icon");
            $(".viewFrameWork").removeClass("sidebar-min").addClass("sidebar-full");
            document.cookie = "ksxFoldState=unfold; path =; domain=;";
            /*$('.sidebar-inner [data-toggle="tooltip"]').tooltip();*/
            $('.sidebar-nav [data-toggle="tooltip"]').tooltip('destroy');
        }
    });

    //一级导航对应模块显示激活状态
    $(function () {
        //当前地址
        var current_url = window.location.href;
        //导航应当激活项
        var current_item;
        //查询状态
        var query_status = false;
        //所有带导航页面url结构列表
        var url_list = {
            "index": ["account/admin/index"],
            "exam-mgr": ["admin/exam_mgr_new", "admin/showtestqm_new", "admin/paper_mgr_new", "admin/result/mgr_new",
                "admin/result/user_mgr_new", "admin/results/analysis/exam", "admin/online_import_html", "admin/addtestqm",
                "admin/exam_add", "admin/exam/update", "admin/paper_add_new", "admin/paper_manual_add", "admin/update"],
            "user-mgr": ["admin/user_mgr_new", "admin/user_reg", "admin/user_add"],
            "course": ["admin/file/manager", "course/course_mgr", "course/study_record_mgr/user",
                "course/study_record_mgr/course", "course/course_add", "course/add_exam", "course/course_update",
                "course/update_exam"],
            "pay-center": ["account/admin_pay_center", "admin/user_pay_set", "account/admin_consume_record",
                "account/admin_usage_record", "account/admin_order_record", "account/examinee_pay_record"],
            "system-mgr": ["admin/sub_admin_mgr", "account/admin_op_record", "admin/modify", "admin/follow_app/"],
            "user": ["admin/admin_information"],
            //证书
            "certificate": ["certificate/certificate_center","/certificate/certificate_template","certificate/certificate_selExam",
                "certificate/certificate_mine","certificate/certificate_detail","certificate/certificate_edit"]
        };

        for(var o in url_list){
            var item_list = url_list[o];
            for(var i=0; i< item_list.length; i++){
                if(current_url.indexOf(item_list[i])!=-1){
                    query_status = true;
                    break;
                }
            }

            if(query_status){
                current_item = o;
                break;
            }
        }

        $(".sidebar-trans .nav-item.nav-item-"+current_item).addClass("nav-item-active");
    });



    //初始化系统消息
    var POPOVER_HTML = '';
    $.ajax({
        type:'POST',
        cache : false,
        headers: { "cache-control": "no-cache" },
        dataType: "json",
        url: '/account/notification/',
        success:function (msg) {
            var tool_count=msg.bizContent.unreadCount;
            //样式调整，先注释
            /*var tool_html = '';

            if(tool_count==0){
                tool_html = '<span>暂无消息</span>'
            }*/

            // 未读标志
            if(tool_count>9){
                $('#stateMessage .state-message-count').text('9+').removeClass('hidden');
            }else if (tool_count>0) {
                $('#stateMessage .state-message-count').text(tool_count).removeClass('hidden');
            }else {
                $('#stateMessage .state-message-count').addClass('hidden');
            }



            // notifications是最新的消息，最多为5条，添加支消息框
            for (var i = 0; i <msg.bizContent.notifications.length; i++) {
                var content=msg.bizContent.notifications[i].content;
                if(msg.bizContent.notifications[i].isRead==0){//若状态为未读添加未读类
                    tool_html+='<div class="message unread" id="'+msg.bizContent.notifications[i].id+'">'+
                        '<span class="glyphicon glyphicon-volume-up" aria-hidden="true"></span>'
                        +content+'</div>';
                }else {
                    tool_html+='<span class="message read" id="'+msg.bizContent.notifications[i].id+'">'+content+'</span><br>';
                }
            }

            // 如果所有消息中未读消息的数目不为0，则显示有未读消息的标志
            if (tool_count != 0) {
                $(".hasUnread").css("display","inline-block");
            }else {
                $(".hasUnread").hide();
            }

            POPOVER_HTML = tool_html;

        }
    });

    // 初始化系统消息popover
    //样式改动，先暂时注释掉,不要删
    /*$('#stateMessage').popover({
        container:'#stateMessage',
        placement: 'bottom',
        trigger: 'hover',
        delay: { "show": 0, "hide": 300 },
        html: true,
        title: '最新消息',
        content: function() {
            return POPOVER_HTML+'<div class="popover-footer"><a href="/account/notification/">查看更多</a></div>';
        }
    });*/





    // 若点击消息内部链接，则认为消息已读
    $("body").on('click', "#stateMessageSection .unread a", function () {
        var notification_id = $(this).parent(".unread").attr("id");
        $.ajax({
            type:'POST',
            cache : false,
            headers: { "cache-control": "no-cache" },
            dataType: "json",
            url: '/account/read_notification/',
            data: 'ids='+notification_id,
            success:function (msg) {}
        })
    });

    // //若有表格，则初始化表格拖拽
    // if($("#grid-data").length!=0){
    //     $("#grid-data").colResizable({
    //         fixed:false,
    //         liveDrag:true,
    //         draggingClass:"dragging"
    //     });
    // }


    $(".state-message-icon").hover(function(){
       $(".state-message-icon").addClass("icon-color");
    },function(){
        $(".state-message-icon").removeClass("icon-color");
    });

    $(".state-message-icon").click(function(){
        window.location.href="/account/notification/";
    });



});



// set cookie
function setCookie(c_name,value){
    document.cookie=c_name+ "=" +escape(value);
}

// get cookie
function getCookie(c_name){
    if(document.cookie.length>0){
        c_start=document.cookie.indexOf(c_name + "=")
        if(c_start!=-1){
            c_start=c_start + c_name.length+1;
            c_end=document.cookie.indexOf(";",c_start);
            if (c_end==-1){
                c_end=document.cookie.length
            }
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

// 退出登录(清空cookie,session&&sessionId)
$("#logoutBtn").click(function (e) {
    e.stopPropagation();
    e.preventDefault();

    $.ajax({
        type: "POST",
        cache : false,
        dataType: "json",
        url: "/account/logout",
        success: function(msg){
            var jump_url = msg.bizContent.url;
            window.location.href = jump_url;
        }
    });

})


// 显示发布成功对话框
function showSelOk(id, url, password,trialExamLink,type,isSkipLogin) {
    $('#sendForm').removeClass('hidden');
    $(".guide-pwd").addClass('hidden');

    $("#exam_url").text(url);
    if(isSkipLogin == 1){
        $('#sendForm').addClass('hidden');
    }
    if(password){
        $("#exam_password").html(password);
        $(".guide-pwd").removeClass('hidden');
    }
    if(type == 'exam'){
        var sendUrl = '/admin/exam_notice/' + id;
    }else {
        var sendUrl = '/course/course_notice/' + id;
    }
    var jumpUrl ='';
    createQrcode(url);

    $("#confirmOkBtn").attr("data-type", type).attr("data-id", id);
    $("#trialExamBtn").prop("disabled", false).attr("data-url", trialExamLink)
        .attr("data-id", id).attr("data-type", type);

    $('#okModal').modal();

    // $("#okModal .btn-div").click(function (e) {
    //     if(e.target.nodeName.toUpperCase() == 'BUTTON'){
    //         if(e.target.innerText == '确定' && type =='exam'){
    //             jumpUrl = '/account/admin/index';
    //         }else if(e.target.innerText == '确定' && type =='course'){
    //             jumpUrl = '/course/course_mgr';
    //         }else {
    //             jumpUrl = trialExamLink;
    //         }
    //         sendNotice(sendUrl,jumpUrl);
    //     }
    // });
}

//okmodal点击确定
$("#confirmOkBtn").click(function () {
    var type = $(this).attr("data-type");
    var id = $(this).attr("data-id");
    var jumpUrl = '', sendUrl = '';

    if(type=='exam'){
        jumpUrl = '/account/admin/index';
        sendUrl = '/admin/exam_notice/' + id;
    }else if(type == 'course'){
        jumpUrl = '/course/course_mgr';
        sendUrl = '/course/course_notice/' + id;
    }
    sendNotice(sendUrl,jumpUrl);
});

//okmodal点击考一下
$("#trialExamBtn").click(function () {
    var type = $(this).attr("data-type");
    var id = $(this).attr("data-id");
    var jumpUrl = $(this).attr("data-url"), sendUrl = '';

    if(type=='exam'){
        sendUrl = '/admin/exam_notice/' + id;
    }else if(type == 'course'){
        sendUrl = '/course/course_notice/' + id;
    }
    sendNotice(sendUrl,jumpUrl);
});

//生成二维码
function createQrcode(examUrl) {
    //二维码生成
    $("#invite-link-qrcode").html("");
    $("#invite-link-qrcode").qrcode({
        width: 150,
        height: 150,
        text: examUrl,
        background: "#FFF"
    });
    //clear canvas before download again
    $("#small").html("");
    $("#medium").html("");
    $("#large").html("");

    $("#small").qrcode({
        width: 560,
        height: 560,
        text: examUrl,
        background: "#FFF"
    });
    var download0 = $("#small canvas")[0];
    $("a[download-size=0]").click(function() {
        if (download0.msToBlob) {//IE9+浏览器下载二维码
            var blob = download0.msToBlob();
            window.navigator.msSaveBlob(blob, $("input[name=examName]").val() + "_二维码小.png");
        }else{ //其他浏览器下载二维码
            this.href = download0.toDataURL();
            this.download = $("input[name=examName]").val() + "_二维码小.png";
        }
    });

    $("#medium").qrcode({
        width: 1050,
        height: 1050,
        text: examUrl,
        background: "#FFF"
    });
    var download1 = $("#medium canvas")[0];
    $("a[download-size=1]").click(function() {
        if (download1.msToBlob) {//IE9+浏览器
            var blob = download1.msToBlob();
            window.navigator.msSaveBlob(blob, $("input[name=examName]").val() + "_二维码中.png");
        }else{
            this.href = download1.toDataURL();
            this.download = $("input[name=examName]").val() + "_二维码中.png";
        }
    });

    $("#large").qrcode({
        width: 3500,
        height: 3500,
        text: examUrl,
        background: "#FFF"
    });
    var download2 = $("#large canvas")[0];
    $("a[download-size=2]").click(function() {
        if (download2.msToBlob) {//IE9+浏览器
            var blob = download2.msToBlob();
            window.navigator.msSaveBlob(blob, $("input[name=examName]").val() + "_二维码大.png");
        }else {
            this.href = download2.toDataURL();
            this.download = $("input[name=examName]").val() + "_二维码大.png";
        }
    });
}

//发送通知
function sendNotice(url,jumpUrl) {
    // var dataForm = $('#sendForm').serialize();
    var sendWay ='';
    var isSendNotice = $("#sendForm input:checked").length;
    if(isSendNotice == 0){
        window.location.href = jumpUrl;
    }else {
        $('#sendForm input:checked').each(function(index,ele) {
            sendWay += $(ele).prop('id')+',';
        });
        sendWay = sendWay.substring(0,sendWay.length-1);
        $.ajax({
            type: "POST",
            cache: false,
            headers: { "cache-control": "no-cache" },
            dataType: "json",
            url: url,
            data: 'sendWay=' + sendWay,
            success: function (msg) {
                if (msg.success == true) {
                    $(".sendAnimation").addClass("sendTips");
                    // 动画完成后的动作
                    var compAnimation = $(".sendAnimation").get(0);
                    compAnimation.addEventListener("animationend", animationEndFunction(jumpUrl));
                } else {
                    alert(msg.desc);
                }
            }
        });
    }
}

// 提示动画完成后
function animationEndFunction(jumpUrl) {
    $('#okModal .modal-content').hide();
    $("#animationLoading").removeClass("hidden");
    setTimeout(function(){
        window.location.href = jumpUrl;
    },1000);
}