
    $('#id_direction').change(function () {
        var module = $(id_direction).find('option:selected').val();
        $.ajax({
            type: "get",
            url: "xadmin/courses/course/6/update/?module=" + module,
            data: '',
            async: true,
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrf_token'));
            },
            success: function (data) {
                console.log(data[0]);
                console.log(data);
                $(id_category)[0].selectize.clearOptions(); //二级select清空选项
                for (var i = 0; i < data.length; i++) {
                    console.log(data[i]);
                    var item = data[i];
                    var test = {text: data[i].name, value: data[i].id, $order: i + 1}; //遍历数据,拼凑出selectize需要的格式
                    $(id_category)[0].selectize.addOption(test); //添加数据
                }
            },
            error: function (xhr, textStatus) {
                console.log(xhr);
                console.log(textStatus);

            }
        });

}
    )