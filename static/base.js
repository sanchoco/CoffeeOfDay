<!-- 커피 좋아요 -->

function likeCoffee(name) {
    $.ajax({
        type: 'POST',
        url: '/api/like',
        data: {name_give: name},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    })
}

<!-- 커피 싫어요 -->

function DislikeCoffee(name) {
    $.ajax({
        type: 'POST',
        url: '/api/dislike',
        data: {name_give: name},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    })
}

function WriteComment() {
    $.ajax({
        type: "POST",
        url: "/detail/<number>",
        data: {comment_write: comment},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    })
}
