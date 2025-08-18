// static/post/create.js
document.addEventListener('DOMContentLoaded', () => {
  // 요소들
  const imgInput   = document.getElementById('image');
  const contentEl  = document.getElementById('content');

  const box        = document.getElementById('aiPhotoBox');
  const loadingEl  = document.getElementById('aiPhotoLoading');
  const resultEl   = document.getElementById('aiPhotoResult');
  const moodEl     = document.getElementById('aiMood');
  const emojisEl   = document.getElementById('aiEmojis');
  const summaryEl  = document.getElementById('aiSummary');
  const tagsEl     = document.getElementById('aiTags');
  const applyBtn   = document.getElementById('aiApply');

  // 템플릿에서 전달된 값들
  const endpoint = document.getElementById('ai-photo-url')?.value || '/post/ai/photo/';
  const csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]')?.value || '';

  // ✅ 중복 호출 방지 플래그
  let aiBusy = false;

  imgInput?.addEventListener('change', async () => {
    if (!imgInput.files || !imgInput.files[0] || aiBusy) return;
    aiBusy = true;

    box.style.display = 'block';
    loadingEl.style.display = 'block';
    loadingEl.textContent = 'AI가 사진을 분석하는 중…';
    resultEl.style.display = 'none';

    try {
      const fd = new FormData();
      fd.append('image', imgInput.files[0]);

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        body: fd,
        credentials: 'same-origin',
      });

      const raw = await res.text();
      let j = {};
      try { j = JSON.parse(raw); } catch { j = { raw }; }

      if (res.status === 429) {
        loadingEl.textContent = '요청이 잠시 많아요. 잠시 후 다시 시도해 주세요.';
        return;
      }
      if (!res.ok) {
        loadingEl.textContent = '분석 실패: ' + (j.detail || j.error || res.status);
        return;
      }

      // 성공 표시
      loadingEl.style.display = 'none';
      resultEl.style.display = 'block';
      moodEl.textContent    = j.mood || '';
      emojisEl.textContent  = j.emojis || '';
      summaryEl.textContent = j.summary || (j.raw || '');
      tagsEl.textContent    = Array.isArray(j.tags) ? j.tags.join(', ') : '';
    } catch (e) {
      loadingEl.textContent = '분석 실패: ' + e.message;
    } finally {
      aiBusy = false;
    }
  });

  // “본문에 반영”
  applyBtn?.addEventListener('click', () => {
    if (!contentEl) return;
    const lines = [];
    if (summaryEl.textContent) lines.push(summaryEl.textContent);
    if (moodEl.textContent || emojisEl.textContent) lines.push(`분위기: ${moodEl.textContent} ${emojisEl.textContent}`);
    if (tagsEl.textContent) lines.push('#' + tagsEl.textContent.split(', ').join(' #'));
    const add = lines.join('\n');
    contentEl.value = (contentEl.value ? contentEl.value + '\n\n' : '') + add;
  });

  if (!res.ok) {
  const msg = j.detail || j.error || raw || res.status;
  loadingEl.textContent = '분석 실패: ' + msg;
  return;
}
});
