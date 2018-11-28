(function (window, $) {
    var submissionFlag = false;
    
    var numbersth = $("#numbersth").val();  //户号
    var numbersthError = $("#numbersth-error");
    var buildingname = $("#buildingname").val(); //栋号
    var buildingnameError = $("#buildingname-error");
    var roomname = $("#roomname").val(); //房号
    var roomnameError = $("#roomname-error");
    var communityid = $("#communityid").val();
    var serialnumber = $("#serialnumber").val();
    var concentrator = $("#concentrator").val();
    var username = $("#username").val();
    var usertel = $("#usertel").val();
    var dn = $("#dn").val();
    var manufacturer = $("#manufacturer").val();
    var ValveMeter = $("#ValveMeter").val();
    var madedate = $("#madedate").val();

    var deviceFlag = false;
    var flag1 = false;
    waterMeterEdit = {
        init: function () {
            var setting = {
                async: {
                    url: "/entm/user/oranizationtree/",
                    tyoe: "post",
                    enable: true,
                    autoParam: ["id"],
                    contentType: "application/json",
                    dataType: "json",
                    dataFilter: waterMeterEdit.ajaxDataFilter
                },
                view: {
                    dblClickExpand: false
                },
                data: {
                    simpleData: {
                        enable: true
                    }
                },
                callback: {
                    beforeClick: waterMeterEdit.beforeClick,
                    onClick: waterMeterEdit.onClick
                }
            };
            $.fn.zTree.init($("#ztreeDemo"), setting, null);
            // laydate.render({elem: '#installDate', theme: '#6dcff6'});
            // laydate.render({elem: '#procurementDate', theme: '#6dcff6'});
            waterMeterEdit.Initcommunity();
            waterMeterEdit.InitCallback();
            console.log('init')
        },
        beforeClick: function (treeId, treeNode) {
            var check = (treeNode);
            return check;
        },
        onClick: function (e, treeId, treeNode) {
            var zTree = $.fn.zTree.getZTreeObj("ztreeDemo"), nodes = zTree
                .getSelectedNodes(), v = "";
            n = "";
            nodes.sort(function compare(a, b) {
                return a.id - b.id;
            });
            for (var i = 0, l = nodes.length; i < l; i++) {
                n += nodes[i].name;
                v += nodes[i].uuid + ",";
            }
            if (v.length > 0)
                v = v.substring(0, v.length - 1);
            var cityObj = $("#zTreeOrganSel");
            cityObj.val(n);
            $("#groupId").val(v);
            $("#zTreeContent").hide();
        },
        //显示菜单
        showMenu: function () {
            if ($("#zTreeContent").is(":hidden")) {
                var inpwidth = $("#zTreeOrganSel").width();
                var spwidth = $("#zTreeOrganSelSpan").width();
                var allWidth = inpwidth + spwidth + 21;
                if (navigator.appName == "Microsoft Internet Explorer") {
                    $("#zTreeContent").css("width", (inpwidth + 7) + "px");
                } else {
                    $("#zTreeContent").css("width", allWidth + "px");
                }
                $(window).resize(function () {
                    var inpwidth = $("#zTreeOrganSel").width();
                    var spwidth = $("#zTreeOrganSelSpan").width();
                    var allWidth = inpwidth + spwidth + 21;
                    if (navigator.appName == "Microsoft Internet Explorer") {
                        $("#zTreeContent").css("width", (inpwidth + 7) + "px");
                    } else {
                        $("#zTreeContent").css("width", allWidth + "px");
                    }
                })
                $("#zTreeContent").show();
            } else {
                $("#zTreeContent").hide();
            }
            $("body").bind("mousedown", waterMeterEdit.onBodyDown);
        },
        //隐藏菜单
        hideMenu: function () {
            $("#zTreeContent").fadeOut("fast");
            $("body").unbind("mousedown", waterMeterEdit.onBodyDown);
        },
        onBodyDown: function (event) {
            if (!(event.target.id == "menuBtn" || event.target.id == "zTreeContent" || $(
                    event.target).parents("#zTreeContent").length > 0)) {
                waterMeterEdit.hideMenu();
            }
        },
        
        hideErrorMsg: function(){
            $("#error_label").hide();
        },
        Initcommunity: function(){
            //sim卡
            var url="/dmam/community/getCommunitySelect/";
            var parameter={};
            json_ajax("POST",url,"json",true,parameter, waterMeterEdit.initcommunityList);
            
        },
        initcommunityList: function(data){
                //集中器list
            var ConcentratorList = data.obj;
            // 初始化集中器数据
            var dataList = {value: []};
            if (ConcentratorList !== null && ConcentratorList.length > 0) {
                for (var i=0; i< ConcentratorList.length; i++) {
                    var obj = {};
                    obj.id = ConcentratorList[i].id;
                    obj.name = ConcentratorList[i].name;
                    dataList.value.push(obj);
                }
                
            }
            $("#communityid").bsSuggest({
                indexId: 1,  //data.value 的第几个数据，作为input输入框的内容
                indexKey: 0, //data.value 的第几个数据，作为input输入框的内容
                idField: "id",
                keyField: "name",
                effectiveFields: ["name"],
                searchFields:["id"],
                data: dataList
            }).on('onDataRequestSuccess', function (e, result) {
            }).on('onSetSelectValue', function (e, keyword, data) {
                // 当选择集中器
                // var vehicleId = keyword.id;
                // var url="/clbs/v/monitoring/command/getCommandParam";
                // var minotor = realTimeCommand.getMinotorObj(currentCommandType);
                // var parameter={"vid": vehicleId,"commandType":currentCommandType,"isRefer":true,"minotor":minotor};
                // json_ajax("POST",url,"json",true,parameter, realTimeCommand.setCommand);
            }).on('onUnsetSelectValue', function () {
            });
        
        },

        InitCallback: function(){
            //sim卡
            var url="/devm/concentrator/getConcentratorSelect/";
            var parameter={};
            json_ajax("POST",url,"json",true,parameter, waterMeterEdit.initConcentratorList);
            
        },
        initConcentratorList: function(data){
                //集中器list
            var ConcentratorList = data.obj;
            // 初始化集中器数据
            var dataList = {value: []};
            if (ConcentratorList !== null && ConcentratorList.length > 0) {
                for (var i=0; i< ConcentratorList.length; i++) {
                    var obj = {};
                    obj.id = ConcentratorList[i].id;
                    obj.name = ConcentratorList[i].name;
                    dataList.value.push(obj);
                }
                
            }
            $("#concentrator").bsSuggest({
                indexId: 1,  //data.value 的第几个数据，作为input输入框的内容
                indexKey: 0, //data.value 的第几个数据，作为input输入框的内容
                idField: "id",
                keyField: "name",
                effectiveFields: ["name"],
                searchFields:["id"],
                data: dataList
            }).on('onDataRequestSuccess', function (e, result) {
            }).on('onSetSelectValue', function (e, keyword, data) {
                // 当选择集中器
                // var vehicleId = keyword.id;
                // var url="/clbs/v/monitoring/command/getCommandParam";
                // var minotor = realTimeCommand.getMinotorObj(currentCommandType);
                // var parameter={"vid": vehicleId,"commandType":currentCommandType,"isRefer":true,"minotor":minotor};
                // json_ajax("POST",url,"json",true,parameter, realTimeCommand.setCommand);
            }).on('onUnsetSelectValue', function () {
            });
        
        },
        //组织树预处理函数
        ajaxDataFilter: function (treeId, parentNode, responseData) {
            waterMeterEdit.hideErrorMsg();//隐藏错误提示样式
            var isAdminStr = $("#isAdmin").attr("value");    // 是否是admin
            var isAdmin = isAdminStr == 'true';
            var userGroupId = $("#userGroupId").attr("value");  // 用户所属组织 id
            var userGroupName = $("#userGroupName").attr("value");  // 用户所属组织 name
            //如果根企业下没有节点,就显示错误提示(根企业下不能创建终端)
            if (responseData != null && responseData != "" && responseData != undefined && responseData.length >= 1) {
                if (!isAdmin) { // 不是admin，默认组织为当前组织
                    $("#groupId").val(userGroupId);
                    $("#zTreeOrganSel").val(userGroupName);
                } else { // admin，默认组织为树结构第一个组织
                    $("#groupId").val(responseData[0].uuid);
                    $("#zTreeOrganSel").attr("value", responseData[0].name);
                }
                return responseData;
            } else {
                waterMeterEdit.showErrorMsg("您需要先新增一个组织", "zTreeOrganSel");
                return;
            }
        },
        valueChange:function () { // 判断值是否改变
            var edit_numbersth = $("#numbersth").val();  //户号
            var edit_buildingname = $("#buildingname").val(); //栋号
            var edit_roomname = $("#roomname").val(); //房号
            var edit_communityid = $("#communityid").val();
            var edit_serialnumber = $("#serialnumber").val();
            var edit_concentrator = $("#concentrator").val();
            var edit_username = $("#username").val();
            var edit_usertel = $("#usertel").val();
            var edit_dn = $("#dn").val();
            var edit_manufacturer = $("#manufacturer").val();
            var edit_ValveMeter = $("#ValveMeter").val();
            var edit_madedate = $("#madedate").val();
            // 值已经发生改变
            if (numbersth != edit_numbersth || buildingname != edit_buildingname || roomname != edit_roomname || communityid != edit_communityid
                || serialnumber != edit_serialnumber || concentrator != edit_concentrator || username != edit_username || usertel != edit_usertel
                || dn != edit_dn || manufacturer != edit_manufacturer || madedate != edit_madedate || ValveMeter != edit_ValveMeter ) {
                    flag1 = true;
            } else { // 表单值没有发生改变
                
                flag1 = false;
            }
        },
        doSubmit: function () {
            console.log("1.flag1",flag1);
            console.log("1.deviceFlag",deviceFlag);
            waterMeterEdit.valueChange();
            console.log("2.flag1",flag1);
            console.log("2.deviceFlag",deviceFlag);
            if(flag1){
                if (submissionFlag) {  // 防止重复提交
                    return;
                } else {
                    
                    waterMeterEdit.nameValidates();
                    console.log("3.flag1",flag1);
                    console.log("3.deviceFlag",deviceFlag);
                    if ( deviceFlag) {
                        if (waterMeterEdit.validates()) {
                            submissionFlag = true;
                            $("#editForm").ajaxSubmit(function (data) {
                                var json = eval("(" + data + ")");
                                if (json.success) {
                                    $("#commonWin").modal("hide");
                                    layer.msg("修改成功");
                                    myTable.requestData();
                                } else {
                                    layer.msg(json.msg);
                                }
                            });
                        }
                    }
                }
            }else{
                $("#commonWin").modal("hide");
            }
        },
        nameValidates: function () {
        
            numbersth = $("#numbersth").val();
            buildingname = $("#buildingname").val()
            roomname = $("#roomname").val()
            
            
            if (numbersth == "") {
                numbersthError.html("请输入小区名称");
                numbersthError.show();
                deviceFlag = false;
            }else if (buildingname == "") {
                buildingnameError.html("请输入栋号");
                buildingnameError.show();
                deviceFlag = false;
            }else if (roomname == "") {
                roomnameError.html("请输入房号");
                roomnameError.show();
                deviceFlag = false;
            }else{
                waterMeterEdit.deviceAjax();
            }
            
        },
        validates: function () {
            return $("#editForm").validate({
                rules: {
                    
                    numbersth: {
                        required: true
                    },
                    belongto: {
                        required: true
                    },
                    vconcentrator1:{
                        required:true
                    }
                    
                },
                messages: {
                    numbersth: {
                        required: "户号不能为空",
                    },
                    belongto: {
                        required: "所属组织不能为空",
                        maxlength: publicSize50
                    },
                    vconcentrator1: {
                        required: "至少选择一个集中器",
                        
                    },
                    
                },
                submitHandler: function (form) {
                    // var typeVal = $("#deviceType").val();
                    // var name = $("#name").val();
                    // if (typeVal == "5") {
                    //     $("#name-error").html("请输入终端号，范围：1~20");
                    //     var reg = /^(?=.*[0-9a-zA-Z])[0-9a-zA-Z-]{1,20}$/;
                    //     if (!reg.test(name)) {
                    //         alert("请输入终端号，范围：1~20");
                    //         return;
                    //     }
                    // }
                }
            }).form();
        },
        
        showErrorMsg: function (msg, inputId) {
            if ($("#error_label_add").is(":hidden")) {
                $("#error_label_add").text(msg);
                $("#error_label_add").insertAfter($("#" + inputId));
                $("#error_label_add").show();
            } else {
                $("#error_label_add").is(":hidden");
            }
        },
        //错误提示信息隐藏
        hideErrorMsg: function () {
            $("#error_label_add").is(":hidden");
            $("#error_label_add").hide();
        },
        deviceAjax: function () {
            var edit_numbersth = $("#numbersth").val();  //户号
            var edit_buildingname = $("#buildingname").val(); //栋号
            var edit_roomname = $("#roomname").val(); //房号
            if(numbersth != edit_numbersth || buildingname != edit_buildingname || roomname != edit_roomname){
                $.ajax({
                        type: "post",
                        url: "/wirelessm/communitymeter/repetition/",
                        data: {"numbersth": numbersth,"buildingname":buildingname,"roomname":roomname},
                        success: function (d) {
                            var result = $.parseJSON(d);
                            // if (!result) {
                            if (result.success == false) {
                                numbersthError.html("小区名称已存在！");
                                numbersthError.show();
                                deviceFlag = false;
                            }
                            else {
                                numbersthError.hide();
                                deviceFlag = true;
                            }
                        }
                    }
                )
            }
            else{
                deviceFlag = true;
            }
        },
        
    }
    $(function () {
        $('input').inputClear();
        //初始化
        waterMeterEdit.init();
        
        $('input').inputClear();

        // $("#numbersth").on("change", function () {
        //     numbersth = $("#numbersth").val();
        //     waterMeterEdit.nameValidates();
        // });
        
        // $("#numbersth,#buildingname,#roomname").bind("input propertychange change", function (event) {
        //     numbersth = $("numbersth").val();
        //     buildingname = $("#buildingname").val()
        //     roomname = $("#roomname").val()
        //     $.ajax({
        //             type: "post",
        //             url: "/wirelessm/communitymeter/repetition/",
        //             data: {"numbersth": numbersth,"buildingname":buildingname,"roomname":roomname},
        //             success: function (d) {
        //                 var result = $.parseJSON(d);
        //                 if (!result) {
        //                     numbersthError.html("该户号已存在！");
        //                     numbersthError.show();
        //                     deviceFlag = false;
        //                 }
        //                 else {
        //                     waterMeterEdit.nameValidates();
        //                 }
        //             }
        //         }
        //     )
        // });

        //显示菜单
        $("#zTreeOrganSel").bind("click", waterMeterEdit.showMenu);
        //提交
        $("#doSubmit").bind("click", waterMeterEdit.doSubmit);
    })
})(window, $)
