<!-- 커피 목록 불러오기 -->
function showcoffee() {
    $.ajax({
        type: 'GET',
        url: '/api/list?sample_give=샘플데이터',
        data: {},
        success: function (response) {
            let coffees = response["coffee"]
            for (let i = 0; i < coffees.length; i++) {
                let name = coffees[i]["name"]
                let image = coffees[i]["img_url"]
                let like = coffees[i]["like"]
                let dislike = coffees[i]["dislike"]
                let total_like = coffees[i]["total_like"]
                let number = coffees[i]['product_id']
                let temp_html = `<div class="col-sm-6">
                                    <div class="card">
                                        <a href="/detail/${number}"><img src="${image}" class="card-img-top"></a>
                                        <div class="card-body">
                                            <p class="card-text" id="coffee_name">${name} (${total_like})</p>
                                        </div>
                                        <div class="card-body">
                                            <a href="#" onclick="likeCoffee('${name}')" class="card-link"> 좋아요! ${like}
                                                <span class="icon">
                                                    <i class="fas fa-thumbs-up"></i>
                                                </span>
                                            </a>
                                            <a href="#" onclick="DislikeCoffee('${name}')" class="card-link"> 싫어요! ${dislike}
                                                <span class="icon">
                                                    <i class="fas fa-thumbs-down"></i>
                                                </span>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                    `
                $('#coffee').append(temp_html)
            }
        }
    })
}

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

<!-- 커피찾기 -->

function search_coffee(name) {
    $.ajax({
        type: 'POST',
        url: '/api/search',
        data: {given_name: name},
        success: function (response) {
            $('#coffee').empty()
            let search = response["search_result"]
            let name = search["name"]
            let image = search["img_url"]
            let like = search["like"]
            let dislike = search["dislike"]
            let total_like = search["total_like"]
            let number = search['product_id']
            let temp_html = `<div class="col-sm-6">
                                <div class="card">
                                    <a href="#" onclick="coffee_details(${number})"><img src="${image}" class="card-img-top"></a>
                                    <div class="card-body">
                                        <p class="card-text" id="coffee_name">${name} (${total_like})</p>
                                    </div>
                                    <div class="card-body">
                                        <a href="#" onclick="likeCoffee('${name}')" class="card-link"> 좋아요! ${like}
                                            <span class="icon">
                                                <i class="fas fa-thumbs-up"></i>
                                            </span>
                                        </a>
                                        <a href="#" onclick="DislikeCoffee('${name}')" class="card-link"> 싫어요! ${dislike}
                                            <span class="icon">
                                                <i class="fas fa-thumbs-down"></i>
                                            </span>
                                        </a>
                                    </div>
                                </div>
                            </div>
                                `
            $('#coffee').append(temp_html)
        }
    })
}