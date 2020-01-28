fetch(`http://localhost:8080/accueil`)
  .then(r => r.json())
  .then(data => {
    let txt = "";
    for (let i = 0; i < data.livres.length; i++) {
        txt += `
        <div>
        <h2>${data.livres[i].titre}</h2>
        <p>${data.livres[i].auteur}</p>
        </div>
        `;
    }
    document.querySelector("#livres").innerHTML = txt;
  });