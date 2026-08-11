const search = document.querySelector("#search");
const state = document.querySelector("#state");
const summary = document.querySelector("#summary");
const list = document.querySelector("#entries");
let entries = [];

function render() {
  const query = search.value.trim().toLocaleLowerCase("pt-BR");
  const selectedState = state.value;
  const filtered = entries.filter((entry) => {
    const matchesTerm = !query || entry.term.toLocaleLowerCase("pt-BR").includes(query);
    const matchesState = !selectedState || entry.state === selectedState;
    return matchesTerm && matchesState;
  });
  summary.textContent = `${filtered.length} de ${entries.length} entradas · nenhuma entrada é canônica por padrão`;
  list.replaceChildren();
  filtered.slice(0, 200).forEach((entry) => {
    const item = document.createElement("li");
    const term = document.createElement("strong");
    term.textContent = entry.term;
    const meta = document.createElement("span");
    meta.textContent = ` — ${entry.state} · ${entry.version}`;
    item.append(term, meta);
    list.append(item);
  });
}

fetch("../data/lote_500_sementes.json")
  .then((response) => {
    if (!response.ok) throw new Error(`corpus indisponível: ${response.status}`);
    return response.json();
  })
  .then((corpus) => {
    entries = corpus.entries;
    [...new Set(entries.map((entry) => entry.state))].sort().forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      state.append(option);
    });
    render();
  })
  .catch((error) => {
    summary.textContent = `Falha fechada: ${error.message}`;
  });

search.addEventListener("input", render);
state.addEventListener("change", render);
