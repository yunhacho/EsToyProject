
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

    var autoSearchArea = document.getElementById('autoSearchArea')
    autoSearchArea.innerHTML='';

    var keyword = search.value
    if(keyword == ''){
        autoSearchArea.innerHTML='';
    }
    else{
        GeneralTopicSearch(keyword)
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
            console.log(data)
            var autoSearchArea = document.getElementById('autoSearchArea')
            let table = document.createElement('table')
            table.innerHTML = '<tr bgcolor="blue" align ="left"> <p><td colspan = "2" span style="color:black">일반 종목</td></p></tr>'
            for(i=0; i<data.length; i++){
                //let div = document.createElement('div')
                //let ul = document.createElement('ul')
                //ul.innerHTML = data[i].item
                table.innerHTML += '<tr><p><td colspan="2">' + data[i].item + '</td></p></tr>'
            }
            autoSearchArea.appendChild(table)
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
            console.log(data)
            var autoSearchArea = document.getElementById('autoSearchArea')
            let table = document.createElement('table')
            table.innerHTML = '<tr bgcolor="blue" align ="left"> <p><td colspan = "2" span style="color:white">일반 종목</td></p></tr>'
            for(i=0; i<data.length; i++){
                //let div = document.createElement('div')
                //let ul = document.createElement('ul')
                //ul.innerHTML = data[i].item
                table.innerHTML += '<tr><p><td colspan="2"' + data[i].item + '</td></p></tr>'
                autoSearchArea.appendChild(table)
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
            console.log(data)
            var autoSearchArea = document.getElementById('autoSearchArea')
            for(i=0; i<data.length; i++){
                //let div = document.createElement('div')
                let ul = document.createElement('ul')
                ul.innerHTML = data[i].item
                autoSearchArea.appendChild(ul)
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
            console.log(data)
            var autoSearchArea = document.getElementById('autoSearchArea')
            for(i=0; i<data.length; i++){
                //let div = document.createElement('div')
                let ul = document.createElement('ul')
                ul.innerHTML = data[i].item
                autoSearchArea.appendChild(ul)
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
            console.log(data)
            var autoSearchArea = document.getElementById('autoSearchArea')
            for(i=0; i<data.length; i++){
                //let div = document.createElement('div')
                let ul = document.createElement('ul')
                ul.innerHTML = data[i].item
                autoSearchArea.appendChild(ul)
            }
        }
    })
}
/*
function searchToElasticSearch_keywordapi(keyword) {
    $.ajax({
        type: 'GET',
        url: "/search?keyword=" + keyword,
        dataType: "json",
        error: function () {
            //alert("통신실패!!!!");
        },
        success: function (data) {
            console.log(data)
            var tickerList = document.getElementById("tickerList")
            for(i=0; i<data.length; i++){
                var row = "<tr> <td>" + data["item"] + "</td> <td>" + data['bzns_dtl_text'] + "</td> <td>" + data['oppr_tot_amt'] + "</td> </tr>"
                console.log(row)
                tickerList.innerHTML += row
            }
        }
    })
}
*/