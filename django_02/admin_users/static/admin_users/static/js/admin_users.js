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
        if ($(this).attr('admin_change') == 'userlist') {
            var data = {'change_data':$(this).attr('admin_change'), 'page_num':$(this).attr('page_num')};
            var ajax_url = url_admin_ajax_change_view;
            var change_id = 'Dinamo_list';
        }
        else if ($(this).attr('admin_change') == 'item_start_edit') {
            var data = {'change_data':$(this).attr('admin_change'), 'item_id':$(this).attr('item_id')};
            var ajax_url = url_admin_ajax_change_view;
            var change_id='item_id_'+$(this).attr('item_id');
        }
        else if ($(this).attr('admin_change') == 'item_stop_edit') {
            var data = {'change_data':$(this).attr('admin_change'), 'item_id':$(this).attr('item_id')};
            var ajax_url = url_admin_ajax_change_view;
            var change_id='item_id_'+$(this).attr('item_id');
        }
        else if ($(this).attr('admin_change') == 'item_edit') {
            var data = jQuery("#"+'edit_user_id').serialize();
            var ajax_url = url_admin_ajax_change_view;
            var change_id='item_id_'+$(this).attr('item_id');

        }
        else if ($(this).attr('admin_change') == 'item_delete') {
            var data = {'change_data':$(this).attr('admin_change'), 'item_id':$(this).attr('item_id')};
            var ajax_url = url_admin_ajax_change_view;
            var change_id='item_id_'+$(this).attr('item_id');
        }

        else if ($(this).attr('admin_change') == 'item_edit_passw') {
            var data = jQuery("#"+'edit_user_id_passw').serialize();
            var ajax_url = url_admin_ajax_change_view;
            var change_id='item_id_'+$(this).attr('item_id');
        }

        else {
            data = '';
            var ajax_url = url_admin_ajax_change_view;
            var change_id = 'Dinamo_list';
        }


        $.ajax({
            type: "POST",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: ajax_url,
            data: data,
            dataType: "html",
            cache: false,
            success: function(data){
                document.getElementById(change_id).innerHTML = data;
            }
       });
    }
});

