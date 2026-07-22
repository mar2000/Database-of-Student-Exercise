let selectedProblems = [];

const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[char]));

function problemCard(problem, index) {
  return `<article class="problem set-problem">
    <div class="top">
      <div>
        <small>Zadanie ${String(problem.number).padStart(4, '0')}</small>
        <h2>${index + 1}. ${escapeHtml(problem.title)}</h2>
      </div>
      <button data-id="${escapeHtml(problem.id)}" class="remove">Usuń</button>
    </div>
    <div class="math">${problem.statement}</div>
    <p class="source">Źródło: ${escapeHtml([
      problem.source?.type,
      problem.source?.name,
      problem.source?.academic_year
    ].filter(Boolean).join(' · '))}</p>
    ${problem.answer ? `<details><summary>Odpowiedź na stronie</summary><div class="answer-preview">${problem.answer}</div></details>` : ''}
  </article>`;
}

function exportProblem(problem, index) {
  return `<section class="pdf-problem">
    <div class="pdf-problem-header">
      <span>Zadanie ${index + 1}</span>
      <span>${escapeHtml(problem.title)}</span>
    </div>
    <div class="pdf-statement math">${problem.statement}</div>
    <div class="pdf-source">${escapeHtml([
      problem.source?.type,
      problem.source?.name,
      problem.source?.academic_year
    ].filter(Boolean).join(' · '))}</div>
  </section>`;
}

async function renderSet() {
  const response = await fetch('../data/catalog.json');
  const data = await response.json();
  selectedProblems = getSet()
    .map(id => data.problems.find(problem => problem.id === id))
    .filter(Boolean);

  const list = document.getElementById('set-list');
  list.innerHTML = selectedProblems.length
    ? selectedProblems.map(problemCard).join('')
    : '<div class="empty"><h2>Zestaw jest pusty</h2><p>Dodaj zadania na stronie wybranego przedmiotu.</p></div>';

  document.querySelectorAll('.remove').forEach(button => {
    button.onclick = () => {
      saveSet(getSet().filter(id => id !== button.dataset.id));
      renderSet();
    };
  });

  const exportButton = document.getElementById('export-pdf');
  exportButton.disabled = selectedProblems.length === 0;

  if (window.MathJax?.typesetPromise) {
    await MathJax.typesetPromise([list]);
  }
}

async function exportPdf() {
  if (!selectedProblems.length) return;

  const button = document.getElementById('export-pdf');
  const status = document.getElementById('export-status');
  const root = document.getElementById('pdf-export-root');

  if (!window.html2pdf) {
    status.textContent = 'Nie udało się załadować modułu eksportu PDF. Sprawdź połączenie z internetem i odśwież stronę.';
    return;
  }

  button.disabled = true;
  button.textContent = 'Tworzenie PDF…';
  status.textContent = 'Przygotowuję skład matematyczny i strony dokumentu.';

  const date = new Date();
  const dateLabel = new Intl.DateTimeFormat('pl-PL', {
    day: '2-digit', month: '2-digit', year: 'numeric'
  }).format(date);

  root.innerHTML = `<div class="pdf-document">
    <header class="pdf-title-page">
      <div class="pdf-brand">Baza zadań studenckich</div>
      <h1>Zestaw zadań</h1>
      <p>Liczba zadań: ${selectedProblems.length}</p>
      <p>Data wygenerowania: ${escapeHtml(dateLabel)}</p>
    </header>
    <main class="pdf-problems">${selectedProblems.map(exportProblem).join('')}</main>
  </div>`;
  root.classList.add('pdf-export-active');

  try {
    if (window.MathJax?.typesetPromise) {
      await MathJax.typesetPromise([root]);
    }

    // MathJax może dodawać niewidoczne warstwy dostępnościowe. Przeglądarkowy
    // renderer HTML->canvas potrafi je błędnie narysować obok właściwego wzoru.
    root.querySelectorAll('mjx-assistive-mml, .MJX_Assistive_MathML').forEach(node => node.remove());
    root.querySelectorAll('mjx-container').forEach(container => {
      container.removeAttribute('tabindex');
      container.setAttribute('aria-hidden', 'true');
    });

    await document.fonts.ready;
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));

    const filenameDate = date.toISOString().slice(0, 10);
    const options = {
      margin: [12, 14, 14, 14],
      filename: `zestaw-zadan-${filenameDate}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: {
        scale: 1.6,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false
      },
      jsPDF: {
        unit: 'mm',
        format: 'a4',
        orientation: 'portrait',
        compress: true
      },
      pagebreak: {
        mode: ['css', 'legacy'],
        before: '.pdf-page-break',
        avoid: ['.pdf-problem-header']
      }
    };

    await html2pdf().set(options).from(root.firstElementChild).save();
    status.textContent = 'Plik PDF został wygenerowany i pobrany.';
  } catch (error) {
    console.error(error);
    status.textContent = 'Nie udało się wygenerować PDF. Odśwież stronę i spróbuj ponownie.';
  } finally {
    root.classList.remove('pdf-export-active');
    root.innerHTML = '';
    button.disabled = selectedProblems.length === 0;
    button.textContent = 'Eksportuj zadania do PDF';
  }
}

document.getElementById('clear-set').onclick = () => {
  saveSet([]);
  renderSet();
};

document.getElementById('export-pdf').onclick = exportPdf;
renderSet();
