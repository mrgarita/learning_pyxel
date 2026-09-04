/* ページ内ナビ（目次パネル ＋ 先頭へ戻るボタン）
   解説ページの <head> から読み込むだけで動く。HTML 側に目次を書く必要はなく、
   ページ内の h2 / h3 を拾って自動で組み立てる。
   すでに id がある見出し（備忘録の #hitbox-size など）はその id をそのまま使うので、
   外部からのリンクは壊れない。 */
(function () {
  "use strict";

  var MIN_HEADINGS = 3;      // 見出しがこれ未満のページには目次を出さない
  var SHOW_TOP_AFTER = 300;  // 「先頭へ」を出しはじめるスクロール量（ドット）
  var CURRENT_LINE = 120;    // 画面上端から何ドットの位置を「いま読んでいる場所」とみなすか
  var SMOOTH_LIMIT = 4000;   // これ以上スクロールしていたら、先頭へは一気に戻す（滑らかだと遅すぎる）

  // 目次に載せない見出し（カードの見出しや、補足ボックス内の見出しなど）
  var SKIP_INSIDE = ".card, .note, .warn, .term, figure, table";

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  ready(function () {
    var root = document.querySelector(".wrap") || document.body;

    var heads = Array.prototype.slice
      .call(root.querySelectorAll("h2, h3"))
      .filter(function (h) {
        return !h.closest(SKIP_INSIDE);
      });

    // ---- 入れ物を作る（見出しが少ないページでも「先頭へ」だけは使えるようにする）----
    var nav = document.createElement("div");
    nav.className = "pagenav";

    var panel = null;
    var links = [];

    if (heads.length >= MIN_HEADINGS) {
      panel = document.createElement("nav");
      panel.className = "pagenav-panel";
      panel.id = "pagenav-panel";
      panel.hidden = true;
      panel.setAttribute("aria-label", "このページの目次");

      var title = document.createElement("p");
      title.className = "pagenav-title";
      title.textContent = "このページの目次";
      panel.appendChild(title);

      var list = document.createElement("ul");

      heads.forEach(function (h, i) {
        if (!h.id) {
          h.id = "sec-" + (i + 1);   // id がない見出しにだけ後付けする
        }
        var li = document.createElement("li");
        li.className = h.tagName === "H3" ? "lv3" : "lv2";

        var a = document.createElement("a");
        a.href = "#" + h.id;
        a.textContent = h.textContent.trim();
        a.addEventListener("click", function () {
          close();
        });

        li.appendChild(a);
        list.appendChild(li);
        links.push(a);
      });

      panel.appendChild(list);
      nav.appendChild(panel);
    }

    var buttons = document.createElement("div");
    buttons.className = "pagenav-buttons";

    var topBtn = document.createElement("button");
    topBtn.type = "button";
    topBtn.className = "pagenav-btn pagenav-top";
    topBtn.innerHTML = "▲ <span>先頭へ</span>";
    topBtn.title = "ページの先頭にもどる";
    topBtn.hidden = true;
    topBtn.addEventListener("click", function () {
      // 距離が長いときに滑らかに動かすと、戻りきるまでとても待たされる。
      // 近いときだけアニメーションさせ、遠いときは一気に戻す。
      var smooth = !prefersReducedMotion() && window.scrollY <= SMOOTH_LIMIT;
      window.scrollTo({ top: 0, behavior: smooth ? "smooth" : "auto" });
      // 先頭に戻ったら URL のハッシュも消しておく（再読み込みで途中へ飛ばないように）
      if (location.hash && history.replaceState) {
        history.replaceState(null, "", location.pathname + location.search);
      }
    });
    buttons.appendChild(topBtn);

    var tocBtn = null;
    if (panel) {
      tocBtn = document.createElement("button");
      tocBtn.type = "button";
      tocBtn.className = "pagenav-btn pagenav-toc";
      tocBtn.innerHTML = "≡ <span>目次</span>";
      tocBtn.title = "このページの目次を開く";
      tocBtn.setAttribute("aria-expanded", "false");
      tocBtn.setAttribute("aria-controls", "pagenav-panel");
      tocBtn.addEventListener("click", function () {
        if (panel.hidden) {
          open();
        } else {
          close();
        }
      });
      buttons.appendChild(tocBtn);
    }

    nav.appendChild(buttons);
    document.body.appendChild(nav);

    // ---- 開閉 ----
    function open() {
      panel.hidden = false;
      tocBtn.setAttribute("aria-expanded", "true");
      markCurrent();
      var cur = panel.querySelector(".is-current");
      if (cur) {
        // いま読んでいる項目が隠れていたら見える位置まで送る
        var pt = panel.getBoundingClientRect().top;
        var ct = cur.getBoundingClientRect().top;
        panel.scrollTop += ct - pt - panel.clientHeight / 3;
      }
    }

    function close() {
      if (!panel || panel.hidden) return;
      panel.hidden = true;
      tocBtn.setAttribute("aria-expanded", "false");
    }

    if (panel) {
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") close();
      });
      document.addEventListener("click", function (e) {
        if (!nav.contains(e.target)) close();
      });
    }

    // ---- スクロールに合わせた表示切りかえ ----
    function markCurrent() {
      if (!links.length) return;
      var found = -1;
      for (var i = 0; i < heads.length; i++) {
        if (heads[i].getBoundingClientRect().top <= CURRENT_LINE) {
          found = i;
        } else {
          break;
        }
      }
      links.forEach(function (a, i) {
        a.classList.toggle("is-current", i === found);
      });
    }

    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        ticking = false;
        topBtn.hidden = window.scrollY < SHOW_TOP_AFTER;
        if (panel && !panel.hidden) markCurrent();
      });
    }

    function prefersReducedMotion() {
      return window.matchMedia &&
             window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  });
})();
