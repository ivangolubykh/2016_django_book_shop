jQuery(document).ready(function ($) {
    $('.change_data').click(changeView);
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

        $.ajax({
            type: "POST",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: url_admin_ajax_change_view,
            data:{
                'change_data':$(this).attr('admin_change'),
            },
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

