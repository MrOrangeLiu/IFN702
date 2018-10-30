/**
 * Created by Administrator on 2017/5/11 0011.
 */
var PMG = window.PMG || {};
PMG.category_upload = function ($) {
    // 相关事件处理
    $(document).ready(function () {
        $("#upload-btn").on('click',function(){
            if ($("#chat_file")[0].files.length == 0) {
                return;
            }
            file = $("#chat_file")[0].files[0];
            var filename = file.name;
            var extStart = filename.lastIndexOf(".");
            var ext = filename.substring(extStart, filename.length).toUpperCase();
            if(ext=='.exe' ){
                 PMG.category_upload.affirm("Do not accept exe files!");
                 return;
            }
            if(file.size>1024*1024*10){
                PMG.category_upload.affirm("File has to be less than 10M!");
                return;
            }
            var formdata =  new FormData($("#chat_file_form")[0]);
            formdata.append('chat_file', file);
            PMG.category_upload.show_loading("File uploading, please try not close this window...");
            $.ajax({
                url: "/fileuploads/upload_file/",
                type: 'POST',
                data: formdata,
                processData: false,
                contentType: false,
                success: function (data) {
                    PMG.category_upload.hide_loading(function(){
                        PMG.category_upload.affirm(data.msg);
                        $("#file_path").val(data.file_path);
                        $("#file_path").text(data.file_path);
                    });
                },
                error:function(){
                    PMG.category_upload.hide_loading();
                    alert("Network exception, try later！");
                }
            });
        });

        // 下载文件
        $("#download-btn").on('click',function(){
            window.open("/mngadmin/download_file/?file_path="+$("#file_path").val(), "_blank")
        });
    });
    // 接口定义
    return {
        show_loading:function (content){
            content = content || 'Loading……';
            $("#loading_text").html(content);
            $('#loading').modal({backdrop: 'static', keyboard: false, show: true});
        },
        hide_loading:function(callback){
            $("#loading_text").html('');
            $('#loading').modal('hide');
            if(callback != undefined){
                callback();
            }
        },
        // 轻提示框
        affirm:function (content,timeout,fg) {
            var flag = fg||false;
            var time_out = timeout||2000;
            $("#content_box").html(content);
            var timer, timer_location;
            $("#affirm_box").fadeIn(1000);
            timer = setInterval(function () {
                clearInterval(timer);
                $("#affirm_box").fadeOut(1000);
            }, time_out);
            timer_location = setInterval(function () {
                clearInterval(timer_location);
                if (flag) {
                    window.location.reload();
                }
            }, 3000);
        }
    }
}($);