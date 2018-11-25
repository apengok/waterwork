(function($,window){
    var isAdminStr = $("#isAdmin").attr("value");//是否是admin
    var AuthorizedDeadline = $("#userAuthorizationDate").attr("value");//获取当前用户授权截止日期
    var username = $("#username").val();//修改用户窗口弹出时,获取到默认的用户名
    var description  = $("#description").val();
    var zTreeStationSelEdit = $("#zTreeStationSelEdit").val();
    var usertype = $("#usertype").val();
    var relate_meter = $("#relate_meter").val();
    var serialnumber = $("#serialnumber").val();
    var simid = $("#simid").val();
    var meter = $("#meter").val();
    var metertype = $("input[type='radio']:checked").val();
    var dn = $("#dn").val();
    var madedate = $("#madedate").val();
    var lng = $("#lng").val();
    var lat = $("#lat").val();
    var focus = $("#focusVal").val();
    var biguser = $("#biguserVal").val();
    // var locate = $("#locate").val();

    var flag1 = false;
    var stationEdit = {
        //初始化
        init:function(){
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
                    beforeClick : stationEdit.beforeClick,
                    onClick : stationEdit.onClick

                }
            };
            $.fn.zTree.init($("#ztreeDemoEdit"), setting, null);
            laydate.render({elem: '#madedate',
              theme: '#6dcff6',
              done: function(value, date, endDate){
                var stdt=new Date();
                var etdt=new Date(value.replace("-","/"));
                if(stdt<=etdt){
                    $("#state").val("1");
                    $("#madedate-error").hide();
                }   
              }
           });
           
           $("[name=meter_type]").val([$("#metertypeEdit").val()]);

           $("#locatesel option").filter(function() {
                return $(this).text() == locate;
            }).attr('selected', true);
            
            if(focus == "1"){
                $("#focusBtn").removeClass("btn btn-default").attr("class","btn btn-primary")
            }

            if(biguser == "1"){
                $("#biguserBtn").removeClass("btn btn-default").attr("class","btn btn-primary")
            }

           // $('#relate_meter').val(relate_meter).trigger('onSetSelectValue', [relate_meter]);
        },
        beforeClick: function(treeId, treeNode){
            var check = (treeNode);
            return check;
        },
        onClick: function(e, treeId, treeNode){
            var zTree = $.fn.zTree.getZTreeObj("ztreeDemoEdit"), nodes = zTree
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
            $("body").bind("mousedown", stationEdit.onBodyDown);
        },
        hideMenu: function(){
            $("#zTreeContentEdit").fadeOut("fast");
            $("body").unbind("mousedown", stationEdit.onBodyDown);
        },
        onBodyDown: function(event){
            if (!(event.target.id == "menuBtn" || event.target.id == "zTreeContentEdit" || $(event.target).parents("#zTreeContentEdit").length > 0)) {
                stationEdit.hideMenu();
            }
        },
        valueChange:function () { // 判断值是否改变
            var edit_username = $("#username").val();//修改用户窗口弹出时,获取到默认的用户名
            var edit_description  = $("#description").val();
            var edit_zTreeStationSelEdit = $("#zTreeStationSelEdit").val();
            var edit_usertype = $("#usertype").val();
            var edit_relate_meter = $("#relate_meter").val();
            var edit_serialnumber = $("#serialnumber").val();
            var edit_simid = $("#simid").val();
            var edit_metertype = $("input[type='radio']:checked").val();
            var edit_dn = $("#dn").val();
            var edit_madedate = $("#madedate").val();
            var edit_lng = $("#lng").val();
            var edit_lat = $("#lat").val();
            var edit_locate = $("#locate").val();
            var edit_focus = $("#focusVal").val();
            var edit_biguser = $("#biguserVal").val();
            // 值已经发生改变
            if (username != edit_username || description != edit_description || zTreeStationSelEdit != edit_zTreeStationSelEdit || usertype != edit_usertype
                || madedate != edit_madedate || lng != edit_lng || lat != edit_lat || locate != edit_locate || focus != edit_focus || biguser != edit_biguser
                || relate_meter != edit_relate_meter ) {
                    flag1 = true;
            } else { // 表单值没有发生改变
                
                flag1 = false;
            }
        },
        locatechange:function(){
            var selectedopt = $("#locatesel :selected").text();
            $("#locate").val(selectedopt);
        },
        initUsertype:function(){
            var url="/dmam/station/findUsertypes/";
            var parameter={};
            // var parameter={"vid": currentVehicle,"commandType":treeNode.id,"isRefer":false};
            json_ajax("POST",url,"json",true,parameter, stationEdit.setUsertype);
        },
        setUsertype:function(data){
            if(data.success == true){
                // $("#phoneBookObject,#infoDemandObject,#eventObject,#gnssObject,#videoCameraObject,#telephoneObject,#locationObject,#specifyServerObject,#UpgradeObject,#terminalObject,#reportObject,#baseStationObject").val(vehicleList);
                if(data.msg == ''&&data.obj.operation!= null){
                    stationEdit.initUsertypeList(data.obj.operation);
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
            json_ajax("POST",url,"json",true,parameter, stationEdit.setRefer);
        },
        setRefer:function(data){
            if(data.success == true){
                // $("#phoneBookObject,#infoDemandObject,#eventObject,#gnssObject,#videoCameraObject,#telephoneObject,#locationObject,#specifyServerObject,#UpgradeObject,#terminalObject,#reportObject,#baseStationObject").val(vehicleList);
                if(data.msg == null&&data.obj.meterlist!= null){
                    stationEdit.initReferMeterList(data.obj.meterlist);
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
                    if(obj.name != ""){
                        dataList.value.push(obj);
                    }
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
                //更精确的查找
                console.log("onDataRequestSuccess");
                $(this).click().next().find('ul tr td').each(function() {
                    //拿缓存的信息作比对，比如文本
                    if ($(this).text() === meter) {
                        $(this).parents('tr').trigger('mousedown');
                        //终止继续 each
                        return false;
                    }
                });
            }).on('onSetSelectValue', function (e, keyword, data) {
                // 当选择meter
                

                var meterid = keyword.id;
                var url="/dmam/station/getmeterParam/";
                var parameter={"mid": meterid};
                json_ajax("POST",url,"json",true,parameter, stationEdit.setMeterParam);
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
                    $("#metertypeEdit").val(mtype);
                }
            }else{
                layer.msg(data.msg,{move:false});
            }
        },
        doSubmit: function(){
            
            stationEdit.valueChange();
            if (flag1){
                if(stationEdit.validates()){
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
                        username : {
                            required : true,
                            remote: {
                                type:"post",
                                async:false,
                                url:"/dmam/station/verifyusername/" ,
                                data:{
                                    username:function(){return $("#username").val();}
                                },
                                dataFilter:function(data){
                                    var resultData = $.parseJSON(data);
                                    if(resultData.success == true){
                                        return true;
                                    }else{
                                        if(username == $("#username").val()){
                                            return true;    //没有修改站点名
                                        }else{
                                            return false;
                                        }
                                    }
                                }
                            }
                        },
                        belongto :{
                            required : true,
                        },
                        meter : {
                            required : true,
                        }
                    },
                    messages : {
                        username : {
                            required : userNameNull,
                            remote:"该名称已被使用"
                        },
                        belongto :{
                            required : "请选择所属组织",
                        },
                        meter : {
                            required : "请关联表具"
                        }
                    }
                }).form();
            }else{
                return $("#editForm").validate({
                    rules : {
                        username : {
                            required : true,
                            remote: {
                                type:"post",
                                async:false,
                                url:"/dmam/station/verifyusername/" ,
                                data:{
                                    username:function(){return $("#username").val();}
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
                        belongto :{
                            required : true,
                        },
                        meter : {
                            required : true,
                        }
                    },
                    messages : {
                        user_name : {
                            required : userNameNull,
                            remote:"该名称已被使用"
                        },
                        belongto :{
                            required : "请选择所属组织",
                        },
                        meter : {
                            required : "请关联表具"
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
        
        stationEdit.initUsertype();
        
        stationEdit.initRefer();
        stationEdit.init();
        $('input').inputClear();
        var userId = $("#currentUserId").val();
        console.log('userId',$("#userId").val());
        console.log('current userId',$("#currentUserId").val());

        $(':radio:not(:checked)').attr('disabled', true);

        $("#locatesel").on("change",stationEdit.locatechange);

        if ($("#userId").val() == userId) {
            $("#zTreeStationSelEdit").attr("disabled","disabled"); // 禁用选择组织控件
            $("#state").attr("disabled","disabled"); // 禁用启停状态下拉选
            $("#authorizationDateEdit").attr("disabled","disabled"); // 禁用选择授权截止日期控件
        } else {
            $("#zTreeStationSelEdit").on("click",function(){stationEdit.showMenu(this)});
        }
        $("#doSubmitEdit").on("click",stationEdit.doSubmit);
    })
})($,window)
