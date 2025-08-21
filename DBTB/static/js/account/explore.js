// send 버튼 가져오기
const sendBtn = document.getElementById("sendBtn");

// 요소 가져오기
const questionBox = document.querySelector(".Question_box"); // 박스 전체
const leftBar = document.getElementById("leftBar");
const Recommend = document.querySelector(".AI_recommend"); 

// 처음에 왼쪽 바 숨김
leftBar.style.display = "none"; 

const conversation = document.querySelector(".conversation");
const Total = document.querySelector(".total");




// 클릭 이벤트
sendBtn.addEventListener("click", () => {
  // Question_box 스타일 변경
  questionBox.style.display = "flex";
  questionBox.style.flexDirection = "column";
  questionBox.style.justifyContent = "space-between";
  questionBox.style.width = "80%";
 
 
  // Question 텍스트는 숨기고 싶으면 따로 잡아서
  const questionText = document.querySelector(".Question");
  if (questionText) {
    questionText.style.display = "none";
  }

  // 왼쪽 바 보이게
  leftBar.style.display = "flex";
  Total.style.display = "flex";

  conversation.style.display = "flex";
  Recommend.style.display = "none";
});
