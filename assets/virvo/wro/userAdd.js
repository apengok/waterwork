(function($,window){
    var isAdminStr = $("#isAdmin").attr("value"); // 是否是admin
    var AuthorizedDeadline = $("#userAuthorizationDate").attr("value");//获取当前用户授权截止日期
    var isAdmina;
    var userAdd = {
        init: function(){
            var setting = {
                async : {
                    url : "user/oranizationtree/",
                    tyoe : "post",
                    enable : true,
                    autoParam : [ "id" ],
                    contentType : "application/json",
                    dataType : "json",
                    dataFilter: userAdd.ajaxDataFilter
                },
                view : {
                    dblClickExpand : false
                },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    beforeClick : userAdd.beforeClick,
                    onClick : userAdd.onClick

                }
            };
            $.fn.zTree.init($("#ztreeDemoAdd"), setting, null);
            laydate.render({elem: '#authorizationDateAdd',
                theme: '#6dcff6',
                done: function(value, date, endDate){
                    $("#authorizationDate-error").hide();
                }
            });
            if(isAdminStr == 'false'){
                if(AuthorizedDeadline == "null"){
                    AuthorizedDeadline = "";
                }
                if(AuthorizedDeadline != null && AuthorizedDeadline != "" && AuthorizedDeadline !="null"){//如果用户有授权截止日器,改变页面日期的值为当前用户的授权截止日期
                    $("#authorizationDateAdd").val(AuthorizedDeadline);
                }else{//如果用户没有授权截止日期,则更改页面时间为当天日期+1年
                    userAdd.getsTheCurrentTime();
                }
            }else {
                userAdd.getsTheCurrentTime();
            }

        },
        beforeClick: function(treeId, treeNode){
            var check = (treeNode);
            return check;
        },
        onClick: function(e, treeId, treeNode){
            var zTree = $.fn.zTree.getZTreeObj("ztreeDemoAdd"), nodes = zTree
                .getSelectedNodes(), v = "";
            n = "";
            nodes.sort(function compare(a, b) {
                return a.id - b.id;
            });
            for (var i = 0, l = nodes.length; i < l; i++) {
                n += nodes[i].name;
                v += nodes[i].id + ",";
            }
            if (v.length > 0)
                v = v.substring(0, v.length - 1);
            var cityObj = $("#zTreeCitySelAdd");

            $("#groupId").val(v);
            cityObj.val(n);
            $("#zTreeContentAdd").hide();
        },
        showMenu: function(e){
            if ($("#zTreeContentAdd").is(":hidden")) {
                var width = $(e).parent().width();
                $("#zTreeContentAdd").css("width",width + "px");
                $(window).resize(function() {
                    var width = $(e).parent().width();
                    $("#zTreeContentAdd").css("width",width + "px");
                })
                $("#zTreeContentAdd").show();
            } else {
                $("#zTreeContentAdd").hide();
            }

            $("body").bind("mousedown", userAdd.onBodyDown);
        },
        hideMenu: function(){
            $("#zTreeContentAdd").fadeOut("fast");
            $("body").unbind("mousedown", userAdd.onBodyDown);
        },
        onBodyDown: function(event){
            if (!(event.target.id == "menuBtn" || event.target.id == "zTreeContentAdd" || $(event.target).parents("#zTreeContentAdd").length > 0)) {
                userAdd.hideMenu();
            }
        },
        //组织树预处理函数
        ajaxDataFilter: function(treeId, parentNode, responseData){
            userAdd.hideErrorMsg();//清除错误提示样式
            var isAdmin = isAdminStr == 'true';
            isAdmina = isAdmin;
            //如果根企业下没有节点,就显示错误提示(根企业下不能新建用户)
            if(responseData != null && responseData != undefined && responseData != "" && responseData.length >= 1){
                if($("#groupId").val()==""){
                    $("#groupId").val(responseData[0].id);
                    $("#zTreeCitySelAdd").attr("value",responseData[0].name);
                }
                return responseData;
            }else{
                userAdd.showErrorMsg(userGroupNull,"zTreeCitySelAdd");
                return;
            }
        },
        // 提交
        doSubmit: function(){
        var sexvalue=$("input[name='sex']:checked").val();
        $("#gender").val(sexvalue);
            if(isAdmina == true){
                userAdd.validates();
                if(userAdd.validates()){
                    $("#addForm").ajaxSubmit(function(data) {
                        if (data != null) {
                            var result =  $.parseJSON(data);
                            if (result.success) {
                                if (result.obj.flag == 1){
                                    $("#commonWin").modal("hide");
                                    layer.msg(publicAddSuccess,{move:false});
                                    myTable.requestData();
                                }else{
                                    layer.msg(result.msg,{move:false});
                                }
                            }else{
                                layer.msg(result.msg,{move:false});
                            }
                        }
                    });
                }
            }else{
                userAdd.fulatAdminValidates();
                if(userAdd.fulatAdminValidates()){
                    $("#addForm").ajaxSubmit(function(data) {
                        if (data != null) {
                            var result = $.parseJSON(data);
                            if (result.success) {
                                if (result.obj.flag == 1){
                                    $("#commonWin").modal("hide");
                                    layer.msg(publicAddSuccess,{move:false});
                                    myTable.requestData();
                                }else{
                                    layer.msg(result.msg,{move:false});
                                }
                            }else{
                                layer.msg(result.msg,{move:false});//result.obj.errMsg
                            }
                        }
                    });
                }
            }

        },
        //校验
        validates: function(){
            return $("#addForm").validate({
                rules : {
                    username : {
                        required : true,
                        stringCheck : true,
                        maxSize : 25,
                        minSize : 4,
                        remote :{
                            type:"post",
                            async:false,
                            url:"user/verifyUserName/" ,
                            data:{
                                userName:function(){
                                    return $("#usernameAdd").val();}
                            },
                            dataFilter:function(data){
                                var resultData = $.parseJSON(data);
                                if(resultData.success == true){
                                    return true;
                                }else{
                                    if(resultData.msg != null && resultData.msg != ""){
                                        layer.msg(resultData.msg,{move:false});
                                    }else{
                                        return false;
                                    }
                                }
                            }
                        }
                    },
                    fullName : {
                        maxlength : 20,
                        minlength : 2
                    },
                    password : {
                        required : true,
                        minlength : 6,
                        maxlength : 25
                    },
                    password1 : {
                        required : true,
                        minlength : 6,
                        equalTo : "#passwordAdd"
                    },
                    groupName : {
                        required : true
                    },
                    authorizationDate : {
                        selectDate : true
                    },
                    mail : {
                        email : true,
                        maxlength : 60
                    },
                    mobile : {
                        isTel : true
                    }
                },
                messages : {
                    username : {
                        required : userNameNull,
                        stringCheck : userNameError,
                        maxSize : publicSize25,
                        minSize : userNameMinLength,
                        remote : usernameExists
                    },
                    fullName : {
                        maxlength : publicSize20,
                        minlength : userNameMixlength
                    },
                    password : {
                        required : passWordNull,
                        maxlength : publicSize25,
                        minlength :  passwordMinLength
                    },
                    password1 : {
                        required : passWordNull,
                        minlength :  passwordMinLength,
                        maxlength : publicSize25,
                        equalTo : passwordCompareNull
                    },
                    groupName : {
                        required : publicSelectGroupNull
                    },
                    authorizationDate : {
                        selectDate : usernameAuthorizationToday
                    },
                    mail : {
                        email : emailError,
                        maxlength : publicSize60
                    },
                    mobile : {
                        isTel : phoneError
                    }
                }
            }).form();
        },
        fulatAdminValidates:function () {
            return $("#addForm").validate({
                rules : {
                    username : {
                        required : true,
                        stringCheck : true,
                        maxSize : 25,
                        minSize : 4,
                        remote :{
                            type:"post",
                            async:false,
                            url:"user/verifyUserName/" ,
                            data:{
                                userName:function(){
                                    return $("#usernameAdd").val();}
                            },
                            dataFilter:function(data){
                                var resultData = $.parseJSON(data);
                                if(resultData.success == true){
                                    return true;
                                }else{
                                    if(resultData.msg != null && resultData.msg != ""){
                                        layer.msg(resultData.msg,{move:false});
                                    }else{
                                        return false;
                                    }
                                }
                            }
                        }
                    },
                    fullName : {
                        maxlength : 20,
                        minlength : 2
                    },
                    password : {
                        required : true,
                        minlength : 6,
                        maxlength : 25
                    },
                    password1 : {
                        required : true,
                        minlength : 6,
                        equalTo : "#passwordAdd"
                    },
                    groupName : {
                        required : true
                    },
                    authorizationDate : {
                        required:true,
                        selectDate :true,
                        remote: {
                            type:"post",
                            async:false,
                            url:"user/verification/" ,
                            data:{
                                authorizationDate:function(){
                                    return $("#authorizationDateAdd").val();}
                            },
                            dataFilter:function(data){
                                var resultData = $.parseJSON(data);
                                if(resultData.success == true){
                                    return true;
                                }else{
                                    if(resultData.msg != null && resultData.msg != ""){
                                        layer.msg(resultData.msg,{move:false});
                                    }else{
                                        return false;
                                    }
                                }
                            }
                        }
                    },
                    mail : {
                        email : true,
                        maxlength : 60
                    },
                    mobile : {
                        isTel : true
                    }
                },
                messages : {
                    username : {
                        required : userNameNull,
                        stringCheck : userNameError,
                        maxSize : publicSize25,
                        minSize : userNameMinLength,
                        remote : usernameExists
                    },
                    fullName : {
                        maxlength : publicSize20,
                        minlength : publicMinSize2Length
                    },
                    password : {
                        required : passWordNull,
                        maxlength : publicSize25,
                        minlength :  passwordMinLength
                    },
                    password1 : {
                        required : passWordNull,
                        minlength :  passwordMinLength,
                        maxlength : publicSize25,
                        equalTo : passwordCompareNull
                    },
                    groupName : {
                        required : publicSelectGroupNull
                    },
                    authorizationDate : {
                        required:usernameAuthorizationDateNull,
                        selectDate : usernameAuthorizationToday,
                        remote:"新建用户的授权截止日期不能大于您自己的授权截止日期("+AuthorizedDeadline+")"
                    },
                    mail : {
                        email : emailError,
                        maxlength :publicSize60
                    },
                    mobile : {
                        isTel : phoneError
                    }
                }
            }).form();
        },
        getsTheCurrentTime: function () {
            var time=$("#authorizationDateAdd").val();
            if(time == null || time == "" || time == "null"){
                var nowDate = new Date();
                startTime = parseInt(nowDate.getFullYear()+1)
                    + "-"
                    + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                        + parseInt(nowDate.getMonth() + 1)
                        : parseInt(nowDate.getMonth() + 1))
                    + "-"
                    + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                        : nowDate.getDate()) + " ";
                $("#authorizationDateAdd").val(startTime);
            }
        },
        showErrorMsg: function(msg, inputId){
            if ($("#error_label_add").is(":hidden")) {
                $("#error_label_add").text(msg);
                $("#error_label_add").insertAfter($("#" + inputId));
                $("#error_label_add").show();
            } else {
                $("#error_label_add").is(":hidden");
            }
        },
        //错误提示信息隐藏
        hideErrorMsg: function(){
            $("#error_label_add").is(":hidden");
            $("#error_label_add").hide();
        },
        closeErrClass:function () {
            userAdd.hideErrorMsg();
        },
        clearPreviousValue :function(){ //清除Validates验证缓存
            if($(".remote").data("previousValue")){
                $(".remote").data("previousValue").old = null;
            }
        },
    }
    $(function(){       
        var myTable;
        userAdd.init();   
        $('input').inputClear();
        $("#zTreeCitySelAdd").on("click",function(){userAdd.showMenu(this)});
        $("#doSubmitAdd").on("click",userAdd.doSubmit);
        $("#closeAdd").on("click",userAdd.closeErrClass);
        $("#usernameAdd").on("change",userAdd.clearPreviousValue);
    })
})($,window)
