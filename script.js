const firebaseConfig = {
  apiKey: "AIzaSyBvvuTg6O_L4qtyRcyueFo8x-M9SfDG6sY",
  authDomain: "capsoteweb.firebaseapp.com",
  projectId: "capsoteweb",
  storageBucket: "capsoteweb.appspot.com",
  messagingSenderId: "514921944177",
  appId: "1:514921944177:web:2516e643f946e994ccf7d0",
  measurementId: "G-24V83F2TF2"
};


firebase.initializeApp(firebaseConfig);
const database = firebase.database();

let textBoxes = [];

function saveData() {
  const dataRef = database.ref('textboxes');
  dataRef.set(textBoxes);
}

function loadData() {
  const dataRef = database.ref('textboxes');
  dataRef.once('value')
    .then(snapshot => {
      const storedData = snapshot.val();
      if (storedData) {
        textBoxes = storedData;
        renderTextBoxes();
      }
    });
}

function addResizableTextBox(section) {
  const container = document.createElement("div");
  const textBox = document.createElement("textarea");
  textBox.setAttribute("rows", "4");
  textBox.setAttribute("cols", "50");
  container.appendChild(textBox);

  const titleContainers = document.querySelectorAll('.title-container');
  for (let i = 0; i < titleContainers.length; i++) {
    if (titleContainers[i].textContent.includes(section)) {
      titleContainers[i].parentNode.insertBefore(container, titleContainers[i].nextSibling);
      break;
    }
  }

  textBoxes.push({ section: section, value: textBox.value });
  saveData();
}

function renderTextBoxes() {
  textBoxes.forEach(textBoxData => {
    const container = document.createElement("div");
    const textBox = document.createElement("textarea");
    textBox.value = textBoxData.value;
    container.appendChild(textBox);
    document.getElementById(textBoxData.section.toLowerCase().replace(/ /g, '-')).parentNode.insertBefore(container, document.getElementById(textBoxData.section.toLowerCase().replace(/ /g, '-')).nextSibling);
  });
}

window.addEventListener('load', loadData);

const textAreas = document.querySelectorAll('textarea');
textAreas.forEach(textArea => {
  textArea.addEventListener('input', saveData);
});
