String.prototype.replaceAll = function (exp, newStr) {
    return this.replace(new RegExp(exp, "gm"), newStr);
}

String.prototype.format = function (args) {
    var result = this;

    if (arguments.length < 1) {
        return result;
    }

    var data = arguments;
    if (arguments.length == 1 && typeof (args) == 'object') {
        data = args;
    }

    for (var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replaceAll("\\{" + key + "\\}", value);
        }
    }
    return result;
}

// String.prototype.format = function () {
//     var str = this;
//     for (var i = 0; i < arguments.length; i++) {
//         var str = str.replace(new RegExp('\\{' + i + '\\}', 'g'), arguments[i])
//     };
//     return str;
// }

$(function () {
    // 评论的提交处理
    $('#comment-form').submit(function () {
        $("#comment_errors").text('');
        var text = CKEDITOR.instances['id_comment_text'].document.getBody().getText();
        // 判断评论内容是否为空
        if (text.trim() == '') {
            $('#comment_errors').text('大神，拜托写点什么吧 -__- ');
            console.log('Error: no comment');
            return false;
        }

        // 判断评论的长度是否超过限制
        if (text.length > 140) {
            $('#comment_errors').text('抱歉，你的神评撑爆了我们的框框 >__< ');
            console.log("Error: comment too long");
            return false;
        }

        var text_length = text.length;
        console.log(text_length);

        CKEDITOR.instances['id_comment_text'].updateElement();

        $.ajax({
            // url: "{% url 'comment' %}", # Holy shitx
            url: "/comment/",
            type: 'POST',
            data: $(this).serialize(),
            cache: false,
            async: true,
            success: function (data) {
                console.log(data);
                if (data['status'] == 'SUCCESS') {
                    // 区分评论
                    if ($('#reply_to_id').val() == '0') {
                        var comment_html = new String(
                            '<li class="list-group-item">' +
                            '<small>' +
                            '<span>{0}</span> ' +
                            '<span>{1}</span>' +
                            '</small>' +
                            '<br>' +
                            '<div id="comment_{2}">' +
                            '{3}' +
                            '</div>' +
                            '<div class="like-area" onclick="javascript:like_it(this, \'{4}\', {2}, \'/like/likechange\')">' +
                            '<i class="iconfont icon-xihuan1"></i> ' +
                            '<span id="likes_num">0</span> ' +
                            '</div>' +
                            '<a href="javascript:reply({2})">回复</a>' +
                            '</li>');
                        comment_html = comment_html.format(data['username'], data['comment_time'], data['pk'], data['comment_text'], data['content_type'])
                        $('#no-commend').remove();
                        $('#comment-box').prepend(comment_html);
                    } else {
                        // 插入回复
                        var reply_html = new String(
                            '<div class="reply">' +
                            '<small>' +
                            '<span>{0}</span> ' +
                            '<span>{1}</span> ' +
                            '<span>回复</span> ' +
                            '<span>{5}</span>' +
                            '</small>' +
                            '<div id="comment_{2}">' +
                            '{3}' +
                            '</div>' +
                            '<div class="like-area" onclick="javascript:like_it(this, \'{4}\', {2}, \'/like/likechange\')">' +
                            '<i class="iconfont icon-xihuan1"></i> ' +
                            '<span id="likes_num">0</span>' +
                            '</div>' +
                            '<a href="javascript:reply({2})">回复</a>' +
                            '</div>');
                        reply_html = reply_html.format(data['username'], data['comment_time'], data['pk'], data['comment_text'], data['content_type'], data['reply_to'])
                        console.log(data['root_pk']);
                        $('#root_' + data['root_pk']).append(reply_html);
                    }

                    // 清空编辑框
                    CKEDITOR.instances['id_comment_text'].setData('');
                    $('#reply_container').hide();
                    $('#reply_to_id').val('0');
                    $('#comment_errors').text('评论成功!');
                } else {
                    $('#comment_errors').text(data['message']);
                }
            },
            error: function (xhr) {
                console.log('出错了');
                console.log(xhr);
            }
        });
        return false;
    });
});

// 回复执行的操作
function reply(reply_comment_id) {
    // console.log(reply_comment_id);
    $('#reply_to_id').val(reply_comment_id);
    // 设置回复框上方的内容
    var html_content = $('#comment_' + reply_comment_id).html();
    // console.log(html_content);
    $('#reply_content').html(html_content);
    $('#reply_container').show();
    // 导航至回复框
    $('html').animate({ scrollTop: $('#comment-form').offset().top - 130 }, 300, function () {
        CKEDITOR.instances['id_comment_text'].focus();
    });
}

function like_it(obj, content_type, object_id, location) {
    console.log('content_type is ' + content_type + ' object_id is ' + object_id);
    var is_like = $(obj).children('.active').length == 0
    console.log(is_like);

    $.ajax({
        url: location,
        data: {
            content_type: content_type,
            object_id: object_id,
            is_like: is_like
        },
        cache: false,
        async: true,
        success: function (data) {
            console.log(data);
            if (data['status'] == 'SUCCESS') {
                // 改变图标颜色
                var element = $(obj).children('.icon-xihuan1');
                if (is_like) {
                    element.addClass('active');
                } else {
                    element.removeClass('active');
                }
                // 更新点赞数量
                var likes_num = $(obj).children('#likes_num');
                likes_num.text(data['likes_num']);
            } else {
                if (data['code'] == 401) {
                    $('#login_modal').modal();
                } else {
                    alert(data['message']);
                }

            }
        },
        error: function (xhr) {
            console.log(xhr);
        }
    })
}
