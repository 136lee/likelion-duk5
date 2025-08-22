document.addEventListener("DOMContentLoaded", function () {
  const ellipsis = document.getElementById("ellipsis");
  const reMo = document.getElementById("reMo");

  ellipsis.addEventListener("click", function (e) {
    e.stopPropagation();
    reMo.classList.toggle("show");
  });

  document.addEventListener("click", function (e) {
    if (!reMo.contains(e.target) && e.target !== ellipsis) {
      reMo.classList.remove("show");
    }
  });
});

// 스크랩수
document.addEventListener("DOMContentLoaded", function () {
  const PlNameSc = document.getElementById("PlNameSc");
  const PlNameScCount = document.getElementById("PlNameScCount");
  let liked = false;

  PlNameSc.addEventListener("click", function () {
    let count = parseInt(PlNameScCount.innerText, 10);

    if (!liked) {
      PlNameScCount.innerText = count + 1;
    } else {
      PlNameScCount.innerText = count - 1;
    }
    liked = !liked;
  });
});

// 여기서 할일
const joH = document.getElementById("PtBoxSyjoH");
const joN = document.getElementById("PtBoxSyjoN");
const CHhd = document.getElementById("PtBoxChList");

function resetBackground() {
  joH.style.backgroundColor = "";
  joN.style.backgroundColor = "";
  CHhd.style.display = "none";
}

let activeBtn = null;

joH.addEventListener("click", () => {
  if (activeBtn === joH) {
    resetBackground();
    activeBtn = null;
  } else {
    resetBackground();
    joH.style.backgroundColor = "#A9DFC0";
    CHhd.style.display = "flex";
    activeBtn = joH;
  }
});

joN.addEventListener("click", () => {
  if (activeBtn === joN) {
    resetBackground();
    activeBtn = null;
  } else {
    resetBackground();
    joN.style.backgroundColor = "#A9DFC0";
    activeBtn = joN;
  }
});

// 스크랩
document.addEventListener("DOMContentLoaded", function () {
  const bookImg = document.getElementById("pstSc");

  const fbookImg = [
    "/DBTB/static/img/bookmark.svg", // 현재 이미지
    "/DBTB/static/img/bookmarkfull.svg", // 교체 이미지
  ];

  let current = 0;

  bookImg.addEventListener("click", function () {
    current = (current + 1) % fbookImg.length;
    bookImg.src = fbookImg[current];
    bookImg.classList.toggle("filled"); 
  });
});

//따봉
document.addEventListener('DOMContentLoaded', function() {

  const likeButton = document.getElementById("PtBoxSyGBG");
  const dislikeButton = document.getElementById("PtBoxSyGBB");

  let activeButton = null; 

  function resetFeedbackStyles() {
    likeButton.style.backgroundColor = "";
    dislikeButton.style.backgroundColor = ""; 
  }

  likeButton.addEventListener("click", () => {
    if (activeButton === likeButton) {
      resetFeedbackStyles(); 
      activeButton = null; 
    } 

    else {
      resetFeedbackStyles(); 
      likeButton.style.backgroundColor =  "#A9DFC0";; 
      activeButton = likeButton;
    }
  });

  dislikeButton.addEventListener("click", () => {

    if (activeButton === dislikeButton) {
      resetFeedbackStyles();
      activeButton = null;
    } 

    else {
      resetFeedbackStyles();
      dislikeButton.style.backgroundColor =  "#A9DFC0";;
      activeButton = dislikeButton;
    }
  });
});


// 스크랩
document.addEventListener('DOMContentLoaded', function() {
  
  const scrapForms = document.querySelectorAll('.scrap_form');

  scrapForms.forEach(form => {
    form.addEventListener('submit', function(event) {
      event.preventDefault();

      const url = this.action;
      const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;
      const button = this.querySelector('button[type="submit"]');

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest'
        },
      })
      .then(response => {
        if (!response.ok) throw new Error('서버 응답 오류');
        return response.json();
      })
      .then(data => {
        
        // 1. 스크랩 수 갱신
        const scrapNumberSpan = this.querySelector('.scrap_number');
        if (scrapNumberSpan) {
          scrapNumberSpan.textContent = data.count;
        }

        // 2. 스크랩 이미지 갱신
        const scrapImg = this.querySelector('.scrap_img');
        const scrappedImgSrc = button.dataset.scrappedSrc;
        const unscrappedImgSrc = button.dataset.unscrappedSrc;

        if (scrapImg) {
          scrapImg.src = data.scrapped ? scrappedImgSrc : unscrappedImgSrc;
        }
      })
      .catch(err => console.error('스크랩 처리 중 오류 발생:', err));
    });
  });
});