

$(document).ready(
    function(){

        $('.answers').each(function () {
            const obj = $(this);
            obj.load(obj.data('url'));

            var centrifuge = new Centrifuge('http://localhost:9000/connection/sockjs', {debug: true});
            centrifuge.setToken(obj.data('token'));
            centrifuge.subscribe(`answers_question_${obj.data('pk')}`, function () {
                    obj.load(obj.data('url'));
            });

            centrifuge.connect();
        });



        $('#id_categories').chosen();
        window.setInterval(
            function() {
                $('.autoload').each(function() {
                $(this).load($(this).attr('data-url'))
                })

            },
            2000
        );


        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", $('meta[name=csrf]').attr("content"));
                }
            }
        });


        $(document).on('click', 'button.ajaxlike', function(e) {
            var data = $(this).data();
            //console.log(data);
            var likesSpan = $('#likes-' + data.questionid);
            $.ajax({url: $('button.ajaxlike').attr('data-url'), method: 'POST'}).done(function(data, status, response) { likesSpan.html(data);  });//$('button.ajaxlike').html(data)); });
            //likesSpan.html("Lul");
            return false;
        });




        $('#myModal').on('shown.bs.modal', function () {
            $('#myInput').focus();
            $('.question-edit').each(function() {
                $(this).load($(this).attr('data-url'));
            });
        });



        $(document).on('submit', '.ajaxform', function() {
            var form = this;
            $.ajax({url: $(form).attr('data-url'), method: 'post', data: $(form).serialize()}).done(function(data, status, response) { location.reload($(form).attr('data-url')) });
            return false;
        });
    }


)
