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
  console.log('Saving data to Firestore');
  const dataRef = database.collection('textboxes').doc('data');
  dataRef.set({ textBoxes: textBoxes })
    .then(() => console.log('Data saved successfully'))
    .catch(error => console.error('Error saving data:', error));
}

function loadData() {
  console.log('Loading data from Firestore');
  const dataRef = database.collection('textboxes').doc('data');
  dataRef.get()
    .then(snapshot => {
      const storedData = snapshot.data();
      console.log('Stored Data:', storedData);
      if (storedData) {
        textBoxes = storedData.textBoxes;
        renderTextBoxes();
      }
    })
    .catch(error => {
      console.error('Error loading data:', error);
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

      // Add event listener for input
      textBox.addEventListener('input', function() {
        textBoxes.push({ section: section, value: textBox.value });
        saveData();
      });

      break;
    }
  }
}

function renderTextBoxes() {
  textBoxes.forEach(textBoxData => {
    const container = document.createElement("div");
    const textBox = document.createElement("textarea");
    textBox.value = textBoxData.value;
    container.appendChild(textBox);

    const sectionId = textBoxData.section.toLowerCase().replace(/ /g, '-');
    const sectionContainer = document.getElementById(sectionId);
    if (sectionContainer) {
      sectionContainer.parentNode.insertBefore(container, sectionContainer.nextSibling);
    }
  });
}

const textAreas = document.querySelectorAll('textarea');
textAreas.forEach(textArea => {
  textArea.addEventListener('input', saveData);
});

window.addEventListener('load', loadData);
