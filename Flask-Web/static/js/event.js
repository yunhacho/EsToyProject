
$("#submitBtn").click(function (event) {
    let word = document.getElementById("search").value
     var tickerContainer = document.getElementById("tickerContainer")
    tickerContainer.hidden = false;//감춰놧던걸 다시 보이기
    var tickerList = document.getElementById("tickerList")
    tickerList.innerHTML = ""//이미 있던 결과 날리기
    event.preventDefault();//submit 없애 버리고

     var bodyRow = "<tr> \
            <th scope='row' class = 'text-center align-middle'>"+id+"</th>\
            <td class = 'text-center align-middle'>"+result[i]+"</td>\
            <td id = 'wordcnt"+(id)+"' class = 'text-center align-middle'></td>\
            <td id = 'processtime"+(id)+"' class = 'text-center align-middle'></td>\
            <td class = 'text-center align-middle'>\
                 <button type='button' class='btn btn-outline-success analysisBtn' data-toggle='modal' data-target='#tfidfModal' name="+result[i]+">단어 분석</button>&nbsp;&nbsp;&nbsp;\
                 <button type='button' class='btn btn-outline-primary similarityBtn' data-toggle='modal' data-target='#similarityModal' name="+result[i]+">유사도</button>&nbsp;&nbsp;&nbsp;\
                 <button type='button' class='btn btn-outline-info wordCloudBtn' data-toggle='modal' data-target='#wordCloudModal' name="+result[i]+">워드 클라우드</button>\
            </td>\
        </tr> "
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
    searchToElasticSearch(keyword)
    if(keyword == ''){
        autoSearchArea.innerHTML='';
    }
})

function searchToElasticSearch(keyword) {
    $.ajax({
        type: 'GET',
        url: "/search?keyword=" + keyword,
        dataType: "json",
        error: function () {
            //alert("통신실패!!!!");
        },
        success: function (data) {
            console.log(data)
            var autoSearchArea = document.getElementById('autoSearchArea')
            for(i=0; i<data.length; i++){
                //let div = document.createElement('div')
                let ul = document.createElement('ul')
                ul.innerHTML = data[i].item
                ul.className =
                autoSearchArea.appendChild(ul)
            }
        }
    })
}

