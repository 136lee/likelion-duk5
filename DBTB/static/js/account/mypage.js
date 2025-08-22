document.addEventListener("DOMContentLoaded", function () {
  const bookImg = document.getElementById("Postsc");

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


// 프로필사진
document.addEventListener('DOMContentLoaded', function() {

  const imagePreviewBox = document.getElementById('image-preview-box');
  const imageInput = document.getElementById('image-input');       
  const imagePreview = document.getElementById('postpf');                

  imagePreviewBox.addEventListener('click', function() {
    imageInput.click();
  });

  imageInput.addEventListener('change', function(event) {
    const file = event.target.files[0];

    if (file) {
      const reader = new FileReader();

      reader.onload = function(e) {
        imagePreview.src = e.target.result;
      }

      reader.readAsDataURL(file);
    }
  });

});

// 스크랩
  // document.addEventListener('DOMContentLoaded', function() {
  //   // 모든 스크랩 form 선택
  //   const scrapForms = document.querySelectorAll('.scrap_form');
  
  //   scrapForms.forEach(form => {
  //     form.addEventListener('submit', function(e) {
  //       e.preventDefault(); // 페이지 새로고침 방지
  
  //       const url = this.action;
  //       const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;
  //       const formData = new FormData(this);

  //       // 현재 form에서 가장 가까운 article.feed_article 요소를 찾습니다.
  //       const articleElement = this.closest('article.feed_article');
  
  //       fetch(url, {
  //         method: 'POST',
  //         headers: {
  //           'X-CSRFToken': csrfToken,
  //           'X-Requested-With': 'XMLHttpRequest'
  //         },
  //         body: formData
  //       })
  //       .then(response => response.json())
  //       .then(data => {
  //           // 스크랩 수 갱신
  //           const scrapNumber = this.querySelector('.scrap_number');
  //           if (scrapNumber) {
  //               scrapNumber.textContent = data.count;
  //           }

  //           // 이미지 갱신
  //           const scrapImg = this.querySelector('.scrap_img');
  //           if (scrapImg) {
  //             scrapImg.src = data.scrapped
  //               ? "{% static 'img/added_scrap.png' %}"
  //               : "{% static 'img/scrap.png' %}";
  //           }

  //           // --- ✨ 추가된 부분 ---
  //           // 만약 현재 페이지가 '마이스크랩' 페이지이고, 사용자가 스크랩을 취소했다면,
  //           // 해당 게시물을 화면에서 제거합니다.
  //           // 참고: 이 로직은 모든 피드 페이지에서 동일하게 동작하므로,
  //           // '마이스크랩' 페이지에서만 동작하게 하려면 추가적인 조건(예: URL 확인)이 필요할 수 있습니다.
  //           if (!data.scrapped && articleElement) {
  //               articleElement.remove();
  //           }
  //       })
  //       .catch(err => console.error(err));
  //     });
  //   });
  // });
  document.addEventListener('DOMContentLoaded', function() {
  // --- 프로필 이미지 변경 로직 (기존에 있었다면 유지) ---
  const imageInput = document.getElementById('image-input');
  const previewBox = document.getElementById('image-preview-box');
  const profileImage = previewBox.querySelector('img');

  previewBox.addEventListener('click', function() {
    imageInput.click();
  });

  imageInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        profileImage.src = e.target.result;
        // 선택적으로 여기서 form을 바로 submit 할 수도 있습니다.
        // document.getElementById('profile-image-form').submit();
      }
      reader.readAsDataURL(file);
    }
  });


  // --- ✨ 스크랩 기능 로직 ✨ ---
  const scrapForms = document.querySelectorAll('.scrap_form');
  
  // 프로필 상단의 전체 스크랩 개수를 표시하는 요소를 선택합니다.
  const totalScrapCountElement = document.querySelector('#myAtSbMd .myAtSbDTTN');

  scrapForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault(); // form의 기본 제출 동작(새로고침)을 막습니다.

      const url = this.action;
      const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;
      const formData = new FormData(this);

      // 제거할 스크랩 항목의 컨테이너를 찾습니다.
      // <form>에서 가장 가까운 <div id="myAsConSe">를 찾습니다.
      const scrapContainer = this.closest('#myAsConSe');

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest' // 비동기 요청임을 서버에 알립니다.
        },
        body: formData
      })
      .then(response => response.json()) // 서버의 응답을 JSON 형태로 파싱합니다.
      .then(data => {
        // data 객체는 Django view에서 JsonResponse로 보낸 값입니다.
        // 예: {'scrapped': False, 'count': 2}

        // 1. 개별 포스트의 스크랩 수 업데이트
        const scrapNumberSpan = this.querySelector('.scrap_number');
        if (scrapNumberSpan) {
          scrapNumberSpan.textContent = data.count;
        }

        // 2. 스크랩 버튼 이미지 업데이트
        const scrapImg = this.querySelector('img'); // form 안의 img 태그를 찾습니다.
        if (scrapImg) {
          if (data.scrapped) {
            // 스크랩이 추가된 경우 (마이페이지에서는 거의 발생하지 않음)
            scrapImg.src = "{% static 'img/bookmark.svg' %}"; // 채워진 북마크 이미지
          } else {
            // 스크랩이 취소된 경우
            scrapImg.src = "{% static 'img/bookmarkfull.svg' %}"; // 빈 북마크 이미지
          }
        }

        // 3. 스크랩이 취소되었다면 화면에서 해당 항목을 제거하고 전체 카운트 감소
        if (!data.scrapped && scrapContainer) {
          scrapContainer.remove(); // 컨테이너를 DOM에서 제거

          // 4. 프로필의 전체 스크랩 수 업데이트
          if (totalScrapCountElement) {
            let currentTotalCount = parseInt(totalScrapCountElement.textContent, 10);
            if (!isNaN(currentTotalCount) && currentTotalCount > 0) {
              totalScrapCountElement.textContent = currentTotalCount - 1;
            }
          }
        }
      })
      .catch(err => console.error('스크랩 처리 중 오류 발생:', err));
    });
  });
});



// 수
document.addEventListener('DOMContentLoaded', function() {

  // ... (프로필 이미지 변경 기능은 이전과 동일) ...
  const imageForm = document.getElementById('profile-image-form');
  const imageInput = document.getElementById('image-input');
  const previewBox = document.getElementById('image-preview-box');
  if (previewBox) {
    previewBox.addEventListener('click', () => imageInput.click());
  }
  if (imageInput) {
    imageInput.addEventListener('change', () => {
      const file = imageInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          document.getElementById('profile-image-preview').src = e.target.result;
        };
        reader.readAsDataURL(file);
        imageForm.submit();
      }
    });
  }

  const scrapForms = document.querySelectorAll('.scrap_form');
  const totalScrapCountElement = document.querySelector('#myAtSbMd .myAtSbDTTN');
  const scrapListContainer = document.getElementById('scrap-list-container');
  const noScrapMessage = scrapListContainer ? scrapListContainer.querySelector('.nopoS') : null;

  scrapForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();

      const url = this.action;
      const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;
      const formData = new FormData(this);
      const scrapContainer = this.closest('.myAsConSe');

      fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken, 'X-Requested-With': 'XMLHttpRequest' },
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        // data.scrapped가 true이면 스크랩 추가, false이면 스크랩 취소
        
        // ✨ --- 기능 추가: 전체 스크랩 수 업데이트 --- ✨
        if (totalScrapCountElement) {
          let currentTotalCount = parseInt(totalScrapCountElement.textContent, 10);
          
          if (data.scrapped) {
            // 스크랩이 추가된 경우 (마이페이지에서는 거의 발생하지 않음)
            totalScrapCountElement.textContent = currentTotalCount + 1;
          } else {
            // 스크rap이 취소된 경우
            totalScrapCountElement.textContent = currentTotalCount - 1;
          }
        }

        // 스크랩이 취소된 경우에만 화면에서 항목 제거
        if (!data.scrapped && scrapContainer) {
          scrapContainer.style.transition = 'opacity 0.3s ease';
          scrapContainer.style.opacity = '0';
          setTimeout(() => {
            scrapContainer.remove();
            
            // 항목 제거 후 남은 개수 확인
            const remainingScraps = scrapListContainer.querySelectorAll('.myAsConSe').length;
            if (remainingScraps === 0 && noScrapMessage) {
              noScrapMessage.style.display = 'block';
            }
          }, 300);
        }
      })
      .catch(err => console.error('스크랩 처리 중 오류 발생:', err));
    });
  });
});
