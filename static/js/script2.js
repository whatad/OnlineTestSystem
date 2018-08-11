    // these are global constant
    var LOCAL_URL = window.location.href;
    var USER_ROLE = 'admin';
    var rights='8';
    var surname="scnu_cs";
    var adjust_t,adjust_l;//对引导层位置进行调整的两个变量
    var tool_html='';//消息内容
    var tool_count=0;//消息数目
    var user_id="4735189";

    $(function () {
        

        // 更新消息已读
        $("#getChangeBtn").click(function (e) {
            e.preventDefault();

            $.ajax({
                url: '',//////https://admin.kaoshixing.com/admin/read_public',
                type: 'get',
                cache: false,
                dataType: 'json',
                success: function (msg) {
                    $("#changeLogModal").modal('hide');
                }
            })
        });

    });


    $(document).ready(function(){

        $("#user").click(function(){
            window.location.href="";//https://admin.kaoshixing.com/admin/admin_information";
            $(".unread-notice").hide();

        });

        //    自管理员点击添加考生，添加试题，创建考试时的权限判断
        $("#staff,#test,#exam").on("click",function(e){
            e.stopPropagation();
            e.preventDefault();
            var type = $(this).prop("id");
            var url = $(this).prop("href");
            $.ajax({
                type:"POST",
                cache:false,
                headers:{"cache-control": "no-cache"},
                dataType:"json",
                url:"",//https://admin.kaoshixing.com/admin/checkout_sub_admin_right",
                data:"type=" + type,
                success:function(msg){
                    if(msg.success){
                        window.location.href = url;
                    }else {
                        alert(msg.desc);
                    }
                }

            })
        });
    });
