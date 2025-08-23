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

document.addEventListener("DOMContentLoaded", function () {
  const joWrap = document.getElementById("PtBoxjo");
  const joH = document.getElementById("PtBoxSyjoH"); // 여기서 할 일
  const joN = document.getElementById("PtBoxSyjoN"); // 다음에 할 일
  const listBox = document.getElementById("PtBoxChList");

  const nowUrl = joWrap.dataset.nowUrl;
  const laterUrl = joWrap.dataset.laterUrl;

  // CSRF 가져오기 (form의 hidden input 또는 <meta name="csrf-token"> 중 하나)
  function getCSRFToken() {
    const inp = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (inp) return inp.value;
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute("content");
    return "";
  }

  function setActive(btn) {
    // 배경 리셋
    joH.style.backgroundColor = "";
    joN.style.backgroundColor = "";
    // 새로 활성화
    btn.style.backgroundColor = "#A9DFC0";
  }

  function renderList(items) {
    // 기존 내용 비우기
    listBox.innerHTML = "";
    listBox.style.display = "flex";
    listBox.style.flexDirection = "column";
    listBox.style.gap = "10px";

    if (!items || items.length === 0) {
      listBox.innerHTML = `<p style="margin:8px 0;">생성된 추천이 없습니다.</p>`;
      return;
    }

    items.forEach((txt, idx) => {
      const label = document.createElement("label");
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.id = `todo_${idx}`;
      const span = document.createElement("span");
      span.textContent = txt;

      label.appendChild(cb);
      label.appendChild(span);
      listBox.appendChild(label);
    });
  }

  async function fetchRecs(url) {
    const token = getCSRFToken();
    // 로딩 표시
    listBox.style.display = "block";
    listBox.innerHTML = `<p style="margin:8px 0;">불러오는 중...</p>`;

    const resp = await fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": token,
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`서버 오류: ${resp.status} ${text}`);
    }
    return resp.json();
  }

  joH.addEventListener("click", async (e) => {
    e.preventDefault();
    try {
      setActive(joH);
      const data = await fetchRecs(nowUrl);
      renderList(data.items);
    } catch (err) {
      console.error(err);
      listBox.innerHTML = `<p style="color:#c00;">불러오기 실패: ${err.message}</p>`;
    }
  });

  joN.addEventListener("click", async (e) => {
    e.preventDefault();
    try {
      setActive(joN);
      const data = await fetchRecs(laterUrl);
      renderList(data.items);
    } catch (err) {
      console.error(err);
      listBox.innerHTML = `<p style="color:#c00;">불러오기 실패: ${err.message}</p>`;
    }
  });
});