(function($,window){
    var isAdminStr = $("#isAdmin").attr("value");//是否是admin
    var AuthorizedDeadline = $("#userAuthorizationDate").attr("value");//获取当前用户授权截止日期
    
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
        locatechange:function(){
            var selectedopt = $("#locatesel :selected").text();
            $("#locate").val(selectedopt);
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
                    $("#metertypeEdit").val(mtype);
                }
            }else{
                layer.msg(data.msg,{move:false});
            }
        },

        doSubmit: function(){
        
            if(stationAdd.validates()){
                $('#simpleQueryParam').val("");
                
                $("#addForm").ajaxSubmit(function(data) {
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
            
        },
        //校验
        validates: function(){
            var isAdmin = isAdminStr == 'true'
            console.log('isadmin?',isAdmin);
            if(isAdmin == true){
                return $("#addForm").validate({
                    rules : {
                        username : {
                            required : true,
                            remote: {
                                type:"post",
                                async:false,
                                url:"user/verification" ,
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
                return $("#addForm").validate({
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
            }

        },
        getsTheCurrentTime: function () {
            var time=$("#madedate").val();
                var nowDate = new Date();
                var startTime = parseInt(nowDate.getFullYear()+1)
                    + "-"
                    + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                        + parseInt(nowDate.getMonth() + 1)
                        : parseInt(nowDate.getMonth() + 1))
                    + "-"
                    + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                        : nowDate.getDate()) + " ";
                $("#madedate").val(startTime);
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

        $("#locatesel").on("change",stationAdd.locatechange);

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
