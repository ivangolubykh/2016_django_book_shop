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
            var ajax_url = url_admin_ajax_change_view;
            var change_id = 'adminDinamo';
        }
        else if ($(this).attr('admin_change') == 'userinfo') {
            var data = {'change_data':$(this).attr('admin_change'), 'info_id':$(this).attr('info_id')};
            var ajax_url = url_admin_ajax_change_view;
            var change_id = 'adminDinamo';
        }
        else if ($(this).attr('admin_change') == 'useredit') {
            var data = jQuery("#"+'edit_user_id').serialize();
            var ajax_url = url_admin_ajax_change_view;
            var change_id = 'adminDinamo';
        }
        else if ($(this).attr('admin_change') == 'userdelete') {
            var data = {'change_data':$(this).attr('admin_change'), 'del_id':$(this).attr('del_id')};
            var ajax_url = url_admin_ajax_change_view;
            var change_id = 'adminDinamo';
        }
        else if ($(this).attr('admin_change') == 'useredit_passw') {
            var data = jQuery("#"+'edit_user_id_passw').serialize();
            var ajax_url = url_admin_ajax_change_view;
            var change_id = 'adminDinamo';
        }

        else if ($(this).attr('admin_change') == 'book_author_list') {
            var data = jQuery("#"+'book_author_list').serialize();
            var ajax_url = url_admin_ajax_books_authors;
            var change_id = 'adminDinamo';
        }
        else if ($(this).attr('admin_change') == 'book_author_start_edit') {
            var data = {'change_data':$(this).attr('admin_change'), 'author_id':$(this).attr('author_id')};
            var ajax_url = url_admin_ajax_books_authors;
            var change_id='book_author_id_'+$(this).attr('author_id');
        }
        else if ($(this).attr('admin_change') == 'book_author_end_edit') {
            var data = jQuery("#"+'book_author_end_edit_id_'+$(this).attr('author_id')).serialize();
            var ajax_url = url_admin_ajax_books_authors;
            var change_id='book_author_id_'+$(this).attr('author_id');
        }
        else if ($(this).attr('admin_change') == 'book_author_deleted') {
            var data = {'change_data':$(this).attr('admin_change'), 'author_id':$(this).attr('author_id')};
            var ajax_url = url_admin_ajax_books_authors;
            var change_id='book_author_id_'+$(this).attr('author_id');
        }
        else if ($(this).attr('admin_change') == 'book_author_stop_edit') {
            var data = {'change_data':$(this).attr('admin_change'), 'author_id':$(this).attr('author_id')};
            var ajax_url = url_admin_ajax_books_authors;
            var change_id='book_author_id_'+$(this).attr('author_id');
        }


        else if ($(this).attr('admin_change') == 'book_categor_list') {
            var data = jQuery("#"+'book_categor_list').serialize();
            var ajax_url = url_admin_ajax_books_categor;
            var change_id = 'adminDinamo';
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
            dataType: "html",
            cache: false,
            success: function(data){
                document.getElementById(change_id).innerHTML = data;
//                if (data == 'ok'){
//                    location.reload();
//                }
            }
       });
    }
});

