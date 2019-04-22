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
                communityid = treeNode.id;
                $("#station_name").val(treeNode.name)
                $("#commaddr").val(treeNode.id)

                communityDaily.requeryComunityData(1);

            }else if(treeNode.type == "building"){
                var pNode = treeNode.getParentNode();
                selectBuilding = treeNode.name;
                selectTreeType = "building";
                selectCommunity = pNode.name;
            }else{
                selectTreeType = "group";
            }
            
        },
    },
    communityDaily = {
        init: function(){
            
        },
        
        requeryComunityData:function(flag){
            if(communityid == ""){
                layer.msg("请选择小区")
                return
            }
            communityDaily.estimate();
            if(flag==1){
                
            }
            console.log(startTime,endTime)

            url = '/wirelessm/neiborhooddailydata/';
            data = {"communityid":communityid,"flag":flag,"sTime":startTime,"eTime":endTime};
            json_ajax("GET",url,"json",true,data,communityDaily.requestDataCallback);

        },
        requestDataCallback:function(data){
            console.log(data)
            if(data.success){
                dm = data.monthdata;
                $.each(dm,function(k,v){
                    // console.log(k,":",v)
                    d = k.substring(8,10)
                    $("#d"+d).text(v)
                })

            communityDaily.comunityDailyUseChart();
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
                tMonth = communityDaily.doHandleMonth(tMonth + 1);
                tDate = communityDaily.doHandleMonth(tDate);
                var num = -(day + 1);
                startTime = tYear + "-" + tMonth + "-" + tDate;
                var end_milliseconds = today.getTime() + 1000 * 60 * 60 * 24
                    * parseInt(num);
                today.setTime(end_milliseconds); //注意，这行是关键代码
                var endYear = today.getFullYear();
                var endMonth = today.getMonth();
                var endDate = today.getDate();
                endMonth = communityDaily.doHandleMonth(endMonth + 1);
                endDate = communityDaily.doHandleMonth(endDate);
                endTime = endYear + "-" + endMonth + "-" + endDate;
            } else {
                var startTimeIndex = startValue.slice(0, 10).replace("-", "/").replace("-", "/");
                var vtoday_milliseconds = Date.parse(startTimeIndex) + 1000 * 60 * 60 * 24 * day;
                var dateList = new Date();
                dateList.setTime(vtoday_milliseconds);
                var vYear = dateList.getFullYear();
                var vMonth = dateList.getMonth();
                var vDate = dateList.getDate();
                vMonth = communityDaily.doHandleMonth(vMonth + 1);
                vDate = communityDaily.doHandleMonth(vDate);
                startTime = vYear + "-" + vMonth + "-" + vDate;
                if (day == 1) {
                    endTime = vYear + "-" + vMonth + "-" + vDate;
                } else {
                    var endNum = -1;
                    var vendtoday_milliseconds = Date.parse(startTimeIndex) + 1000 * 60 * 60 * 24 * parseInt(endNum);
                    var dateEnd = new Date();
                    dateEnd.setTime(vendtoday_milliseconds);
                    var vendYear = dateEnd.getFullYear();
                    var vendMonth = dateEnd.getMonth();
                    var vendDate = dateEnd.getDate();
                    vendMonth = communityDaily.doHandleMonth(vendMonth + 1);
                    vendDate = communityDaily.doHandleMonth(vendDate);
                    endTime = vendYear + "-" + vendMonth + "-" + vendDate;
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
                    : nowDate.getDate());
            endTime = nowDate.getFullYear()
                + "-"
                + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                    + parseInt(nowDate.getMonth() + 1)
                    : parseInt(nowDate.getMonth() + 1))
                + "-"
                + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                    : nowDate.getDate());
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
            communityDaily.getsTheCurrentTime();
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
            var firstDay = year + "-" + month + "-" + "01";//上个月的第一天
            if (sTime < firstDay) {                                 //查询判断开始时间不能超过       上个月的第一天
                $("#timeInterval-error").html(starTimeExceedOne).show();
                /*layer.msg(starTimeExceedOne, {move: false});
                key = false;*/
                return;
            }
            $("#timeInterval-error").hide();
            
            key = true;
            startTime=sTime;
            endTime=eTime;
        },
        comunityDailyUseChart:function(){

            options = {
                backgroundColor: '#FFFFFF',
                
                title: {
                    text: '近7日流量压力曲线图',
                    left:'left',
                    textStyle:{
                        fontSize:12,
                        fontWeight:'100'
                    },
                },
                // tooltip: {
                //     trigger: 'axis',
                //     axisPointer: { // 坐标轴指示器，坐标轴触发有效
                //         type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                //     }
                // },
                
                legend: {
                    data: ['流量'],
                    
                },
                    grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '15%',
                    containLabel: true
                    },
                
                xAxis: [{
                    type: 'category',
                     boundaryGap: false,
                    //show:false,
                    data: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','20','31','32','33','34','35','36','37','38','39','40'],
                    axisLabel:{
                        textStyle:{
                            fontSize:10
                        }
                    }
                }],
                yAxis: {
                    type: 'value',
                    //show:false,
                  //  name: '流量',
                    // min: 0,
                     max: 10,
                    interval: 10,
                    splitLine:{
                        show:false,
                    }
                },
                series: [{
                    name: 'flow',
                    type: 'line',
                    itemStyle: {
                        normal: {
                            color: '#7acf88',
                            // areaStyle:{type:'default'}
                        },
                    },
                    
                    data: [4,6,3,7,2,4,4,4,1,2,3,2,6,3,2,0,1,2,4,0,4,6,3,7,2,4,4,4,1,2,3,2,6,3,2,0,1,2,4,0]
                }]
            };

            recent7flowpress = echarts.init(document.getElementById('comunity_daily_chart'));
            recent7flowpress.setOption(options);
            
        },

    }

    $(function(){
        $('input').inputClear();
        communityTree.init();
        communityDaily.init();
        
        $('#timeInterval').dateRangePicker({dateLimit:30});
        communityDaily.getsTheCurrentTime();  
        communityDaily.startDay(-30);  
        $('#timeInterval').val(startTime + '--' + endTime);

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
        $("#checkAll").bind("click",communityDaily.cleckAll);
        //单选
        subChk.bind("click",communityDaily.subChkClick);
        //批量删除
        $("#del_model").bind("click",communityDaily.delModel);
        //加载完成后执行
        $("#refreshTable").on("click",communityDaily.refreshTable);
        // 组织架构模糊搜索
        $("#search_condition").on("input oninput",function(){
            search_ztree('commubitytreeDemo', 'search_condition', 'assignment');
        });

        $("#thismonthClick").on("click",function(){
            communityDaily.requeryComunityData(0);
        })
        $("#lastmonthClick").on("click",function(){
            communityDaily.requeryComunityData(-1);
        })
        $("#inquireClick").on("click",function(){
            communityDaily.requeryComunityData(1);
        })

        // $("#addId").bind("click",function(){
        //     $("#addDistrictForm").modal("show")
        // })
    })
})(window,$)