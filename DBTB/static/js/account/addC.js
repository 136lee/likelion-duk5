// static/js/account/addC.js

document.addEventListener('DOMContentLoaded', () => {
  // --- 요소 선택 부분 (기존과 동일) ---
  const fileInput = document.getElementById('fileUpload');
  const addPhotoButton = document.getElementById('addPtCon');
  const previewImage = document.getElementById('adpts');
  const contentEl = document.getElementById('content');
  const aiBox = document.getElementById('aiPhotoBox');
  const loadingEl = document.getElementById('aiPhotoLoading');
  const resultEl = document.getElementById('aiPhotoResult');
  
  // ▼▼▼ 수정된 부분 ▼▼▼
  // 이제 'raw' 데이터만 받으므로, 세부 항목들은 직접 표시할 필요가 없습니다.
  // 대신 '본문에 반영'할 때 사용할 것이므로 그대로 둡니다.
  const moodEl = document.getElementById('aiMood');
  const emojisEl = document.getElementById('aiEmojis');
  const summaryEl = document.getElementById('aiSummary');
  const tagsEl = document.getElementById('aiTags');
  const applyBtn = document.getElementById('aiApply');

  const endpoint = document.getElementById('ai-photo-url')?.value;
  const csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]')?.value;
  let isAiAnalyzing = false;

  fileInput?.addEventListener('change', async (event) => {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    // --- 이미지 미리보기 (기존과 동일) ---
    const reader = new FileReader();
    reader.onload = function(e) {
      previewImage.src = e.target.result;
      addPhotoButton.style.display = 'none';
      previewImage.style.display = 'block';
    };
    reader.readAsDataURL(selectedFile);

    // --- AI 분석 요청 (기존과 동일) ---
    if (isAiAnalyzing) return;
    isAiAnalyzing = true;

    aiBox.style.display = 'block';
    loadingEl.style.display = 'block';
    loadingEl.textContent = 'AI가 사진을 분석하는 중…';
    resultEl.style.display = 'none';

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        body: formData,
      });

      const resultData = await response.json();

      if (!response.ok) {
        loadingEl.textContent = '분석 실패: ' + (resultData.detail || resultData.error || '서버 응답 오류');
        return;
      }

      // ▼▼▼ ★★★★★ 가장 중요한 수정 부분 ★★★★★ ▼▼▼
      // 서버가 보내준 'raw' 데이터를 '요약(summary)' 부분에 직접 표시합니다.
      summaryEl.textContent = resultData.raw || '분석 결과를 받지 못했습니다.';
      
      // 'raw' 데이터만 있으므로 나머지 필드는 비워둡니다.
      moodEl.textContent = '';
      emojisEl.textContent = '';
      tagsEl.textContent = '';

      // 로딩 메시지를 숨기고 결과 박스를 보여줍니다.
      loadingEl.style.display = 'none';
      resultEl.style.display = 'block';

    } catch (error) {
      loadingEl.textContent = '분석 중 오류 발생: ' + error.message;
      console.error("AI 분석 요청 오류:", error);
    } finally {
      isAiAnalyzing = false;
    }
  });

  // --- '본문에 반영' 버튼 기능 수정 ---
  applyBtn?.addEventListener('click', () => {
    if (!contentEl) return;
    
    // 이제 'raw' 데이터 (summaryEl에 표시된)만 본문에 반영합니다.
    const analysisResult = summaryEl.textContent;
    
    if (analysisResult) {
      // 기존 내용을 지우고 AI 분석 결과로 채웁니다.
      contentEl.value = analysisResult;
    }
  });
});

// 이미지 변경
// 페이지의 모든 요소가 로드된 후 스크립트 실행
    document.addEventListener('DOMContentLoaded', function() {

      // 미리보기 이미지와 숨겨진 파일 입력 요소를 가져옴
      const postImagePreview = document.getElementById('postImagePreview');
      const imageInput = document.getElementById('addfile');       
      
      // 두 요소가 모두 존재하는지 확인하여 오류 방지
      if (postImagePreview && imageInput) {
        
        // 1. 이미지 미리보기를 클릭했을 때의 동작 정의
        postImagePreview.addEventListener('click', function() {
          // 숨겨진 파일 입력(imageInput)을 클릭한 것처럼 동작시킴
          imageInput.click();
        });

        // 2. 파일 입력창에서 새로운 파일을 선택했을 때의 동작 정의
        imageInput.addEventListener('change', function(event) {
          // 사용자가 선택한 파일 가져오기
          const file = event.target.files[0];

          // 파일이 실제로 선택되었다면
          if (file) {
            // 파일을 읽기 위한 FileReader 객체 생성
            const reader = new FileReader();

            // 파일 읽기가 완료되었을 때 실행될 함수 정의
            reader.onload = function(e) {
              // 이미지 미리보기(postImagePreview)의 소스(src)를
              // 방금 읽은 파일의 데이터 URL로 교체함
              postImagePreview.src = e.target.result;
            }

            // FileReader가 파일을 데이터 URL 형태로 읽도록 명령
            reader.readAsDataURL(file);
          }
        });
      }
    });