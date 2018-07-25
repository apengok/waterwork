(function($,window){
    var isAdminStr = $("#isAdmin").attr("value");//是否是admin
    var AuthorizedDeadline = $("#userAuthorizationDate").attr("value");//获取当前用户授权截止日期
    var userName = $("#username").val();//修改用户窗口弹出时,获取到默认的用户名
    var password  = $("#passwordEdit").val();
    var sendDownCommand = $("#sendDownCommand").val();
    var groupName = $("#zTreeStationSelEdit").val();
    var state = $("#state").val();
    var authorizationDate = $("#authorizationDateEdit").val();
    var fullName = $("#fullName").val();
    var gender = $("input[type='radio']:checked").val();
    var mobile = $("#mobile").val();
    var mail = $("#mail").val();
    var flag1 = false;
    var stationAdd = {
        //初始化
        init:function(){
            console.log('stationAdd.init ...');
            var setting = {
                async : {
                    url : "/entm/user/oranizationtree/",
                    tyoe : "post",
                    enable : true,
                    autoParam : [ "id" ],
                    contentType : "application/json",
                    dataType : "json",
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
                    beforeClick : stationAdd.beforeClick,
                    onClick : stationAdd.onClick

                }
            };
            $.fn.zTree.init($("#ztreeOrganEdit"), setting, null);
            laydate.render({elem: '#authorizationDateEdit',
              theme: '#6dcff6',
              done: function(value, date, endDate){
                var stdt=new Date();
                var etdt=new Date(value.replace("-","/"));
                if(stdt<=etdt){
                    $("#state").val("1");
                    $("#authorizationDate-error").hide();
                }   
              }
           });
           if(isAdminStr == 'false'){
                if(AuthorizedDeadline == "null"){ // 赋值为空字符串,方便判断
                    AuthorizedDeadline = "";
                }
           }else{
               //为administrator
               if(userName == "admin"){//如果是admin,取消下发口令文本框的隐藏
                   $("#sendAPassWord").removeClass("hidden");
               }
           }
        },
        beforeClick: function(treeId, treeNode){
            var check = (treeNode);
            return check;
        },
        onClick: function(e, treeId, treeNode){
            var zTree = $.fn.zTree.getZTreeObj("ztreeOrganEdit"), nodes = zTree
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
            var cityObj = $("#zTreeStationSelEdit");
            console.log('before:',$("#groupIds").val());
            $("#groupIds").val(v);
            $("#idstr").val(v);
            console.log('after:',$("#groupIds").val());
            cityObj.val(n);
            $("#zTreeContentEdit").hide();
        },
        showMenu: function(e){
            // 判断是否是当前用户,不能修改自己的组织 
            if ($("#zTreeContentEdit").is(":hidden")) {
                var width = $(e).parent().width();
                $("#zTreeContentEdit").css("width",width + "px");
                $(window).resize(function() {
                    var width = $(e).parent().width();
                    $("#zTreeContentEdit").css("width",width + "px");
                })
                $("#zTreeContentEdit").show();
            } else {
                $("#zTreeContentEdit").hide();
            }
            $("body").bind("mousedown", stationAdd.onBodyDown);
        },
        hideMenu: function(){
            $("#zTreeContentEdit").fadeOut("fast");
            $("body").unbind("mousedown", stationAdd.onBodyDown);
        },
        onBodyDown: function(event){
            if (!(event.target.id == "menuBtn" || event.target.id == "zTreeContentEdit" || $(event.target).parents("#zTreeContentEdit").length > 0)) {
                stationAdd.hideMenu();
            }
        },
        initUsertype:function(){
            var url="/dmam/station/findUsertypes/";
            var parameter={};
            // var parameter={"vid": currentVehicle,"commandType":treeNode.id,"isRefer":false};
            json_ajax("POST",url,"json",true,parameter, stationAdd.setUsertype);
        },
        setUsertype:function(data){
            if(data.success == true){
                // $("#phoneBookObject,#infoDemandObject,#eventObject,#gnssObject,#videoCameraObject,#telephoneObject,#locationObject,#specifyServerObject,#UpgradeObject,#terminalObject,#reportObject,#baseStationObject").val(vehicleList);
                if(data.msg == ''&&data.obj.operation!= null){
                    stationAdd.initUsertypeList(data.obj.operation);
                }
            }else{
                layer.msg(data.msg,{move:false});
            }
        },
        initUsertypeList: function(data){
        
            //meter list
            var usertypelist = data;

            // 初始化车辆数据
            var dataList = {value: []};
            if (usertypelist !== null && usertypelist.length > 0) {
                for (var i=0; i< usertypelist.length; i++) {
                    var obj = {};
                    obj.id = usertypelist[i].id;
                    obj.name = usertypelist[i].userType;
                    dataList.value.push(obj);
                }
                
            }
            $("#usertype").bsSuggest({
                indexId: 1,  //data.value 的第几个数据，作为input输入框的内容
                indexKey: 0, //data.value 的第几个数据，作为input输入框的内容
                idField: "id",
                keyField: "name",
                effectiveFields: ["name"],
                searchFields:["id"],
                data: dataList
            }).on('onDataRequestSuccess', function (e, result) {
            }).on('onSetSelectValue', function (e, keyword, data) {
                // 当选择meter
                
            }).on('onUnsetSelectValue', function () {
            });
            
        },
        initRefer:function(){
            var url="/dmam/station/getmeterlist/";
            var parameter={};
            // var parameter={"vid": currentVehicle,"commandType":treeNode.id,"isRefer":false};
            json_ajax("POST",url,"json",true,parameter, stationAdd.setRefer);
        },
        setRefer:function(data){
            if(data.success == true){
                // $("#phoneBookObject,#infoDemandObject,#eventObject,#gnssObject,#videoCameraObject,#telephoneObject,#locationObject,#specifyServerObject,#UpgradeObject,#terminalObject,#reportObject,#baseStationObject").val(vehicleList);
                if(data.msg == null&&data.obj.meterlist!= null){
                    stationAdd.initReferMeterList(data.obj.meterlist);
                }
            }else{
                layer.msg(data.msg,{move:false});
            }
        },
        initReferMeterList: function(data){
        
            //meter list
            var meterlist = data;
            console.log('meterlist:',meterlist);

            // 初始化车辆数据
            var dataList = {value: []};
            if (meterlist !== null && meterlist.length > 0) {
                for (var i=0; i< meterlist.length; i++) {
                    var obj = {};
                    obj.id = meterlist[i].id;
                    obj.name = meterlist[i].serialnumber;
                    dataList.value.push(obj);
                }
                
            }
            $("#relate_meter").bsSuggest({
                indexId: 1,  //data.value 的第几个数据，作为input输入框的内容
                indexKey: 0, //data.value 的第几个数据，作为input输入框的内容
                idField: "id",
                keyField: "name",
                effectiveFields: ["name"],
                searchFields:["id"],
                data: dataList
            }).on('onDataRequestSuccess', function (e, result) {
            }).on('onSetSelectValue', function (e, keyword, data) {
                // 当选择meter
                

                var meterid = keyword.id;
                var url="/dmam/station/getmeterParam/";
                var parameter={"mid": meterid};
                json_ajax("POST",url,"json",true,parameter, stationAdd.setMeterParam);
            }).on('onUnsetSelectValue', function () {
            });
            
        },
        setMeterParam:function(data){
            if(data.success == true){
                if(data.msg == null&&data.obj != null){
                    var mtype = data.obj.metertype;
                    $("#serialnumber").val(data.obj.serialnumber);
                    $("#simid").val(data.obj.simid);
                    $("#dn").val(data.obj.dn);
                    // $('input:radio[name="meter_type"]').filter('[value="Male"]').attr('checked', true);
                    $("[name=meter_type]").val([mtype]);
                }
            }else{
                layer.msg(data.msg,{move:false});
            }
        },
        valueChange:function () { // 判断值是否改变
            var editPassword = $("#passwordEdit").val();
            var editSendDownCommand = $("#sendDownCommand").val();
            var editGroupName = $("#zTreeStationSelEdit").val();
            var editState = $("#state").val();
            var editAuthorizationDate = $("#authorizationDateEdit").val();
            var editFullName = $("#fullName").val();
            var editGender = $("input[type='radio']:checked").val();
            var editMobile = $("#mobile").val();
            var editMail = $("#mail").val();
            // 值已经发生改变
            if (password != editPassword || sendDownCommand != editSendDownCommand || groupName != editGroupName || state != editState
                || authorizationDate != editAuthorizationDate || fullName != editFullName || gender != editGender || mobile != editMobile || mail != editMail) {
                    flag1 = true;
            } else { // 表单值没有发生改变
                var timestamp = Date.parse(new Date(editAuthorizationDate));
                timestamp = timestamp / 1000;
                var timestamp2 = Date.parse(new Date(AuthorizedDeadline));
                timestamp2 =  timestamp2 / 1000;
                if (timestamp > timestamp2) { // 如果页面获取的授予权截止日期小于等于当前登录用户的授权截止日期,则需要验证
                    flag1 = true;
                    return;
                }
                flag1 = false;
            }
        },
        doSubmit: function(){
            console.log("pawd:",$("#passwordEdit").attr("value"));
            stationAdd.valueChange();
            if (flag1){
                if(stationAdd.validates()){
                    $('#simpleQueryParam').val("");
                    //验证通过后,获取到用户名，与窗口加载时的用户名比较,看用户是否修改过用户名
                    var nowUserName = $("#username").val();
                    if(nowUserName === userName){
                        //如果没有修改用户名
                        //则重新赋值
                        $("#sign").val("1");
                    }
                    $("#editForm").ajaxSubmit(function(data) {
                        if (data != null) {
                            var result =  $.parseJSON(data);
                            console.log(result);
                            if (result.success == true) {
                                if (result.obj.flag == 1){
                                    $("#commonLgWin").modal("hide");
                                    layer.msg(publicEditSuccess,{move:false});
                                    myTable.refresh()
                                }else{
                                    if(date != null){
                                        layer.msg(publicEditError,{move:false});
                                    }
                                }
                            }else{
                                layer.msg(result.obj.errMsg,{move:false});
                            }
                        }
                    });
                    // $("#commonLgWin").modal("hide"); // 关闭窗口
                }
            } else {
                $("#commonLgWin").modal("hide"); // 关闭窗口
            }
        },
        //校验
        validates: function(){
            var isAdmin = isAdminStr == 'true'
            console.log('isadmin?',isAdmin);
            if(isAdmin == true){
                return $("#editForm").validate({
                    rules : {
                        user_name : {
                            required : true,
                            stringCheck:true,
                            maxSize : 25,
                            minSize : 4
                        },
                        real_name : {
                            maxlength : 20,
                            minlength : 2
                        },
                        password : {
                            // required : true,
                            minlength : 6,
                            maxlength : 25
                        },
                        sendDownCommand : {
                            minlength : 6,
                            maxlength : 25
                        },
                        belongto : {
                            required : true
                        },
                        expire_date : {
                            selectDate : true
                        },
                        email : {
                            email : true,
                            maxlength : 60
                        },
                        phone_number : {
                            isTel : true
                        }
                    },
                    messages : {
                        user_name : {
                            required : userNameNull,
                            stringCheck : userNameError,
                            maxSize : publicSize25,
                            minSize : userNameMinLength
                        },
                        real_name : {
                            required : publicNull,
                            maxlength : publicSize20,
                            minlength : publicMinSize2Length
                        },
                        password : {
                            // required  : "密码不能为空",
                            minlength : passwordMinLength,
                            maxlength : publicSize25
                        },
                        sendDownCommand : {
                            minlength : publicMinSize6Length,
                            maxlength : publicSize25
                        },
                        belongto : {
                            required : publicSelectGroupNull
                        },
                        expire_date : {
                            selectDate : usernameAuthorizationToday
                        },
                        mail : {
                            email :emailError,
                            maxlength : publicSize60
                        },
                        mobile : {
                            isTel : phoneError
                        }
                    }
                }).form();
            }else{
                return $("#editForm").validate({
                    rules : {
                        user_name : {
                            required : true,
                            stringCheck:true,
                            maxSize : 25,
                            minSize : 4
                        },
                        real_name : {
                            // required : true,
                            maxlength : 20,
                            minlength : 2
                        },
                        password : {
                            minlength : 6,
                            maxlength : 25
                        },
                        belongto : {
                            required : true
                        },
                        expire_date : {
                            required:true,
                            selectDate : true,
                            remote: {
                                type:"post",
                                async:false,
                                url:"user/verification" ,
                                data:{
                                    expire_date:function(){return $("#authorizationDateEdit").val();}
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
                        email : {
                            email : true,
                            maxlength : 60
                        },
                        phone_number : {
                            isTel : true
                        }
                    },
                    messages : {
                        user_name : {
                            required : userNameNull,
                            stringCheck : userNameError,
                            maxSize : publicSize25,
                            minSize : userNameMinLength
                        },
                        real_name : {
                            required : publicNull,
                            maxlength : publicSize20,
                            minlength : publicMinSize2Length
                        },
                        password : {
                            minlength : passwordMinLength,
                            maxlength : publicSize25
                        },
                        belongto : {
                            required : userGroupSelectNull
                        },
                        expire_date : {
                            required:usernameAuthorizationDateNull,
                            selectDate:usernameAuthorizationToday,
                            remote:"该用户的授权截止日期不能大于您自己的授权截止日期("+AuthorizedDeadline+")"
                        },
                        email : {
                            email :emailError,
                            maxlength : publicSize60
                        },
                        phone_number : {
                            isTel : phoneError
                        }
                    }
                }).form();
            }

        },
        getsTheCurrentTime: function () {
            var time=$("#authorizationDateEdit").val();
                var nowDate = new Date();
                var startTime = parseInt(nowDate.getFullYear()+1)
                    + "-"
                    + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                        + parseInt(nowDate.getMonth() + 1)
                        : parseInt(nowDate.getMonth() + 1))
                    + "-"
                    + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                        : nowDate.getDate()) + " ";
                $("#authorizationDateEdit").val(startTime);
        },
    }
    $(function(){
        var myTable;
        stationAdd.init();
        stationAdd.initUsertype();
        stationAdd.initRefer();
        $('input').inputClear();
        var userId = $("#currentUserId").val();
        console.log('userId',$("#userId").val());
        console.log('current userId',$("#currentUserId").val());

        $(':radio:not(:checked)').attr('disabled', true);

        // if ($("#userId").val() == userId) {
        //     $("#zTreeStationSelEdit").attr("disabled","disabled"); // 禁用选择组织控件
        //     $("#state").attr("disabled","disabled"); // 禁用启停状态下拉选
        //     $("#authorizationDateEdit").attr("disabled","disabled"); // 禁用选择授权截止日期控件
        // } else {
        //     $("#zTreeStationSelEdit").on("click",function(){stationAdd.showMenu(this)});
        // }
        $("#zTreeStationSelEdit").on("click",function(){stationAdd.showMenu(this)});
        $("#doSubmitEdit").on("click",stationAdd.doSubmit);
    })
})($,window)
