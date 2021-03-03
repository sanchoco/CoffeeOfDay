// 커피 좋아요
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

//커피 싫어요
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

// 글쓰기
function WriteComment(comment, number, nickname) {
    if (comment=='') {
        alert("내용을 입력해주세요.")
        window.location.reload()
        return
    } else if (!number || number== '' || !nickname || nickname == '') {
        alert("문제가 발생하였습니다. 다시 시도해주세요.")
        window.location.reload()
        return
    }
    $.ajax({
            type: 'POST',
            url: '/api/write',
            data: {comment: comment, number: number, nickname: nickname},
            success:function (response) {
                if (response['msg'] == 'error'){
                    alert("에러가 발생하였습니다. 다시 시도해주세요.")
                } else {
                    alert(response['msg'])
                }
                window.location.reload()
            },
            error:function (error){
                alert("다시 시도해주세요.")
                window.location.reload()
            }
    })
}

// 로그아웃
function deleteToken() {
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃 완료!')
    window.location.reload()
}