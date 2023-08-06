function getHashUrl() {
	return location.hash.substring(1);
}

function isInArray(item, arr) {
	let isin = false;
	for(let i of arr) {
		if(i == item)
			isin = true;
	}
	return isin;
}

function getClassNameArray(objs, arr=[]) {
	let regex = /[a-z0-9]+-page/
	for(obj of objs) {
		for(cls of obj.classList) {
			if(cls.search(regex)>=0) {
				arr.push(cls.split('-')[0]);
			}
		}
	}
	return arr;
}

function hashChange() {
	let url = getHashUrl();
	$('.active').removeClass('active');
	$(`.menu-item-${url}`).addClass('active');
	let childrens = $('.body').children();
	let classArr = getClassNameArray(childrens, [''])
	$.map(childrens, value=>$(value).css('display','none'));
	$(`.${url}-page`).css('display','block');
	if(!url) {
		let name = classArr[1]
		$(`.${name}-page`).css('display','block');
		$(`.menu-item-${name}`).addClass('active');
	}
	if(!isInArray(url, classArr)) {
		$('.404-page').css('display', 'block');
	}
}

// 哈希事件
window.onhashchange = hashChange;

$(function() {
	let isShow = false;
	hashChange();
	// 小尺寸横条展开
	$('.heng-icon').click(event => {
		if (!isShow) {
			$('.hidden-list').animate({height: "250px"}, 200)
			isShow = true;
		}
		else {
			$('.hidden-list').animate({height: '0px'}, 200);
			isShow = false;
		}
	})
})
