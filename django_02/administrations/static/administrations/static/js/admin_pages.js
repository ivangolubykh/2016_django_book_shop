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
            var data = {'change_data':$(this).attr('admin_change')};
        }
        else if ($(this).attr('admin_change') == 'userinfo') {
            var data = {'change_data':$(this).attr('admin_change'), 'info_id':$(this).attr('info_id')};
        }
        else if ($(this).attr('admin_change') == 'useredit') {
            var data = jQuery("#"+'edit_user_id').serialize();
        }
        else {
            data = '';
        }

        $.ajax({
            type: "POST",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: url_admin_ajax_change_view,
            data: data,
            dataType: "html",
            cache: false,
            success: function(data){
                document.getElementById('adminDinamo').innerHTML = data;
                if (data == 'ok'){
                    location.reload();
                }
            }
       });
    }
});

