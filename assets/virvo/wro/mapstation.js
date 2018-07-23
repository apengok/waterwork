(function($,window){
    var selectTreeId = '';
    var selectDistrictId = '';
    var zNodes = null;
    var log, className = "dark";
    var newCount = 1;
    var columnDefs;
    var columns;
    var setting;
    var treeSetting;
    var idStr;
    var OperationId;
    var selectTreeIdAdd="";
    var startOperation;// 点击运营资质类别的修改按钮时，弹出界面时运营资质类别文本的内容
    var expliant;// 点击运营资质类别的修改按钮时，弹出界面时说明文本的内容
    var vagueSearchlast = $("#userType").val();
    var overlay;
    var getdmamapusedata_flag = 0;
    var markerInfoWindow = null;
    mapStation = {
        init: function(){
            // map
            var layer = new AMap.TileLayer({
                  zooms:[3,20],    //可见级别
                  visible:true,    //是否可见
                  opacity:1,       //透明度
                  zIndex:0         //叠加层级
            });
            

            map = new AMap.Map('map-container',{
                zoom: 10,  //设置地图显示的缩放级别
                center: [118.438781,29.871515],
                layers:[layer], //当只想显示标准图层时layers属性可缺省
                viewMode: '2D',  //设置地图模式
                lang:'zh_cn',  //设置地图语言类型
            });

            // overlay = document.getElementById('js-overlay');
            markerInfoWindow = new AMap.InfoWindow({
                // isCustom: true,  //使用自定义窗体
                // content: mapStation.createInfoWindow("title", overlay.innerHTML),
                size:new AMap.Size(400,300),
                offset: new AMap.Pixel(0, 0),
                autoMove: true
            });

            var marker = new AMap.Marker({
                position: new AMap.LngLat(118.438781,29.871515),   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
                title: 'station1'
            });

            marker.on("mouseover",function(e){
                overlay = document.getElementById('js-overlay');
                overlay.getElement().style.display = 'block';
                console.log(overlay.outerHTML);
                var position = e.lnglat;


                markerInfoWindow.setContent(overlay.outerHTML);
                // markerInfoWindow.setSize(AMap.Size(400,300));
                markerInfoWindow.open(map,position);
            });

            marker.on("mouseout",function(){
                markerInfoWindow.close();
            })

            map.add(marker);
            
        },
        //构建自定义信息窗体
        createInfoWindow:function (title, content) {
            var info = document.createElement("div");
            info.className = "info";
     
            //可以通过下面的方式修改自定义窗体的宽高
            //info.style.width = "400px";
            // 定义顶部标题
            var top = document.createElement("div");
            var titleD = document.createElement("div");
            var closeX = document.createElement("img");
            top.className = "info-top";
            titleD.innerHTML = title;
            closeX.src = "http://webapi.amap.com/images/close2.gif";
            closeX.onclick = mapStation.closeInfoWindow();
     
            top.appendChild(titleD);
            top.appendChild(closeX);
            info.appendChild(top);
     
            // 定义中部内容
            var middle = document.createElement("div");
            middle.className = "info-middle";
            middle.style.backgroundColor = 'white';
            middle.innerHTML = content;
            info.appendChild(middle);
     
            // 定义底部内容
            var bottom = document.createElement("div");
            bottom.className = "info-bottom";
            bottom.style.position = 'relative';
            bottom.style.top = '0px';
            bottom.style.margin = '0 auto';
            var sharp = document.createElement("img");
            sharp.src = "http://webapi.amap.com/images/sharp.png";
            bottom.appendChild(sharp);
            info.appendChild(bottom);
            return info;
        },
        //关闭信息窗体
        closeInfoWindow:function () {
            map.clearInfoWindow();
        },
        appLayer:function (options) {
            var layer = new ol.layer.Tile({
                //extent: ol.proj.transformExtent(options.mapExtent, options.fromProject, options.toProject),
                source: new ol.source.XYZ({
                urls: options.urls,
                tilePixelRatio: options.tilePixelRatio,
                minZoom: options.mapMinZoom,
                maxZoom: options.mapMaxZoom
                })
           });
           return layer;
        },
        moveonmapevent:function(evt) {
            var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
                overlay.setPosition(evt.coordinate);
                // overlay.getElement().innerHTML = feature.get('name');
                // console.log(feature.get('text'));
                name = feature.get('name');
                
                return feature;
              });
              // console.log(feature);
              
              mapStation.rebuildoverlay(name);
              overlay.getElement().style.display = 'block';
              (feature) ? overlay.setPosition(mapStation.recalcposition(feature.getGeometry().getCoordinates())) : overlay.setPosition(undefined);

              // overlay.getElement().style.display = feature ? 'block' : 'none';
              // document.body.style.cursor = feature ? 'pointer' : '';
        },
        recalcposition:function(cord){
            console.log(cord);
            if(cord[1] < -1000){
                return [cord[0],cord[1]+800];
            }
            return cord;
        },
        createIconStyle:function(country,description) {
            return new ol.style.Style({
                image: new ol.style.Icon({
                    anchor: [0.5, 46],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'pixels',
                    // opacity: 0.75,
                    src: "/static/virvo/images/" + country + '.png'
                }),
                text: new ol.style.Text({
                        font: '20px Calibri,sans-serif',
                        fill: new ol.style.Fill({ color: '#000' }),
                        stroke: new ol.style.Stroke({
                        color: '#fff', width: 2
                    }),
                // get the text from the feature - `this` is ol.Feature
                // and show only under certain resolution
                text: description

                // text: map.getView().getZoom() > 12 ? this.get('description') : ''
              })
            })
        },
        rebuildoverlay:function(name){
            console.log('name:',name);
            $("#dma_name span").html(name);

            var tmpste = eval(statsinfo);
            
            if(tmpste != null){
                statistic = tmpste.statsinfo;
                for (var i = 0; i < statistic.length; i++){
                    if(name==statistic[i].dma_name){
                        $("#belongto span").html(statistic[i].belongto);
                        $("#dma_level span").html(statistic[i].dma_level);
                        $("#dma_status span").html(statistic[i].dma_status);
                        $("#dmaflow span").html(statistic[i].dmaflow);
                        $("#month_sale span").html(statistic[i].month_sale);
                        $("#lastmonth_sale span").html(statistic[i].lastmonth_sale);
                        $("#bili span").html(statistic[i].bili);
                    }
                }
            }
            
            // var data={"dma_name":name,'csrfmiddlewaretoken': '{{ csrf_token }}'};
            // var url="/dmam/getdmamapusedata/";
            // json_ajax("GET", url, "json", true,data,mapStation.updateoverlay);
        },
        updateoverlay:function(data){
            console.log('updateoverlay',data);
            if(data.dma_statics != null){
                statistic = data.dma_statics;
                // $("#dma_name span").html(name);
                // $("#dma_name span").html(name);
                $("#belongto span").html(statistic.belongto);
                $("#dma_level span").html(statistic.dma_level);
                $("#dma_status span").html(statistic.dma_status);
                $("#dmaflow span").html(statistic.dmaflow);
                $("#month_sale span").html(statistic.month_sale);
                $("#lastmonth_sale span").html(statistic.lastmonth_sale);
                $("#bili span").html(statistic.bili);
            }
        },
        userTree : function(){
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
                        // "csrfmiddlewaretoken": "{{ csrf_token }}"
                    },
                    dataFilter: mapStation.ajaxDataFilter
                },
                view : {
                    // addHoverDom : mapStation.addHoverDom,
                    // removeHoverDom : mapStation.removeHoverDom,
                    selectedMulti : false,
                    nameIsHTML: true,
                    // fontCss: setFontCss_ztree
                },
                edit : {
                    enable : true,
                    editNameSelectAll : true,
                    showRemoveBtn : false,//mapStation.showRemoveBtn,
                    showRenameBtn : false
                },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    beforeDrag : mapStation.beforeDrag,
                    beforeEditName : mapStation.beforeEditName,
                    beforeRemove : mapStation.beforeRemove,
                    beforeRename : mapStation.beforeRename,
                    // onRemove : mapStation.onRemove,
                    onRename : mapStation.onRename,
                    onClick : mapStation.zTreeOnClick
                }
            };
            $.fn.zTree.init($("#treeDemo"), treeSetting, zNodes);
            var treeObj = $.fn.zTree.getZTreeObj('treeDemo');treeObj.expandAll(true);
           
        },

        beforeDrag: function(treeId, treeNodes){
            return false;
        },
        beforeEditName: function(treeId, treeNode){
            className = (className === "dark" ? "" : "dark");
            mapStation.showLog("[ " + mapStation.getTime() + " beforeEditName ]&nbsp;&nbsp;&nbsp;&nbsp; "
                    + treeNode.name);
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            zTree.selectNode(treeNode);
            return tg_confirmDialog(null,userGroupDeleteConfirm);
        },
        // 组织树预处理函数
        ajaxDataFilter: function(treeId, parentNode, responseData){
            var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
            if (responseData) {
                for (var i = 0; i < responseData.length; i++) {
                        responseData[i].open = true;
                }
            }
            return responseData;
        },
        beforeRemove: function(treeId, treeNode){
            className = (className === "dark" ? "" : "dark");
            mapStation.showLog("[ " + mapStation.getTime() + " beforeRemove ]&nbsp;&nbsp;&nbsp;&nbsp; "
                    + treeNode.name);
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            zTree.selectNode(treeNode);
            var result;
            layer.confirm(userGroupDeleteConfirm, {
                title :'操作确认',
                icon : 3, // 问号图标
                btn: ['确认','取消'] // 按钮
            }, function(index){
                selectTreeIdAdd="";
                var nodes = zTree.getSelectedNodes();
                var preNode = nodes[0].getPreNode();
                var nextNode = nodes[0].getNextNode();
                var parentNode = nodes[0].getParentNode();
                $.ajax({
                    type: 'POST',
                    url: 'district/delete/',
                    data: {"pId": treeNode.id},
                    async:false,
                    dataType: 'json',
                    success: function (data) {
                        var flag=data.success;      
                        if(flag==false){
                            layer.msg(data.msg,{move:false})
                        }
                        if(flag==true){
                            $('#simpleQueryParam').val("");
                            selectTreeId = "";
                            selectDistrictId = "";
                            $.ajax({
                                type: 'POST',
                                url: 'district/dmatree/',
                                data: {"isOrg" : "1"},
                                async:false,
                                dataType: 'json',
                                success: function (data) {
                                    var data2 = JSON.stringify(data);
                                    var addData = JSON.parse(data2);             
                                    var nodeName;
                                    if(preNode != null){
                                        nodeName = preNode.name;
                                    }else if(nextNode != null){
                                        nodeName = nextNode.name;
                                    }else{
                                        nodeName = parentNode.name;
                                    };
                                    $.fn.zTree.init($("#treeDemo"), treeSetting, addData);  
                                    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                                    var nodes = treeObj.getNodes();
                                    for(var j=0;j<nodes.length;j++){
                                         zTree.expandNode(nodes[j], true, true, true);
                                    }
                                    // pengwl delete group and user refresh tabale
                                    myTable.requestData();
                                },      
                            });
                        }
                        layer.close(index,{move:false});
                    },
                    error: function () {
                        layer.msg(systemError, {move: false});
                    }
                });
            }, function(index){
                layer.close(index,{move:false});
            });
            return false;
        },
        onRemove: function(e, treeId, treeNode){
            selectTreeIdAdd="";
            mapStation.showLog("[ " + mapStation.getTime() + " onRemove ]&nbsp;&nbsp;&nbsp;&nbsp; "
                + treeNode.name);
        },
        beforeRename: function(treeId, treeNode, newName, isCancel){
            className = (className === "dark" ? "" : "dark");
            mapStation.showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + mapStation.getTime()
                    + " beforeRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name
                    + (isCancel ? "</span>" : ""));
            if (newName.length == 0) {
                layer.msg(userNodeNameNull, {move: false});
                var zTree = $.fn.zTree.getZTreeObj("treeDemo");
                setTimeout(function() {
                    zTree.editName(treeNode)
                }, 10);
                return false;
            }
            return true;
        },
        onRename: function(e, treeId, treeNode, isCancel){
            mapStation.showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + mapStation.getTime()
                + " onRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name
                + (isCancel ? "</span>" : ""));
        },
        // 显示删除组织按钮
        showRemoveBtn: function(treeId, treeNode){
            return treeNode.children==undefined;
        },
        showRenameBtn: function(treeId, treeNode){
            return !treeNode.isLastNode;
        },
        showLog: function(str){
            if (!log)
                log = $("#log");
                log.append("<li class='"+className+"'>" + str + "</li>");
            if (log.children("li").length > 8) {
                log.get(0).removeChild(log.children("li")[0]);
            }
        },
        getTime: function(){
            var now = new Date(), h = now.getHours(), m = now.getMinutes(), s = now
                .getSeconds(), ms = now.getMilliseconds();
            return (h + ":" + m + ":" + s + " " + ms);
        },
        
        selectAll: function(){
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            zTree.treeSetting.edit.editNameSelectAll = $("#selectAll").attr("checked");
        },
        //点击节点
        zTreeOnClick: function(event, treeId, treeNode){
            selectTreeId = treeNode.id;
            selectDistrictId = treeNode.districtid;
            selectTreeIdAdd=treeNode.uuid;
            $('#simpleQueryParam').val("");
            myTable.requestData();
        },
        // ajax参数
        ajaxDataParamFun: function(d){
            d.simpleQueryParam = $('#simpleQueryParam').val(); // 模糊查询
            d.groupName = selectTreeId;
            d.districtId = selectDistrictId;
        },
        findDownKey:function(event){
            if(event.keyCode==13){
                mapStation.findOperation();
            }
        }
    }
    $(function(){
        $('input').inputClear().on('onClearEvent',function(e,data){
            var id = data.id;
            if(id == 'search_condition'){
                search_ztree('treeDemo',id,'group');
            };
        });
        var map;
        mapStation.userTree();
        
        mapStation.init();
        
        // map.on(['pointermove', 'singleclick'], mapStation.moveonmapevent);
        
    })
})($,window)
