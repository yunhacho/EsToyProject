
$("#search_btn").click(function() {
    let keyword = document.getElementById("search_btn").value
    var tickerContainer = document.getElementById("tickerContainer")
    tickerContainer.hidden = false;//감춰놧던걸 다시 보이기
    var tickerList = document.getElementById("tickerList")
    tickerList.innerHTML = ""//이미 있던 결과 날리기
    event.preventDefault();//submit 없애 버리고
    searchToElasticSearch_keywordapi(keyword)
});


var search = document.getElementById('search')
search.addEventListener('keyup', function (){
        // 엔터키 입력 처리
    if (window.event.keyCode === 13) {
        // Cancel the default action, if needed
        // preventDefault() 를 사용해서 올바르지 않은 텍스트가 입력란에 입력되는것을 막습니다.
        window.event.preventDefault();
        // 검색어 버튼 클릭
        var submitBtn = document.getElementById('submitBtn')
        submitBtn.click();
    }

    var tickerList = document.getElementById('generalTopic')
    tickerList.innerHTML = ''
    var tickerList = document.getElementById('keyword')
    tickerList.innerHTML = ''
    var tickerList = document.getElementById('brand')
    tickerList.innerHTML = ''
    var tickerList = document.getElementById('category')
    tickerList.innerHTML = ''
    var tickerList = document.getElementById('ETFTopic')
    tickerList.innerHTML = ''

    var keyword = search.value
    if(keyword != ''){
        GeneralTopicSearch(keyword)
        KeywordSearch(keyword)
        BrandSearch(keyword)
        CategorySearch(keyword)
        ETFTopicSearch(keyword)
    }
})

// 일반 종목 검색
function GeneralTopicSearch(keyword) {
    $.ajax({
        type: 'GET',
        url: "/search?keyword=" + keyword,
        dataType: "json",
        error: function () {
            alert("통신실패");
        },
        success: function (data) {
            var tickerList = document.getElementById('generalTopic')
            tickerList.innerHTML=''
            for(i=0; i<data.length; i++){
                tickerList.innerHTML += '<tr><td colspan="2">' + data[i].item + '</td></tr>'
            }
        }
    })
}

// 키워드 검색
function KeywordSearch(keyword) {
    $.ajax({
        type: 'GET',
        url: "/keywordsearch?keyword=" + keyword,
        dataType: "json",
        error: function () {
            alert("통신실패");
        },
        success: function (data) {
            var tickerList = document.getElementById('keyword')
            tickerList.innerHTML=''
            for(i=0; i<data.length; i++){
                tickerList.innerHTML += '<tr><td>' + data[i].item + '</td> <td>'+ keyword+ '</td></tr>'
            }
        }
    })
}


// 브랜드 검색
function BrandSearch(keyword) {
    $.ajax({
        type: 'GET',
        url: "/brandsearch?keyword=" + keyword,
        dataType: "json",
        error: function () {
            alert("통신실패");
        },
        success: function (data) {
            var tickerList = document.getElementById('brand')
            tickerList.innerHTML=''
            for(i=0; i<data.length; i++){
                tickerList.innerHTML += '<tr><td>' + data[i].item + '</td> <td>'+ keyword+ '</td></tr>'
            }
        }
    })
}

// 카테고리 검색
function CategorySearch(keyword) {
    $.ajax({
        type: 'GET',
        url: "/categorysearch?keyword=" + keyword,
        dataType: "json",
        error: function () {
            alert("통신실패");
        },
        success: function (data) {
            var tickerList = document.getElementById('category')
            tickerList.innerHTML=''
            for(i=0; i<data.length; i++){
                tickerList.innerHTML += '<tr><td>' + data[i].item + '</td> <td>'+ keyword+ '</td></tr>'
            }
        }
    })
}
// ETF 검색
function ETFTopicSearch(keyword) {
    $.ajax({
        type: 'GET',
        url: "/etfsearch?keyword=" + keyword,
        dataType: "json",
        error: function () {
            alert("통신실패");
        },
        success: function (data) {
            var tickerList = document.getElementById('ETFTopic')
            tickerList.innerHTML=''
            for(i=0; i<data.length; i++){
                tickerList.innerHTML += '<tr><td colspan="2">' + data[i].item + '</td></tr>'
            }
        }
    })
}
