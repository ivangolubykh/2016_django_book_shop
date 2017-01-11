jQuery(document).ready(function ($) {
    //'.change_data').click(changeView); // статичный метод
    $('body').on('click','.change_data',changeView) // Динамичный метод
    function changeView() {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        var process_data = true;
        var content_type = 'application/x-www-form-urlencoded; charset=UTF-8';

        if ($(this).attr('admin_change') == 'item_list') {
            if (send_file == true) {
                var data = new FormData(document.getElementById('item_list'));
                process_data = false;
                content_type = false;
            }
            else {
                var data = jQuery("#"+'item_list').serialize();
            }
            var ajax_url = url_admin_ajax_items;
            var change_id = 'List_Dinamo';
        }
        else if ($(this).attr('admin_change') == 'item_start_edit') {
            var data = {'change_data':$(this).attr('admin_change'), 'item_id':$(this).attr('item_id')};
            var ajax_url = url_admin_ajax_items;
            var change_id='item_id_'+$(this).attr('item_id');
        }
        else if ($(this).attr('admin_change') == 'item_end_edit') {
            var data = jQuery("#"+'item_end_edit_id_'+$(this).attr('item_id')).serialize();
            var ajax_url = url_admin_ajax_items;
            var change_id='item_id_'+$(this).attr('item_id');
        }
        else if ($(this).attr('admin_change') == 'item_deleted') {
            var data = {'change_data':$(this).attr('admin_change'), 'item_id':$(this).attr('item_id')};
            var ajax_url = url_admin_ajax_items;
            var change_id='item_id_'+$(this).attr('item_id');
        }
        else if ($(this).attr('admin_change') == 'item_stop_edit') {
            var data = {'change_data':$(this).attr('admin_change'), 'item_id':$(this).attr('item_id')};
            var ajax_url = url_admin_ajax_items;
            var change_id='item_id_'+$(this).attr('item_id');
        }

        else {
            data = '';
            var ajax_url = url_admin_ajax_change_view;
            var change_id = 'adminDinamo';
        }

        $.ajax({
            type: "POST",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: ajax_url,
            data: data,
            contentType: content_type, // важно - при отправке файлов убираем форматирование данных по умолчанию
            processData: process_data, // Необходимо false для отправки данных типа FormData (убираем форматирование данных по умолчанию)и необходимо true для остальных случаев.
            dataType: "html",
            cache: false,
            success: function(data){
                document.getElementById(change_id).innerHTML = data;
            }
       });
    }
});

