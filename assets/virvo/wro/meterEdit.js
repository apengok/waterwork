(function(window,$){
    var bindId = $("#bindId").val();
    var installTime = $("#installTime").val();
    var serialnumber = $("#serialnumber").val();
    var oldDeviceNumber = $("#serialnumber").val();
    var deviceType = $("#deviceType").val();
    var serialnumberError = $("#serialnumber-error");
    var deviceFlag = false;
    var fts="";
    editMeterManagement = {
        init: function () {
            if (bindId != null && bindId != '') {
                $("#serialnumber").attr("readonly", true);
                $("#deviceType").attr("disabled", true);
                $("#bindMsg").attr("hidden", false);
            }
            var setting = {
                async: {
                    url: "/entm/user/oranizationtree/",
                    tyoe: "post",
                    enable: true,
                    autoParam: ["id"],
                    contentType: "application/json",
                    dataType: "json",
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
                    beforeClick: editMeterManagement.beforeClick,
                    onClick: editMeterManagement.onClick
                }
            };
            $.fn.zTree.init($("#ztreeDemo"), setting, null);
            fts = $("#functionalType").val();//获取当前终端通讯类型
            // laydate.render({elem: '#installDateEdit', theme: '#6dcff6'});
            // laydate.render({elem: '#procurementDateEdit', theme: '#6dcff6'});
        },
        beforeClick: function (treeId, treeNode) {
            var check = (treeNode);
            return check;
        },
        onClick: function (e, treeId, treeNode) {
            var zTree = $.fn.zTree.getZTreeObj("ztreeDemo"), nodes = zTree
                .getSelectedNodes(), n = "";
            v = "";
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
            cityObj.attr("value", v);
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
            $("body").bind("mousedown", editMeterManagement.onBodyDown);
        },
        hideMenu: function () {
            $("#zTreeContent").fadeOut("fast");
            $("body").unbind("mousedown", editMeterManagement.onBodyDown);
        },
        onBodyDown: function (event) {
            if (!(event.target.id == "menuBtn" || event.target.id == "zTreeContent" || $(
                    event.target).parents("#zTreeContent").length > 0)) {
                editMeterManagement.hideMenu();
            }
        },
        serialnumberValidates: function () {
            if (serialnumber == "") {
                serialnumberError.html("请输入终端号，范围：1~20");
                serialnumberError.show();
                deviceFlag = false;
            }
            else {
                editMeterManagement.deviceAjax();
            }
            
        },
        deviceAjax: function () {
            serialnumber = $("#serialnumber").val();
            if (oldDeviceNumber != serialnumber) {
                $.ajax({
                        type: "post",
                        url: "/devm/meter/repetition/",
                        data: {serialnumber: serialnumber},
                        success: function (d) {
                            var result = $.parseJSON(d);
                            if (!result) {
                                serialnumberError.html("终端号已存在！");
                                serialnumberError.show();
                                deviceFlag = false;
                            }
                            else {
                                serialnumberError.hide();
                                deviceFlag = true;
                            }
                        }
                    }
                )
            }else{
                deviceFlag = true;
            }
        },
        validates: function(){
             return $("#editForm").validate({
                 rules : {
                 /*serialnumber : {
                    required : true,
                    checkDeviceNumber : "#deviceType",                  
                    isRightfulString : true,
                    remote: {
                        type:"post",
                        async:false,
                        url:"/clbs/m/basicinfo/equipment/device/repetition" ,
                        dataType:"json",
                        data:{
                              username:function(){return $("#serialnumber").val();}
                         },
                         dataFilter: function(data, type) {
                             var oldV = $("#scn").val();
                            var newV = $("#serialnumber").val();
                            var data2 = data;
                            if (oldV == newV) {
                                return true;
                            } else {
                                if (data2 == "true"){
                                        return true;
                                 } else {
                                        return false;
                                 }
                            }
                          }
                       }
                },*/
                belongto: {
                        required: true
                    },
                    simid: {
                        required: true,
                        maxlength: 50
                    },
                    mtype: {
                        required: true,
                        maxlength: 50
                    },
                    // isVideo: {
                    //     maxlength: 6
                    // },
                    protocol: {
                        maxlength: 64
                    },
                    check_cycle: {
                        maxlength: 11
                    },
                    dn: {
                        required: false,
                        maxlength: 6
                    },
                    // manuFacturer: {
                    //     maxlength: 100
                    // },
                    R: {
                        maxlength: 100
                    },
                    q3: {
                        required: false,
                        maxlength: 50
                    }
            },
            messages : {
                /*serialnumber : {
                    required: serialnumberNull,
                    checkDeviceNumber : serialnumberError,
                    isRightfulString :  serialnumberError,
                    remote: serialnumberExists
                },*/
                belongto: {
                        required: "所属组织不能为空",
                        maxlength: publicSize50
                    },
                    simid: {
                        required: publicNull
                    },
                    mtype: {
                        required: deviceTypeNull,
                        maxlength: publicSize50
                    },
                    protocol: {
                        required: publicNull,
                        maxlength: publicSize50
                    },
                    check_cycle: {
                        maxlength: publicSize6
                    },
                    dn: {
                        maxlength: publicSize64
                    },
                    R: {
                        maxlength: publicSize10
                    },
                    q3: {
                        required: publicNull,
                        maxlength: publicSize6
                    }
           }}).form();
        },
        //提交
        doSubmit: function(){
            deviceType = $("#deviceType").val();
            serialnumber = $("#serialnumber").val();
            editMeterManagement.serialnumberValidates();
            if ($("#serialnumber").val() != "" && deviceFlag) {
                if (editMeterManagement.validates()) {
                    $("#editForm").ajaxSubmit(function (data) {
                        var json = eval("(" + data + ")");
                        if (json.success) {
                            $("#commonWin").modal("hide");
                            myTable.refresh();
                        } else {
                            layer.msg(json.msg);
                        }
                    });
                }
                ;
            }
        },
        deviceTypeChange: function(){
            if($("#deviceType").val() == 5){//如果是北斗天地协议
                $("#functionalType").find("option[value='"+ 1 +"']").remove();
                $("#functionalType").find("option[value='"+ 2 +"']").remove();
                $("#functionalType").find("option[value='"+ 3 +"']").remove();
                $("#functionalType").find("option[value='"+ 4 +"']").remove();
                $("#functionalType").find("option[value='"+ 5 +"']").remove();
                $("#functionalType").append("<option value='4'>手咪设备</option>");
            }else{
                $("#functionalType").find("option[value='"+ 1 +"']").remove();
                $("#functionalType").find("option[value='"+ 2 +"']").remove();
                $("#functionalType").find("option[value='"+ 3 +"']").remove();
                $("#functionalType").find("option[value='"+ 4 +"']").remove();
                $("#functionalType").find("option[value='"+ 5 +"']").remove();
                $("#functionalType").append(
                    "<option value='1'>简易型车机</option>" +
                    "<option value='2'>行车记录仪</option>" +
                    "<option value='3'>对讲设备</option>" +
                    "<option value='5'>超长待机设备</option>");
            }
        },
        functionalTypeInit:function(){
            $("#functionalType").val(fts);
        }
    }
    $(function(){
        $('input').inputClear();
        editMeterManagement.init();
        editMeterManagement.deviceTypeChange();
        editMeterManagement.functionalTypeInit();
        //显示菜单
        $("#zTreeOrganSel").bind("click",editMeterManagement.showMenu);
        $("#installTime").val(installTime!=null?installTime.substr(0, 10):"");
        //表单提交
        $("#doSubmit").bind("click",editMeterManagement.doSubmit);
        // $("#deviceType").on("change", function () {
        //     deviceType = $(this).val();
        //     serialnumber = $("#serialnumber").val();
        //     editMeterManagement.serialnumberValidates();
        // })
        $("#serialnumber").bind("input propertychange change", function (event) {
            deviceType = $("#deviceType").val();
            serialnumber = $(this).val();
            if (oldDeviceNumber != serialnumber){
                $.ajax({
                        type: "post",
                        url: "/devm/meter/repetition/",
                        data: {serialnumber: serialnumber},
                        success: function (d) {
                            var result = $.parseJSON(d);
                            if (!result) {
                                serialnumberError.html("终端号已存在！");
                                serialnumberError.show();
                                deviceFlag = false;
                            }
                            else {
                                editMeterManagement.serialnumberValidates();
                            }
                        }
                    }
                )
            }else{
                serialnumberError.hide();
                deviceFlag = true;

            }
        });
    })
})(window,$)
