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