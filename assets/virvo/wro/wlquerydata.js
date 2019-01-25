(function(window,$){
    var selectTreeId = '';
    var selectTreepId="";
    var selectTreeType = '';

    var selectCommunity = "";
    var selectBuilding = "";
    var communityid = "";
    //显示隐藏列
    var menu_text = "";
    var table = $("#dataTable tr th:gt(1)");
    //单选
    var subChk = $("input[name='subChk']");
    var communityTree = {
        init : function(){
            // 初始化文件树
            treeSetting = {
                async : {
                    url : "/dmam/district/dmatree/",
                    type : "post",
                    enable : true,
                    autoParam : [ "id" ],
                    dataType : "json",
                    data:{'csrfmiddlewaretoken': '{{ csrf_token }}'},
                    otherParam : {  // 是否可选 Organization
                        "isOrg" : "1",
                        "isCommunity" : "1",
                        "isBuilding":"1",
                        // "csrfmiddlewaretoken": "{{ csrf_token }}"
                    },
                    dataFilter: communityTree.ajaxDataFilter
                },
                view : {
                    // addHoverDom : communityTree.addHoverDom,
                    // removeHoverDom : communityTree.removeHoverDom,
                    selectedMulti : false,
                    nameIsHTML: true,
                    fontCss: setFontCss_ztree
                },
                // edit : {
                //     enable : true,
                //     editNameSelectAll : true,
                //     showRenameBtn : false
                // },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    // beforeDrag : dmaManage.beforeDrag,
                    // beforeEditName : dmaManage.beforeEditName,
                    // beforeRemove : dmaManage.beforeRemove,
                    // beforeRename : dmaManage.beforeRename,
                    // // onRemove : dmaManage.onRemove,
                    // onRename : dmaManage.onRename,
                    onClick : communityTree.zTreeOnClick
                }
            };
            $.fn.zTree.init($("#commubitytreeDemo"), treeSetting, null);
            var treeObj = $.fn.zTree.getZTreeObj('commubitytreeDemo');treeObj.expandAll(true);
           
        },

        beforeDrag: function(treeId, treeNodes){
            return false;
        },
        beforeEditName: function(treeId, treeNode){
            className = (className === "dark" ? "" : "dark");
            dmaManage.showLog("[ " + dmaManage.getTime() + " beforeEditName ]&nbsp;&nbsp;&nbsp;&nbsp; "
                    + treeNode.name);
            var zTree = $.fn.zTree.getZTreeObj("commubitytreeDemo");
            zTree.selectNode(treeNode);
            return tg_confirmDialog(null,userGroupDeleteConfirm);
        },
        // 组织树预处理函数
        ajaxDataFilter: function(treeId, parentNode, responseData){
            var treeObj = $.fn.zTree.getZTreeObj("commubitytreeDemo");
            if (responseData) {
                for (var i = 0; i < responseData.length; i++) {
                        responseData[i].open = true;
                }
            }
            return responseData;
        },
        //点击节点
        zTreeOnClick: function(event, treeId, treeNode){
            selectTreeId = treeNode.id;
            selectDistrictId = treeNode.districtid;
            selectTreeIdAdd=treeNode.uuid;
            
            $('#simpleQueryParam').val("");
            
            
            // dmaManage.getBaseinfo();
            if(treeNode.type == "community"){
                var pNode = treeNode.getParentNode();
                selectCommunity = treeNode.name;
                selectTreeType = "community";

                

            }else if(treeNode.type == "building"){
                var pNode = treeNode.getParentNode();
                selectBuilding = treeNode.name;
                selectTreeType = "building";
                selectCommunity = pNode.name;
            }else{
                selectTreeType = "group";
            }
            myTable.requestData();
            
        },
    },
    wlqData = {
        init: function(){
            menu_text += "<li><label><input type=\"checkbox\" checked=\"checked\" class=\"toggle-vis\" data-column=\"" + parseInt(2) +"\" disabled />"+ table[0].innerHTML +"</label></li>"
            for(var i = 1; i < table.length; i++){
                menu_text += "<li><label><input type=\"checkbox\" checked=\"checked\" class=\"toggle-vis\" data-column=\"" + parseInt(i+2) +"\" />"+ table[i].innerHTML +"</label></li>"
                
            };
            $("#Ul-menu-text").html(menu_text);
            //表格列定义
            var columnDefs = [ {
                //第一列，用来显示序号
                "searchable" : false,
                "orderable" : false,
                "targets" : 0
            } ];
            var columns = [
                    {
                        //第一列，用来显示序号
                        "data" : null,
                        "class" : "text-center"
                    },
                    {
                        "data" : "numbersth",//户号
                        "class" : "text-center",
                        
                    },
                    {
                        "data" : "community",
                        "class" : "text-center", 
                        
                    }, {
                        "data" : "buildingname",
                        "class" : "text-center",
                        
                    },{
                        "data" : "roomname",
                        "class" : "text-center",
                        
                    },{
                        "data" : "nodeaddr",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "wateraddr",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d01",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d02",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d03",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d04",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d05",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d06",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d07",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d08",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d09",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d10",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d11",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d12",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d13",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d14",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d15",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d16",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d17",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d18",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d19",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d20",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d21",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d22",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d23",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d24",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d25",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d26",
                        "class" : "text-center",
                        
                    },{
                        "data" : "d27",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d28",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d29",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d30",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "d31",
                        "class" : "text-center",
                        "hidden":true
                        
                    }];
            //ajax参数
            var ajaxDataParamFun = function(d) {
                d.simpleQueryParam = $('#simpleQueryParam').val(); //模糊查询
                d.groupName = selectTreeId;
                d.groupType = selectTreeType;
                d.selectBuilding = selectBuilding;
                d.selectCommunity = selectCommunity;
                d.selectTreeType = selectTreeType;

            };
            //表格setting
            var setting = {
                suffix  : '/',
                listUrl : '/wirelessm/watermeter/comunitiquery/',
                // editUrl : '/wirelessm/watermeter/edit/',
                // deleteUrl : '/wirelessm/watermeter/delete/',
                // deletemoreUrl : '/wirelessm/watermeter/deletemore/',
                // enableUrl : '/wirelessm/watermeter/enable_',
                // disableUrl : '/wirelessm/watermeter/disable_',
                columnDefs : columnDefs, //表格列定义
                columns : columns, //表格列
                dataTableDiv : 'dataTable', //表格
                ajaxDataParamFun : ajaxDataParamFun, //ajax参数
                pageable : true, //是否分页
                showIndexColumn : true, //是否显示第一列的索引列
                enabledChange : true
            };
            //创建表格
            myTable = new TG_Tabel.createNew(setting);
            //表格初始化
            myTable.init();

            //隐藏大于当日日期的日期
            var dt = $('#dataTable').dataTable().api();
            var now = new Date();
            var tday = now.getDate();
            for(var i = 0; i < table.length; i++){

                    
                if(parseInt(i-4) > parseInt(tday)){
                    //menu_text data-column is i+2
                    dt.column(parseInt(i+2)).visible(false);
                }
            }
            
        },
         //加载完成后执行
        refreshTable: function(){
            $("#simpleQueryParam").val("");
//            selectTreeId = '';
//            selectTreeType = '';
//            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
//            zTree.selectNode("");
//            zTree.cancelSelectedNode();
            myTable.requestData();
            
        },
        
        requeryComunityData:function(flag){
            url = '/wirelessm/neiborhooddailydata/';
            data = {"communityid":communityid,"flag":flag};
            json_ajax("GET",url,"json",true,data,wlqData.requestDataCallback);

        },
        requestDataCallback:function(data){
            console.log(data)
            if(data.success){
                dm = data.monthdata2;
                $.each(dm,function(k,v){
                    console.log(k,":",v)
                    d = k.substring(8,10)
                    $("#d"+d).text(v)
                })
            }
        },
        //开始时间
        startDay: function (day) {
            var timeInterval = $('#timeInterval').val().split('--');
            var startValue = timeInterval[0];
            var endValue = timeInterval[1];
            if (startValue == "" || endValue == "") {
                var today = new Date();
                var targetday_milliseconds = today.getTime() + 1000 * 60 * 60
                    * 24 * day;

                today.setTime(targetday_milliseconds); //注意，这行是关键代码

                var tYear = today.getFullYear();
                var tMonth = today.getMonth();
                var tDate = today.getDate();
                tMonth = wlqData.doHandleMonth(tMonth + 1);
                tDate = wlqData.doHandleMonth(tDate);
                var num = -(day + 1);
                startTime = tYear + "-" + tMonth + "-" + tDate + " "
                    + "00:00:00";
                var end_milliseconds = today.getTime() + 1000 * 60 * 60 * 24
                    * parseInt(num);
                today.setTime(end_milliseconds); //注意，这行是关键代码
                var endYear = today.getFullYear();
                var endMonth = today.getMonth();
                var endDate = today.getDate();
                endMonth = wlqData.doHandleMonth(endMonth + 1);
                endDate = wlqData.doHandleMonth(endDate);
                endTime = endYear + "-" + endMonth + "-" + endDate + " "
                    + "23:59:59";
            } else {
                var startTimeIndex = startValue.slice(0, 10).replace("-", "/").replace("-", "/");
                var vtoday_milliseconds = Date.parse(startTimeIndex) + 1000 * 60 * 60 * 24 * day;
                var dateList = new Date();
                dateList.setTime(vtoday_milliseconds);
                var vYear = dateList.getFullYear();
                var vMonth = dateList.getMonth();
                var vDate = dateList.getDate();
                vMonth = wlqData.doHandleMonth(vMonth + 1);
                vDate = wlqData.doHandleMonth(vDate);
                startTime = vYear + "-" + vMonth + "-" + vDate + " "
                    + "00:00:00";
                if (day == 1) {
                    endTime = vYear + "-" + vMonth + "-" + vDate + " "
                        + "23:59:59";
                } else {
                    var endNum = -1;
                    var vendtoday_milliseconds = Date.parse(startTimeIndex) + 1000 * 60 * 60 * 24 * parseInt(endNum);
                    var dateEnd = new Date();
                    dateEnd.setTime(vendtoday_milliseconds);
                    var vendYear = dateEnd.getFullYear();
                    var vendMonth = dateEnd.getMonth();
                    var vendDate = dateEnd.getDate();
                    vendMonth = wlqData.doHandleMonth(vendMonth + 1);
                    vendDate = wlqData.doHandleMonth(vendDate);
                    endTime = vendYear + "-" + vendMonth + "-" + vendDate + " "
                        + "23:59:59";
                }
            }
        },
        doHandleMonth: function (month) {
            var m = month;
            if (month.toString().length == 1) {
                m = "0" + month;
            }
            return m;
        },
        //当前时间
        getsTheCurrentTime: function () {
            var nowDate = new Date();
            startTime = nowDate.getFullYear()
                + "-"
                + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                    + parseInt(nowDate.getMonth() + 1)
                    : parseInt(nowDate.getMonth() + 1))
                + "-"
                + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                    : nowDate.getDate()) + " " + "00:00:00";
            endTime = nowDate.getFullYear()
                + "-"
                + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                    + parseInt(nowDate.getMonth() + 1)
                    : parseInt(nowDate.getMonth() + 1))
                + "-"
                + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                    : nowDate.getDate())
                + " "
                + ("23")
                + ":"
                + ("59")
                + ":"
                + ("59");
            var atime = $("#atime").val();
            if (atime != undefined && atime != "") {
                startTime = atime;
            }
        },
        unique: function (arr) {
            var result = [], hash = {};
            for (var i = 0, elem; (elem = arr[i]) != null; i++) {
                if (!hash[elem]) {
                    result.push(elem);
                    hash[elem] = true;
                }
            }
            return result;
        },
        estimate: function () {
            var timeInterval = $('#timeInterval').val().split('--');
            sTime = timeInterval[0];
            eTime = timeInterval[1];
            wlqData.getsTheCurrentTime();
            if (eTime > endTime) {                              //查询判断
                layer.msg(endTimeGtNowTime, {move: false});
                key = false
                return;
            }
            if (sTime > eTime) {
                layer.msg(endtimeComStarttime, {move: false});
                key = false;
                return;
            }
            var nowdays = new Date();                       // 获取当前时间  计算上个月的第一天
            var year = nowdays.getFullYear();
            var month = nowdays.getMonth();
            if (month == 0) {
                month = 12;
                year = year - 1;
            }
            if (month < 10) {
                month = "0" + month;
            }
            var firstDay = year + "-" + month + "-" + "01 00:00:00";//上个月的第一天
            if (sTime < firstDay) {                                 //查询判断开始时间不能超过       上个月的第一天
                $("#timeInterval-error").html(starTimeExceedOne).show();
                /*layer.msg(starTimeExceedOne, {move: false});
                key = false;*/
                return;
            }
            $("#timeInterval-error").hide();
            var treeObj = $.fn.zTree.getZTreeObj("treeDemo");       //遍历树节点，获取vehicleID 存入集合
            var nodes = treeObj.getCheckedNodes(true);
            vid = "";
            for (var j = 0; j < nodes.length; j++) {
                if (nodes[j].type == "vehicle") {
                    vid += nodes[j].id + ",";
                }
            }
            key = true;
            startTime=sTime;
            endTime=eTime;
        },

    }

    $(function(){
        $('input').inputClear();
        communityTree.init();
        wlqData.init();
        
        // $('#timeInterval').dateRangePicker({dateLimit:30});
        // wlqData.getsTheCurrentTime();  
        // wlqData.startDay(-7);  
        // $('#timeInterval').val(startTime + '--' + endTime);

        $('input').inputClear().on('onClearEvent',function(e,data){
            var id = data.id;
            if(id == 'search_condition'){
                search_ztree('commubitytreeDemo', id,'assignment');
            };
        });
        //IE9
        if(navigator.appName=="Microsoft Internet Explorer" && navigator.appVersion.split(";")[1].replace(/[ ]/g,"")=="MSIE9.0") {
            var search;
            $("#search_condition").bind("focus",function(){
                search = setInterval(function(){
                    search_ztree('commubitytreeDemo', 'search_condition','assignment');
                },500);
            }).bind("blur",function(){
                clearInterval(search);
            });
        }
        //全选
        $("#checkAll").bind("click",wlqData.cleckAll);
        //单选
        subChk.bind("click",wlqData.subChkClick);
        //批量删除
        $("#del_model").bind("click",wlqData.delModel);
        //加载完成后执行
        $("#refreshTable").on("click",wlqData.refreshTable);
        // 组织架构模糊搜索
        $("#search_condition").on("input oninput",function(){
            search_ztree('commubitytreeDemo', 'search_condition', 'assignment');
        });

        // $("#addId").bind("click",function(){
        //     $("#addDistrictForm").modal("show")
        // })
    })
})(window,$)