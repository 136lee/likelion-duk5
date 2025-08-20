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