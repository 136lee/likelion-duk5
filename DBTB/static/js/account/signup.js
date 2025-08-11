// 체크박스 요소(전체동의)
document.addEventListener("DOMContentLoaded", function () {
  const master = document.getElementById("agreeAll");
  const items = Array.from(document.querySelectorAll("input.agree")); //하위 체크박스

  if (!master || items.length === 0) return;

  // 전체동의 클릭->모두클릭
  master.addEventListener("change", () => {
    items.forEach((cb) => (cb.checked = master.checked));
    master.indeterminate = false;
  });

  // 하위 체크 상태 업데이트
  const updateMasterState = () => {
    const checkedCount = items.filter((cb) => cb.checked).length;
    if (checkedCount === 0) {
      master.checked = false;
      master.indeterminate = false;
    } else if (checkedCount === items.length) {
      master.checked = true;
      master.indeterminate = false;
    }
  };

  items.forEach((cb) => cb.addEventListener("change", updateMasterState));

  updateMasterState();
});

//폼 제출 필수요소 점검
document.querySelector("form").addEventListener("submit", function (e) {
  e.preventDefault(); //기본 제출 제한

  const name = document.getElementById("LId").value.trim();
  const email = document.querySelector('input[type="email"]').value.trim();
  const pw1 = document.querySelectorAll('input[type="password"]')[0].value;
  const pw2 = document.querySelectorAll('input[type="password"]')[1].value;
  const requiredChecks = document.querySelectorAll(".agree");

  if (!name) {
    alert("이름을 입력하세요.");
    return;
  }

  if (!email || !email.includes("@")) {
    alert("올바른 이메일 주소를 입력하세요.");
    return;
  }

  const pwRegex =
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,20}$/;
  if (!pwRegex.test(pw1)) {
    alert("비밀번호는 영문, 숫자, 특수문자를 포함한 8~20자여야 합니다.");
    return;
  }

  if (pw1 !== pw2) {
    alert("비밀번호가 일치하지 않습니다.");
    return;
  }

  for (let check of requiredChecks) {
    if (!check.checked) {
      alert("필수 약관에 모두 동의해야 합니다.");
      return;
    }
  }

  e.target.submit();
});
