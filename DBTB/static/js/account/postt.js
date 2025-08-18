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
