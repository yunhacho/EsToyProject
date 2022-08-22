let Setting = {
    expandedFlags: {} // 멀리플 셀렉트박스 펼침 여부 플래그
    , holdOnTimeout: {} // 자동검색완성 setTimeout id
    , completeFlags: {} // 자동검색완성 값선택 완성 여부 플래그
    , highlightTxt: "txt-red"
    , showHideCkArea: function(innerSelectBoxId, selectAreaId, dataId) {
        let innerSelectBox = document.getElementById(innerSelectBoxId);
        let selectedArea = document.getElementById(selectAreaId);

        innerSelectBox.addEventListener("click", function(e){
            if (!Setting.expandedFlags[selectAreaId]) {
                selectedArea.style.display = "block";
                Setting.expandedFlags[selectAreaId] = true;
            } else {
                selectedArea.style.display = "none";
                Setting.expandedFlags[selectAreaId] = false;
            }
        });

        document.body.addEventListener("click", event => {
            if(Setting.expandedFlags[selectAreaId]
                && event.target.dataset.id != dataId
            ){
                console.log("숨기시오.");
                selectedArea.style.display = "none";
                Setting.expandedFlags[selectAreaId] = false;
            }
        });

    }
}

let SelectUserSetting = {
    isRedText: false
}

const SelectDataFunc = {
    /**
     * 체크된 셀렉트박스 값을 배열로 반환
     * @param {string} inputName input tag name
     * @returns array
     */
    getSelectedDataArr: function (inputName) {
        let ckValArray = new Array();

        let ckEle = document.getElementsByName(inputName);
        for (let i = 0; i < ckEle.length; i++) {
            if (ckEle[i].checked) {
                ckValArray.push(ckEle[i].value);
            }
        }
        return ckValArray;
    }
}

const SelectDataHandling = {
    /**
     * 검색 단어 매칭해서 일치하는 부분만 색깔 칠해서 반환
     * @param {stirng} str 검색된 전체 단어
     * @param {string} searchingValue 검색 단어
     * @returns
     */
    highlightMathedStr: function(str, searchingValue){
        const regExp = new RegExp(searchingValue, "gi");
        let matchedStr = str.match(regExp);

        let highlightedStr = "<span style='color: #6BD089'>" + matchedStr + "</span>"
        return str.replace(regExp, highlightedStr);
    }
}

const SelectEventFunc = {
    /**
     * 자동 검색 완성
     * @param {string} searchInputId 검색 input id
     * @param {string} selectDivId 검색결과 div id
     * @param {method} getDataListMethod 검색어 입력 시 실행할 메서드
     */
    autoSearch: function(searchInputId, selectDivId, getDataListMethod){
        let searchInput = document.getElementById(searchInputId);

        searchInput.addEventListener("keydown", event => {
            if(event.code === "ArrowUp" || event.code === "ArrowDown" || event.code === "Enter"){
                // 화살표 위아래 혹은 엔터 눌렀을 때 실행
                let selectDiv = document.getElementById(selectDivId);
                let selectDivDisplay = selectDiv.style.display;
                let selectLabel = selectDiv.children;
                /**
                 * 한글/한자/히라가나,가타가나의 경우 갓 입력했을 때 keyCode가 229이거나 isComposing이 true를 반환
                 * 이 조건을 추가하지 않으면 가장 처음의 이벤트는 두 번 발생하는 참사가..
                 * 가능하면 change 이벤트를 사용하는 게 좋음.
                */
                if(selectDivDisplay === "block" && event.keyCode != 229 && !event.isComposing){
                    if(event.code == "ArrowUp"){
                        // 화살표 위↑ 누름
                        Setting.holdOnTimeout[searchInputId] = setTimeout(SelectEventFunc.arrowUp(selectLabel), 500);
                    }else if(event.code == "ArrowDown"){
                        // 화살표 아래↓ 누름
                        Setting.holdOnTimeout[searchInputId] = setTimeout(SelectEventFunc.arrowDown(selectLabel), 500);
                    }else if(event.code == "Enter"){
                        // 엔터┘ 누름
                        // 엔터 누르면 클릭해줌. 이미 클릭 이벤트가 걸려있기 때문에 이벤트에 걸려있는 메서드가 실행될 것임.
                        let selectedHover = document.getElementsByClassName("selectAreaHover")[0];
                        if(selectedHover) selectedHover.click();
                    }
                }
            }
        });

        // 검색 Input에 키를 누르고 뗐을 때의 이벤트
		searchInput.addEventListener("keyup", event => {
            if(event.code != "ArrowUp" && event.code != "ArrowDown" && event.code != "Enter"){
                getDataListMethod(searchInput); // 글자 입력했을 때 실행
                if(event.code != "ArrowLeft" && event.code != "ArrowRight"){
                    if(SelectUserSetting.isRedText){
                        searchInput.classList.add(Setting.highlightTxt); // 빨간색 글씨 On
                    }
                    Setting.completeFlags[searchInputId] = false; // 자동검색 미완성
                }
            }else{
                // 화살표 위아래 혹은 엔터 눌렀다 뗐을 때 실행
                SelectEventFunc.stopArrowKey(searchInputId);
            }
		});
    },
    stopArrowKey: function(searchInputId){
        clearTimeout(Setting.holdOnTimeout[searchInputId]);
        Setting.holdOnTimeout[searchInputId] = -1;
    },
    arrowUp: function(selectLabel){
        loop1: for (let i = 0; i < selectLabel.length; i++) {
            let labelClasses = selectLabel[i].classList;
            for (let j = 0; j < labelClasses.length; j++) {
                if (labelClasses[j] == "selectAreaHover") {
                    if (selectLabel[i - 1]) {
                        selectLabel[i].classList.remove("selectAreaHover");
                        selectLabel[i - 1].classList.add("selectAreaHover");
                    } else if (i == 0) {
                        // 첫번째 라벨일 때 제일 아래로 이동
                        selectLabel[i].classList.remove("selectAreaHover");
                        selectLabel[selectLabel.length - 1].classList.add("selectAreaHover");
                    }
                    break loop1;
                }
            }
        }
    },
    arrowDown: function(selectLabel){
        let isHovered = false;
        loop1:
        for(let i=0; i<selectLabel.length; i++){
            let labelClasses = selectLabel[i].classList;
            for(let j=0; j<labelClasses.length; j++){
                if(labelClasses[j] == "selectAreaHover"){
                    isHovered = true;
                    if(selectLabel[i+1]) {
                        selectLabel[i].classList.remove("selectAreaHover");
                        selectLabel[i+1].classList.add("selectAreaHover");
                    }else if(i+1 == selectLabel.length){
                        // 마지막 라벨일 때 제일 위로 이동
                        selectLabel[i].classList.remove("selectAreaHover");
                        selectLabel[0].classList.add("selectAreaHover");
                    }
                    break loop1;
                }
            }
        }
        // 선택된 것이 아무것도 없다면 첫번째 선택
        if(isHovered == false){
            selectLabel[0].classList.add("selectAreaHover");
        }
    },
    hoverSelectLabelMouse: function(selectDivId){
        // 검색 셀렉트 div label에 마우스 오버/아웃했을 때의 이벤트
        let selectLabel = document.getElementById(selectDivId).children;
        for(let i=0; i<selectLabel.length; i++){
            selectLabel[i].addEventListener("mouseover", event => {
                selectLabel[i].classList.add("selectAreaHover");
            });
            selectLabel[i].addEventListener("mouseout", event => {
                selectLabel[i].classList.remove("selectAreaHover");
            });
        }
    },
    /**
     * 검색 결과 라벨 클릭 이벤트
     * @param {string} searchInputId 검색 input id
     * @param {string} searchAreaId 검색결과 div id
     * @param {string} lavelClassNm 라벨의 클래스명
     * @param {method} callbackMethod 검색 결과 라벨 클릭 시 실행될 메서드
     */
     clickAutoSearchingLavel: function(searchInputId, searchAreaId, lavelClassNm, callbackMethod){
		let searchingLaveles = document.getElementsByClassName(lavelClassNm);
		for (let i = 0; i < searchingLaveles.length; i++) {
			searchingLaveles[i].addEventListener("click", event => {
				let fillValue = searchingLaveles[i].dataset.value;
				callbackMethod(fillValue, searchInputId, searchAreaId);
			});
		}
	},
    /**
     * 검색 input에서 포커스 아웃 시
     * 자동검색완성이 미완일 경우, 즉 검색된 라벨 목록에서 클릭이나 엔터로 선택된 값이 아닐 경우,
     * 검색 input에 있는 텍스트는 지워준다.
     * @param {String} searchInputId 검색 input id
     * @param {String} searchAreaId 검색결과 div id
     */
    eraseIncompletion: function(searchInputId, searchAreaId){
        document.getElementById(searchInputId).addEventListener("focusout", event => {
            if(!Setting.completeFlags[searchInputId]){
                document.getElementById(searchInputId).value = "";
                document.getElementById(searchAreaId).style.display = "none";
            }
        });
    }

}

const SelectCallback = {
    /**
     * 선택한 값을 어떻게 할 것인지 여기서 처리
     * @param {String} fillValue 채워야 할 값. 즉 검색된 라벨 목록에서 클릭이나 엔터로 선택된 값
     * @param {String} objId 검색 input id
     * @param {String} searchAreaId 검색결과 div id
     */
    fillSelectedValue: function(fillValue, objId, searchAreaId){
        document.getElementById(objId).classList.remove(Setting.highlightTxt); // 빨간색 글씨 Off
        Setting.completeFlags[objId] = true; // 자동검색 완성

        document.getElementById(objId).value = fillValue;
        document.getElementById(searchAreaId).style.display = "none";
    }
}